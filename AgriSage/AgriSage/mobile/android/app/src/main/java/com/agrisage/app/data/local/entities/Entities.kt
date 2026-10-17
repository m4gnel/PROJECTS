package com.agrisage.app.data.local.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "farmers")
data class FarmerEntity(
    @PrimaryKey val id: String,
    val phone: String,
    val name: String?,
    val language: String = "ml",
    val subscriptionTier: String = "free",
    val subscriptionExpires: Long? = null,
    val updatedAt: Long
)

@Entity(tableName = "farms")
data class FarmEntity(
    @PrimaryKey val id: String,
    val userId: String,
    val name: String,
    val locationLat: Double?,
    val locationLon: Double?,
    val district: String?,
    val state: String?,
    val areaHa: Double?,
    val isSynced: Boolean = false,
    val createdAt: Long
)

@Entity(tableName = "fields")
data class FieldEntity(
    @PrimaryKey val id: String,
    val farmId: String,
    val name: String,
    val areaHa: Double?,
    val soilType: String?,
    val irrigationType: String?,
    val isSynced: Boolean = false
)

@Entity(tableName = "crop_cycles")
data class CropCycleEntity(
    @PrimaryKey val id: String,
    val fieldId: String,
    val crop: String,
    val variety: String?,
    val sowingDate: String,
    val expectedHarvestDate: String?,
    val status: String = "active",
    val isSynced: Boolean = false
)

@Entity(tableName = "observations")
data class ObservationEntity(
    @PrimaryKey val id: String,
    val cropCycleId: String,
    val observationDate: String,
    val notes: String?,
    val status: String = "pending",
    val isSynced: Boolean = false
)

@Entity(tableName = "images")
data class ImageEntity(
    @PrimaryKey val id: String,
    val observationId: String,
    val imagePath: String,
    val qualityScore: Double?,
    val isSynced: Boolean = false
)

@Entity(tableName = "cached_advisories")
data class CachedAdvisoryEntity(
    @PrimaryKey val id: String,
    val observationId: String,
    val advisoryJson: String,
    val type: String = "advisory",
    val isOffline: Boolean = false,
    val createdAt: Long
)

@Entity(tableName = "weather_cache")
data class WeatherCacheEntity(
    @PrimaryKey val locationKey: String,
    val dataJson: String,
    val cachedAt: Long
)

@Entity(tableName = "sync_queue")
data class SyncQueueEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val entityType: String,
    val entityId: String,
    val action: String,
    val payloadJson: String,
    val priority: Int = 5,
    val retryCount: Int = 0,
    val createdAt: Long
)
