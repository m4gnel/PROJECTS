package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.theme.DarkText

enum class AlertSeverity {
    CRITICAL,
    WARNING,
    INFO,
    SUCCESS
}

/**
 * Reusable AlertBanner component displaying real-time weather, pest, market,
 * or field warnings with proper severity color-coding and icons per spec.
 */
@Composable
fun AlertBanner(
    title: String,
    message: String,
    severity: AlertSeverity = AlertSeverity.WARNING,
    modifier: Modifier = Modifier,
    onDismiss: (() -> Unit)? = null
) {
    val (bgColor, borderColor, icon, iconColor) = when (severity) {
        AlertSeverity.CRITICAL -> Quadruple(
            Color(0xFFFFEBEE), Color(0xFFEF5350), Icons.Default.Error, Color(0xFFC62828)
        )
        AlertSeverity.WARNING -> Quadruple(
            Color(0xFFFFF8E1), Color(0xFFFFB74D), Icons.Default.Warning, Color(0xFFE65100)
        )
        AlertSeverity.INFO -> Quadruple(
            Color(0xFFE3F2FD), Color(0xFF64B5F6), Icons.Default.Info, Color(0xFF1565C0)
        )
        AlertSeverity.SUCCESS -> Quadruple(
            Color(0xFFE8F5E9), Color(0xFF81C784), Icons.Default.CheckCircle, Color(0xFF2E7D32)
        )
    }

    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        color = bgColor,
        border = androidx.compose.foundation.BorderStroke(1.dp, borderColor)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            verticalAlignment = Alignment.Top
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = iconColor,
                modifier = Modifier.size(24.dp)
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp,
                    color = iconColor
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = message,
                    fontSize = 13.sp,
                    color = DarkText.copy(alpha = 0.85f),
                    lineHeight = 18.sp
                )
            }
            if (onDismiss != null) {
                IconButton(
                    onClick = onDismiss,
                    modifier = Modifier.size(24.dp)
                ) {
                    Icon(
                        Icons.Default.Close,
                        contentDescription = "Dismiss",
                        tint = Color.Gray,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        }
    }
}

private data class Quadruple<A, B, C, D>(val first: A, val second: B, val third: C, val fourth: D)
