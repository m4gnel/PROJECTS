package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Hero KPI Cards overlaid at the bottom of the illustrated farm scene (Reference Reel 2).
 * Left Card: Farm Health with circular progress gauge
 * Right Card: Weather summary with temperature & humidity
 */
@Composable
fun HeroKpiCardsRow(
    healthScore: Int = 92,
    healthStatus: String = "Healthy",
    tempCelsius: Int = 28,
    weatherCondition: String = "Sunny",
    rainChance: Int = 15,
    humidity: Int = 68,
    modifier: Modifier = Modifier,
    onHealthClick: () -> Unit = {},
    onWeatherClick: () -> Unit = {}
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Farm Health Card
        Card(
            modifier = Modifier
                .weight(1f)
                .clip(RoundedCornerShape(20.dp))
                .tactilePress(scaleDown = 0.95f, onClick = onHealthClick),
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                    .padding(14.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Circular Ring Gauge
                Box(
                    modifier = Modifier.size(52.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(
                        progress = { healthScore / 100f },
                        modifier = Modifier.fillMaxSize(),
                        color = Color(0xFF16A34A),
                        trackColor = Color(0xFFDCFCE7),
                        strokeWidth = 4.5.dp,
                        strokeCap = StrokeCap.Round
                    )
                    Text(
                        text = "$healthScore%",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF0F172A)
                    )
                }

                Spacer(Modifier.width(10.dp))

                Column {
                    Text(
                        text = "Farm Health",
                        fontSize = 11.sp,
                        color = Color(0xFF64748B),
                        fontWeight = FontWeight.Medium
                    )
                    Text(
                        text = healthStatus,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF0F172A)
                    )
                    Spacer(Modifier.height(2.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF16A34A))
                        )
                        Spacer(Modifier.width(4.dp))
                        Text(
                            text = "All good",
                            fontSize = 10.sp,
                            color = Color(0xFF16A34A),
                            fontWeight = FontWeight.SemiBold
                        )
                    }
                }
            }
        }

        // Weather Snapshot Card
        Card(
            modifier = Modifier
                .weight(1f)
                .clip(RoundedCornerShape(20.dp))
                .tactilePress(scaleDown = 0.95f, onClick = onWeatherClick),
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                    .padding(14.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Weather Sun Icon in light yellow badge
                Box(
                    modifier = Modifier
                        .size(46.dp)
                        .clip(RoundedCornerShape(14.dp))
                        .background(Color(0xFFFEF3C7)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("☀️", fontSize = 24.sp)
                }

                Spacer(Modifier.width(10.dp))

                Column {
                    Text(
                        text = "$tempCelsius°C",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF0F172A)
                    )
                    Text(
                        text = weatherCondition,
                        fontSize = 12.sp,
                        color = Color(0xFF64748B),
                        fontWeight = FontWeight.Medium
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        text = "💨 $rainChance% · 💧 $humidity%",
                        fontSize = 10.sp,
                        color = Color(0xFF94A3B8),
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }
    }
}
