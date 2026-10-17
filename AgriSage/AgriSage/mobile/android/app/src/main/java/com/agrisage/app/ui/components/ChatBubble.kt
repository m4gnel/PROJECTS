package com.agrisage.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireLeafPale
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary

@Composable
fun ChatBubble(
    message: String,
    isUser: Boolean,
    modifier: Modifier = Modifier,
    timestamp: String? = null
) {
    val alignment = if (isUser) Alignment.End else Alignment.Start

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalAlignment = alignment
    ) {
        Row(
            verticalAlignment = Alignment.Top,
            modifier = Modifier.padding(horizontal = 4.dp)
        ) {
            if (!isUser) {
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(WireLeafPale),
                    contentAlignment = Alignment.Center
                ) {
                    Text("🤖", fontSize = 16.sp)
                }
                Spacer(modifier = Modifier.width(8.dp))
            }

            Card(
                shape = if (isUser) {
                    RoundedCornerShape(topStart = 14.dp, topEnd = 14.dp, bottomStart = 14.dp, bottomEnd = 2.dp)
                } else {
                    RoundedCornerShape(topStart = 14.dp, topEnd = 14.dp, bottomStart = 2.dp, bottomEnd = 14.dp)
                },
                colors = CardDefaults.cardColors(
                    containerColor = if (isUser) WireSage else Color.White
                ),
                border = if (isUser) null else BorderStroke(1.5.dp, WireBorder),
                elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
                modifier = Modifier.widthIn(max = 280.dp)
            ) {
                Text(
                    text = message,
                    color = if (isUser) Color.White else WireTextPrimary,
                    fontSize = 14.sp,
                    lineHeight = 20.sp,
                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp)
                )
            }

            if (isUser) {
                Spacer(modifier = Modifier.width(8.dp))
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(WireLeafPale),
                    contentAlignment = Alignment.Center
                ) {
                    Text("👨‍🌾", fontSize = 16.sp)
                }
            }
        }

        if (timestamp != null) {
            Text(
                text = timestamp,
                fontSize = 10.sp,
                color = WireTextMuted,
                modifier = Modifier.padding(top = 2.dp, start = if (!isUser) 42.dp else 0.dp, end = if (isUser) 42.dp else 0.dp)
            )
        }
    }
}
