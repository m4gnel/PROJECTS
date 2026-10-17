package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.theme.OnSurface
import com.agrisage.app.ui.theme.SurfaceDim

@Composable
fun WeatherChip(
    temperatureC: Float,
    condition: String,
    onClick: () -> Unit = {}
) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(16.dp))
            .background(SurfaceDim)
            .clickable { onClick() }
            .padding(horizontal = 12.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = "🌤️ ${temperatureC.toInt()}°C",
            fontSize = 14.sp,
            fontWeight = FontWeight.Bold,
            color = OnSurface
        )
        Spacer(modifier = Modifier.width(6.dp))
        Text(
            text = condition,
            fontSize = 12.sp,
            color = OnSurface.copy(alpha = 0.7f)
        )
    }
}
