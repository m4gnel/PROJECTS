package com.agrisage.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "alerts")
data class AlertEntity(
    @PrimaryKey val id: String,
    val severity: String,
    val title: String,
    val message: String,
    val isRead: Boolean = false,
    val createdAt: Long
)
