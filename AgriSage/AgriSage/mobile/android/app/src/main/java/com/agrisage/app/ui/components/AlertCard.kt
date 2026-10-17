package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.theme.AlertGold
import com.agrisage.app.ui.theme.AlertRed
import com.agrisage.app.ui.theme.OnSurface
import com.agrisage.app.ui.theme.OnSurfaceVar
import com.agrisage.app.ui.theme.Surface

@Composable
fun AlertCard(
    title: String,
    message: String,
    severity: String,
    isRead: Boolean = false,
    onClick: () -> Unit = {}
) {
    val borderColor = when (severity.uppercase()) {
        "CRITICAL" -> AlertRed
        "WARNING" -> AlertGold
        else -> Color.Transparent
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable { onClick() },
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                SeverityBadge(severity = severity)
                Spacer(modifier = Modifier.weight(1f))
                if (!isRead) {
                    Text(text = "●", color = AlertRed, fontSize = 12.sp)
                }
            }

            Spacer(modifier = Modifier.height(6.dp))

            Text(
                text = title,
                fontSize = 15.sp,
                fontWeight = FontWeight.Bold,
                color = OnSurface
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = message,
                fontSize = 13.sp,
                color = OnSurfaceVar,
                lineHeight = 18.sp
            )
        }
    }
}
