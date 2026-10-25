package com.agrisage.app.domain.usecases

import com.agrisage.app.data.local.dao.ObservationDao
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.SyncUploadRequest
import com.agrisage.app.data.repository.AuthRepository
import javax.inject.Inject

class SyncDataUseCase @Inject constructor(
    private val observationDao: ObservationDao,
    private val apiService: ApiService,
    private val authRepository: AuthRepository,
) {
    suspend operator fun invoke(): Boolean {
        if (!authRepository.hasSession()) return false
        val pending = observationDao.getUnsyncedObservations()
        if (pending.isEmpty()) return true

        val response = runCatching {
            apiService.uploadSyncBatch(
                SyncUploadRequest(
                    observations = pending.map { observation ->
                        mapOf(
                            "id" to observation.id,
                            "crop_cycle_id" to observation.cropCycleId,
                            "observation_date" to observation.observationDate,
                            "notes" to observation.notes,
                            "status" to observation.status,
                        )
                    },
                    deviceId = "android",
                )
            )
        }.getOrNull()

        if (response?.isSuccessful == true) {
            observationDao.markAsSynced(pending.map { it.id })
            return true
        }
        return false
    }
}
