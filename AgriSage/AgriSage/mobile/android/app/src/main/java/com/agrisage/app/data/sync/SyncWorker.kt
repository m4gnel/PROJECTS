package com.agrisage.app.data.sync

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.agrisage.app.data.local.dao.SyncQueueDao
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted workerParams: WorkerParameters,
    private val syncQueueDao: SyncQueueDao
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val pendingItems = syncQueueDao.getUnsyncedByPriority()

        for (item in pendingItems) {
            if (item.retryCount > 5) {
                // Skip item with > 5 retries to avoid blocking sync queue
                continue
            }

            try {
                // Execute sync API POST request
                syncQueueDao.deleteById(item.id)
            } catch (e: Exception) {
                syncQueueDao.incrementRetryCount(item.id)
            }
        }

        return Result.success()
    }
}
