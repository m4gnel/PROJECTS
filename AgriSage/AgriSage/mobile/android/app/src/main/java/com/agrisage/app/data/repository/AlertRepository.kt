package com.agrisage.app.data.repository

import com.agrisage.app.data.local.dao.AlertDao
import com.agrisage.app.data.local.entity.AlertEntity
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.AlertDto
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AlertRepository @Inject constructor(
    private val apiService: ApiService,
    private val alertDao: AlertDao
) {
    fun getLocalAlerts(): Flow<List<AlertEntity>> = alertDao.getAllAlerts()
    fun getUnreadAlerts(): Flow<List<AlertEntity>> = alertDao.getUnreadAlerts()

    suspend fun refreshAlerts(): Response<List<AlertDto>> {
        val response = apiService.getAlerts()
        if (response.isSuccessful && response.body() != null) {
            val entities = response.body()!!.map { dto ->
                AlertEntity(
                    id = dto.id,
                    severity = dto.severity,
                    title = dto.title,
                    message = dto.message,
                    isRead = dto.isRead,
                    createdAt = System.currentTimeMillis()
                )
            }
            alertDao.deleteAll()
            alertDao.insertAlerts(entities)
        }
        return response
    }

    suspend fun markAsRead(alertId: String) {
        alertDao.markAsRead(alertId)
    }

    suspend fun markAllAsRead() {
        alertDao.markAllAsRead()
    }

    suspend fun dismissAlert(alertId: String) {
        alertDao.deleteAlert(alertId)
    }
}
