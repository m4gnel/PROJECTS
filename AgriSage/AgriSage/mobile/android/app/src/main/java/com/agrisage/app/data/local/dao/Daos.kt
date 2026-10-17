package com.agrisage.app.data.local.dao

import androidx.room.*
import com.agrisage.app.data.local.entities.*
import kotlinx.coroutines.flow.Flow

@Dao
interface FarmerDao {
    @Query("SELECT * FROM farmers LIMIT 1")
    fun getFarmer(): Flow<FarmerEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertFarmer(farmer: FarmerEntity)
}

@Dao
interface FarmDao {
    @Query("SELECT * FROM farms WHERE userId = :userId")
    fun getFarmsByUserId(userId: String): Flow<List<FarmEntity>>

    @Query("SELECT * FROM farms WHERE id = :id")
    suspend fun getFarmById(id: String): FarmEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertFarm(farm: FarmEntity)

    @Query("UPDATE farms SET isSynced = :isSynced WHERE id = :id")
    suspend fun updateSyncStatus(id: String, isSynced: Boolean)
}

@Dao
interface CachedAdvisoryDao {
    @Query("SELECT * FROM cached_advisories WHERE observationId = :obsId LIMIT 1")
    suspend fun getByObservationId(obsId: String): CachedAdvisoryEntity?

    @Query("SELECT * FROM cached_advisories WHERE type = 'morning_briefing' ORDER BY createdAt DESC LIMIT 1")
    fun getMorningBriefing(): Flow<CachedAdvisoryEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAdvisory(advisory: CachedAdvisoryEntity)

    @Query("DELETE FROM cached_advisories WHERE createdAt < :timestamp")
    suspend fun deleteOlderThan(timestamp: Long)
}

@Dao
interface SyncQueueDao {
    @Query("SELECT * FROM sync_queue WHERE retryCount <= 5 ORDER BY priority ASC, id ASC")
    suspend fun getUnsyncedByPriority(): List<SyncQueueEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: SyncQueueEntity)

    @Query("UPDATE sync_queue SET retryCount = retryCount + 1 WHERE id = :id")
    suspend fun incrementRetryCount(id: Int)

    @Query("DELETE FROM sync_queue WHERE id = :id")
    suspend fun deleteById(id: Int)
}

@Dao
interface ObservationDao {
    @Query("SELECT * FROM observations WHERE isSynced = 0")
    suspend fun getUnsyncedObservations(): List<ObservationEntity>

    @Query("UPDATE observations SET isSynced = 1 WHERE id IN (:ids)")
    suspend fun markAsSynced(ids: List<String>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertObservation(observation: ObservationEntity)
}

