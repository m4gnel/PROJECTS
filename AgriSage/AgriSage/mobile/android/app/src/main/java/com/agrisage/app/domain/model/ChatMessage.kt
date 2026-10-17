package com.agrisage.app.domain.model

data class ChatMessage(
    val id: String,
    val content: String,
    val isFromUser: Boolean,
    val timestamp: Long,
    val language: String,
    val confidenceScore: Float? = null
)
