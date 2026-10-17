package com.agrisage.app.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "chat_messages")
data class ChatMessageEntity(
    @PrimaryKey val id: String,
    val sessionId: String,
    val content: String,
    val isFromUser: Boolean,
    val language: String,
    val timestamp: Long
)
