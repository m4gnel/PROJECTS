package com.agrisage.app.data.sync

import android.content.Context
import android.provider.Settings
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.local.dao.SyncQueueDao
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.SyncUploadRequest
import com.agrisage.app.data.repository.AuthRepository
import com.google.gson.Gson
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import kotlinx.coroutines.CancellationException

@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted workerParams: WorkerParameters,
    private val syncQueueDao: SyncQueueDao,
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        if (BuildConfig.REFERENCE_PREVIEW) return Result.failure()
        // Keep local observations while signed out; the next periodic run
        // after authentication will upload them.
        if (!authRepository.hasSession()) return Result.success()

        val pendingItems = syncQueueDao.getUnsyncedByPriority()
        var shouldRetry = false
        var hasUnconfirmedUploads = false
        val deviceId = Settings.Secure.getString(
            applicationContext.contentResolver,
            Settings.Secure.ANDROID_ID,
        ) ?: "unknown_device"

        for (item in pendingItems) {
            try {
                @Suppress("UNCHECKED_CAST")
                val payload = Gson().fromJson(item.payloadJson, Map::class.java)
                    as? Map<String, Any?>
                    ?: throw IllegalArgumentException("Sync payload is not an object")
                val response = apiService.uploadSyncBatch(
                    SyncUploadRequest(
                        observations = listOf(payload),
                        deviceId = deviceId,
                    )
                )
                if (response.isSuccessful && response.body()?.confirmsPersistedObservation(item.entityId) == true) {
                    syncQueueDao.deleteById(item.id)
                } else {
                    hasUnconfirmedUploads = true
                    syncQueueDao.incrementRetryCount(item.id)
                    shouldRetry = shouldRetry || response.code() >= 500 || response.code() == 429
                }
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (e: Exception) {
                syncQueueDao.incrementRetryCount(item.id)
                shouldRetry = true
            }
        }

        return when {
            shouldRetry -> Result.retry()
            hasUnconfirmedUploads -> Result.failure()
            else -> Result.success()
        }
    }
}
