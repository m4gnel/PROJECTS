package com.agrisage.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 2x2 Bento Quick Stat Card replicated from Reference Reel 2 (DailyFlutterUI Farm App).
 * Features:
 * - Rounded 20dp card container with subtle ambient shadow & border
 * - Colored pastel icon pill on top-left
 * - Circular interactive chevron navigation button on top-right
 * - Large display typography for metric values (e.g., "12", "48", "72%", "1,280 kg")
 * - Subtitle label in clean neutral slate
 */
@Composable
fun QuickStatCard(
    emojiOrIcon: String,
    value: String,
    label: String,
    badgeBgColor: Color,
    badgeTextColor: Color = Color.Unspecified,
    iconVector: ImageVector? = null,
    modifier: Modifier = Modifier,
    onClick: () -> Unit = {}
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(20.dp))
            .tactilePress(scaleDown = 0.95f, onClick = onClick),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Color(0xFFF1F5F9), RoundedCornerShape(20.dp))
                .padding(16.dp)
        ) {
            // Top Row: Pastel Icon Badge + Circular Chevron Action
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(42.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(badgeBgColor),
                    contentAlignment = Alignment.Center
                ) {
                    if (iconVector != null) {
                        Icon(
                            imageVector = iconVector,
                            contentDescription = label,
                            tint = badgeTextColor,
                            modifier = Modifier.size(20.dp)
                        )
                    } else {
                        Text(
                            text = emojiOrIcon,
                            fontSize = 20.sp
                        )
                    }
                }

                Box(
                    modifier = Modifier
                        .size(28.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFF8FAFC))
                        .border(1.dp, Color(0xFFE2E8F0), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                        contentDescription = "Details",
                        tint = Color(0xFF64748B),
                        modifier = Modifier.size(16.dp)
                    )
                }
            }

            Spacer(Modifier.height(14.dp))

            // Main Display Metric Value
            Text(
                text = value,
                fontSize = 22.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF0F172A),
                letterSpacing = (-0.5).sp
            )

            Spacer(Modifier.height(2.dp))

            // Label
            Text(
                text = label,
                fontSize = 13.sp,
                color = Color(0xFF64748B),
                fontWeight = FontWeight.Medium
            )
        }
    }
}
