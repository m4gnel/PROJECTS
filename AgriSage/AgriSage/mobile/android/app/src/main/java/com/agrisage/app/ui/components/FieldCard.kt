package com.agrisage.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
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
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireGoldPale
import com.agrisage.app.ui.theme.WireLeafPale
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSoilLight
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary

@Composable
fun FieldCard(
    name: String,
    areaSqM: Float,
    cropName: String,
    lastNdvi: Float? = null,
    soilType: String = "Laterite",
    soilPh: Float = 6.2f,
    status: String = "Active",
    onClick: () -> Unit = {}
) {
    val cropIcon = when {
        cropName.contains("Rice", ignoreCase = true) || cropName.contains("Paddy", ignoreCase = true) -> "🌾"
        cropName.contains("Coconut", ignoreCase = true) -> "🌴"
        cropName.contains("Veg", ignoreCase = true) -> "🥦"
        else -> "🌱"
    }

    val acres = areaSqM / 4046.86f

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable { onClick() },
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        border = BorderStroke(1.5.dp, WireBorder),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(42.dp)
                    .clip(RoundedCornerShape(10.dp))
                    .background(WireLeafPale),
                contentAlignment = Alignment.Center
            ) {
                Text(text = cropIcon, fontSize = 22.sp)
            }

            Spacer(modifier = Modifier.width(12.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = name,
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = WireSageDeep
                )
                Text(
                    text = "%.1f acres · %s".format(acres.coerceAtLeast(0.5f), cropName),
                    fontSize = 12.sp,
                    color = WireTextMuted,
                    modifier = Modifier.padding(top = 2.dp)
                )
                Text(
                    text = "Soil: $soilType · pH %.1f".format(soilPh),
                    fontSize = 11.sp,
                    color = WireTextMuted
                )
            }

            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(6.dp))
                    .background(if (status == "Harvesting") WireGoldPale else WireLeafPale)
                    .padding(horizontal = 8.dp, vertical = 3.dp)
            ) {
                Text(
                    text = status,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (status == "Harvesting") WireSoilLight else WireSage
                )
            }
        }
    }
}
