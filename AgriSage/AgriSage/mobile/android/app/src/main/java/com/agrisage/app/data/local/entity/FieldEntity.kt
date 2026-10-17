package com.agrisage.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "fields")
data class FieldEntity(
    @PrimaryKey val id: String,
    val farmerId: String,
    val name: String,
    val areaSqM: Float,
    val cropName: String,
    val cropVariety: String,
    val sowingDate: String,
    val latitude: Double,
    val longitude: Double,
    val lastNdvi: Float = 0f,
    val updatedAt: Long
)
