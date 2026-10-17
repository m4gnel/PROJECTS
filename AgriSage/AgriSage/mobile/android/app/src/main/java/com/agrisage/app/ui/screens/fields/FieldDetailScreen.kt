package com.agrisage.app.ui.screens.fields

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.agrisage.app.ui.theme.AlertGreen
import com.agrisage.app.ui.theme.OnSurface
import com.agrisage.app.ui.theme.OnSurfaceVar
import com.agrisage.app.ui.theme.SageGreen700
import com.agrisage.app.ui.theme.SageGreen900
import com.agrisage.app.ui.theme.Surface
import com.agrisage.app.ui.theme.SurfaceDim

@Composable
fun FieldDetailScreen(
    navController: NavHostController,
    fieldId: String
) {
    Box(modifier = Modifier.fillMaxSize().background(Surface)) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            // Top Bar
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { navController.popBackStack() }) {
                    Icon(imageVector = Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                }
                Text(
                    text = "Plot Details",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = SageGreen900
                )
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Field Info Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDim)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(text = "South Paddy Field", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = SageGreen700)
                    Text(text = "Plot ID: $fieldId", fontSize = 12.sp, color = OnSurfaceVar)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = "Area: 5,000 m² (0.5 Hectares)", fontSize = 14.sp, color = OnSurface)
                    Text(text = "Active Crop: Rice (Jyothi Variety)", fontSize = 14.sp, color = OnSurface)
                    Text(text = "Stage: Vegetative (Day 45)", fontSize = 14.sp, color = OnSurface)
                    Text(text = "Soil Type: Laterite (pH 5.8)", fontSize = 14.sp, color = OnSurface)
                }
            }

            Spacer(modifier = Modifier.height(14.dp))

            // NDVI Satellite Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDim)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(text = "🛰️ Satellite NDVI Health", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = OnSurface)
                        Spacer(modifier = Modifier.weight(1f))
                        Text(text = "0.65 (Healthy)", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = AlertGreen)
                    }
                    Text(
                        text = "NASA AppEEARS / Sentinel-2 data indicates dense green canopy and normal chlorophyll levels.",
                        fontSize = 12.sp,
                        color = OnSurfaceVar,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(14.dp))

            // Irrigation Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDim)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(text = "💧 Irrigation Schedule", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = OnSurface)
                    Text(
                        text = "Maintain 2-3 cm standing water. Expected rainfall (2.3mm) will suffice for today. Next flood irrigation recommended on Friday.",
                        fontSize = 13.sp,
                        color = OnSurfaceVar,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(14.dp))

            // Fertilizer Recommendation Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceDim)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(text = "🌿 Fertilizer Advisory (KAU)", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = OnSurface)
                    Text(
                        text = "Apply second top dressing of Urea (35 kg/ha) mixed with neem cake at panicle initiation stage.",
                        fontSize = 13.sp,
                        color = OnSurfaceVar,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }
        }
    }
}
