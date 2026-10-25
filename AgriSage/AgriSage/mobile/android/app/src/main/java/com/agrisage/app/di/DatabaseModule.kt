package com.agrisage.app.di

import android.content.Context
import androidx.room.migration.Migration
import androidx.room.Room
import androidx.sqlite.db.SupportSQLiteDatabase
import com.agrisage.app.data.local.AppDatabase
import com.agrisage.app.data.local.dao.*
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    private val migration1To2 = object : Migration(1, 2) {
        override fun migrate(db: SupportSQLiteDatabase) {
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS farmers (
                    id TEXT NOT NULL PRIMARY KEY,
                    phone TEXT NOT NULL,
                    name TEXT,
                    language TEXT NOT NULL,
                    subscriptionTier TEXT NOT NULL,
                    subscriptionExpires INTEGER,
                    updatedAt INTEGER NOT NULL
                )""".trimIndent()
            )
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS farms (
                    id TEXT NOT NULL PRIMARY KEY,
                    userId TEXT NOT NULL,
                    name TEXT NOT NULL,
                    locationLat REAL,
                    locationLon REAL,
                    district TEXT,
                    state TEXT,
                    areaHa REAL,
                    isSynced INTEGER NOT NULL,
                    createdAt INTEGER NOT NULL
                )""".trimIndent()
            )
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS crop_cycles (
                    id TEXT NOT NULL PRIMARY KEY,
                    fieldId TEXT NOT NULL,
                    crop TEXT NOT NULL,
                    variety TEXT,
                    sowingDate TEXT NOT NULL,
                    expectedHarvestDate TEXT,
                    status TEXT NOT NULL,
                    isSynced INTEGER NOT NULL
                )""".trimIndent()
            )
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS observations (
                    id TEXT NOT NULL PRIMARY KEY,
                    cropCycleId TEXT NOT NULL,
                    observationDate TEXT NOT NULL,
                    notes TEXT,
                    status TEXT NOT NULL,
                    isSynced INTEGER NOT NULL
                )""".trimIndent()
            )
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS images (
                    id TEXT NOT NULL PRIMARY KEY,
                    observationId TEXT NOT NULL,
                    imagePath TEXT NOT NULL,
                    qualityScore REAL,
                    isSynced INTEGER NOT NULL
                )""".trimIndent()
            )
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS cached_advisories (
                    id TEXT NOT NULL PRIMARY KEY,
                    observationId TEXT NOT NULL,
                    advisoryJson TEXT NOT NULL,
                    type TEXT NOT NULL,
                    isOffline INTEGER NOT NULL,
                    createdAt INTEGER NOT NULL
                )""".trimIndent()
            )
            db.execSQL(
                """CREATE TABLE IF NOT EXISTS sync_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    entityType TEXT NOT NULL,
                    entityId TEXT NOT NULL,
                    action TEXT NOT NULL,
                    payloadJson TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    retryCount INTEGER NOT NULL,
                    createdAt INTEGER NOT NULL
                )""".trimIndent()
            )
        }
    }

    @Provides
    @Singleton
    fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "agrisage_app_db"
        ).addMigrations(migration1To2).build()
    }

    @Provides
    fun provideWeatherDao(db: AppDatabase): WeatherDao = db.weatherDao()

    @Provides
    fun provideAlertDao(db: AppDatabase): AlertDao = db.alertDao()

    @Provides
    fun provideChatDao(db: AppDatabase): ChatDao = db.chatDao()

    @Provides
    fun provideFieldDao(db: AppDatabase): FieldDao = db.fieldDao()

    @Provides
    fun provideFarmerDao(db: AppDatabase): FarmerDao = db.farmerDao()

    @Provides
    fun provideFarmDao(db: AppDatabase): FarmDao = db.farmDao()

    @Provides
    fun provideCachedAdvisoryDao(db: AppDatabase): CachedAdvisoryDao = db.cachedAdvisoryDao()

    @Provides
    fun provideSyncQueueDao(db: AppDatabase): SyncQueueDao = db.syncQueueDao()

    @Provides
    fun provideObservationDao(db: AppDatabase): ObservationDao = db.observationDao()
}
