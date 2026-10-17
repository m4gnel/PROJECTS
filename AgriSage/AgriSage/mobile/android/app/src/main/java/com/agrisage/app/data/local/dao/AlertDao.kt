package com.agrisage.app.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.agrisage.app.data.local.entity.AlertEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface AlertDao {
    @Query("SELECT * FROM alerts ORDER BY createdAt DESC")
    fun getAllAlerts(): Flow<List<AlertEntity>>

    @Query("SELECT * FROM alerts WHERE isRead = 0 ORDER BY createdAt DESC")
    fun getUnreadAlerts(): Flow<List<AlertEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAlerts(alerts: List<AlertEntity>)

    @Query("UPDATE alerts SET isRead = 1 WHERE id = :alertId")
    suspend fun markAsRead(alertId: String)

    @Query("UPDATE alerts SET isRead = 1")
    suspend fun markAllAsRead()

    @Query("DELETE FROM alerts WHERE id = :alertId")
    suspend fun deleteAlert(alertId: String)
}
