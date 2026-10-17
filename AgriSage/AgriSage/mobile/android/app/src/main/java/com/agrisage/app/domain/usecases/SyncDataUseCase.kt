package com.agrisage.app.domain.usecases

import com.agrisage.app.data.local.dao.ObservationDao
import javax.inject.Inject

class SyncDataUseCase @Inject constructor(
    private val observationDao: ObservationDao
) {
    suspend operator fun invoke(): Boolean {
        val pending = observationDao.getUnsyncedObservations()
        if (pending.isNotEmpty()) {
            // Simulated upload batch sync
            observationDao.markAsSynced(pending.map { it.id })
        }
        return true
    }
}
