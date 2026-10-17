package com.agrisage.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.agrisage.app.data.local.dao.AlertDao
import com.agrisage.app.data.local.dao.ChatDao
import com.agrisage.app.data.local.dao.FieldDao
import com.agrisage.app.data.local.dao.WeatherDao
import com.agrisage.app.data.local.entity.AlertEntity
import com.agrisage.app.data.local.entity.ChatMessageEntity
import com.agrisage.app.data.local.entity.FieldEntity
import com.agrisage.app.data.local.entity.WeatherEntity

@Database(
    entities = [
        WeatherEntity::class,
        AlertEntity::class,
        ChatMessageEntity::class,
        FieldEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun weatherDao(): WeatherDao
    abstract fun alertDao(): AlertDao
    abstract fun chatDao(): ChatDao
    abstract fun fieldDao(): FieldDao
}
