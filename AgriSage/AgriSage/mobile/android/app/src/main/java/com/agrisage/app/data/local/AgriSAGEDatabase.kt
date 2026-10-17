package com.agrisage.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.agrisage.app.data.local.dao.*
import com.agrisage.app.data.local.entities.*

@Database(
    entities = [
        FarmerEntity::class,
        FarmEntity::class,
        FieldEntity::class,
        CropCycleEntity::class,
        ObservationEntity::class,
        ImageEntity::class,
        CachedAdvisoryEntity::class,
        WeatherCacheEntity::class,
        SyncQueueEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AgriSAGEDatabase : RoomDatabase() {
    abstract fun farmerDao(): FarmerDao
    abstract fun farmDao(): FarmDao
    abstract fun cachedAdvisoryDao(): CachedAdvisoryDao
    abstract fun syncQueueDao(): SyncQueueDao
    abstract fun observationDao(): ObservationDao
}
