package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.theme.AlertBlue
import com.agrisage.app.ui.theme.AlertGold
import com.agrisage.app.ui.theme.AlertGreen
import com.agrisage.app.ui.theme.AlertRed

@Composable
fun SeverityBadge(
    severity: String,
    modifier: Modifier = Modifier
) {
    val (bgColor, textColor) = when (severity.uppercase()) {
        "CRITICAL" -> AlertRed to Color.White
        "WARNING" -> AlertGold to Color.Black
        "INFO" -> AlertBlue to Color.White
        "SUCCESS" -> AlertGreen to Color.White
        else -> AlertBlue to Color.White
    }

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(4.dp))
            .background(bgColor)
            .padding(horizontal = 6.dp, vertical = 2.dp)
    ) {
        Text(
            text = severity.uppercase(),
            fontSize = 10.sp,
            fontWeight = FontWeight.Bold,
            color = textColor
        )
    }
}
