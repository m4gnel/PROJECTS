package com.agrisage.app.domain.model

enum class AlertSeverity { CRITICAL, WARNING, INFO, SUCCESS }

data class Alert(
    val id: String,
    val farmerId: String,
    val fieldId: String? = null,
    val severity: AlertSeverity,
    val title: String,
    val message: String,
    val sourceAgent: String? = null,
    val isRead: Boolean = false,
    val createdAt: String
)
