package com.agrisage.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.agrisage.app.data.local.dao.AlertDao
import com.agrisage.app.data.local.dao.ChatDao
import com.agrisage.app.data.local.dao.CachedAdvisoryDao
import com.agrisage.app.data.local.dao.FieldDao
import com.agrisage.app.data.local.dao.FarmDao
import com.agrisage.app.data.local.dao.FarmerDao
import com.agrisage.app.data.local.dao.ObservationDao
import com.agrisage.app.data.local.dao.SyncQueueDao
import com.agrisage.app.data.local.dao.WeatherDao
import com.agrisage.app.data.local.entities.CachedAdvisoryEntity
import com.agrisage.app.data.local.entities.CropCycleEntity
import com.agrisage.app.data.local.entities.FarmEntity
import com.agrisage.app.data.local.entities.FarmerEntity
import com.agrisage.app.data.local.entities.ImageEntity
import com.agrisage.app.data.local.entities.ObservationEntity
import com.agrisage.app.data.local.entities.SyncQueueEntity
import com.agrisage.app.data.local.entity.AlertEntity
import com.agrisage.app.data.local.entity.ChatMessageEntity
import com.agrisage.app.data.local.entity.FieldEntity
import com.agrisage.app.data.local.entity.WeatherEntity

@Database(
    entities = [
        WeatherEntity::class,
        AlertEntity::class,
        ChatMessageEntity::class,
        FieldEntity::class,
        FarmerEntity::class,
        FarmEntity::class,
        CropCycleEntity::class,
        ObservationEntity::class,
        ImageEntity::class,
        CachedAdvisoryEntity::class,
        SyncQueueEntity::class,
    ],
    version = 2,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun weatherDao(): WeatherDao
    abstract fun alertDao(): AlertDao
    abstract fun chatDao(): ChatDao
    abstract fun fieldDao(): FieldDao
    abstract fun farmerDao(): FarmerDao
    abstract fun farmDao(): FarmDao
    abstract fun cachedAdvisoryDao(): CachedAdvisoryDao
    abstract fun syncQueueDao(): SyncQueueDao
    abstract fun observationDao(): ObservationDao
}
