package com.agrisage.app.ui.screens.fields

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Agriculture
import androidx.compose.material.icons.filled.CloudOff
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.BuildConfig
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.components.tactilePress
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSurface
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireTextSecondary
import com.agrisage.app.ui.theme.WireWhite
import java.util.Locale

@Composable
fun FieldDetailScreen(
    navController: NavHostController,
    fieldId: String,
    viewModel: FieldDetailViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    LaunchedEffect(fieldId) { viewModel.load(fieldId) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(WireWhite),
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = "Back",
                    tint = WireTextPrimary,
                    modifier = Modifier
                        .tactilePress(scaleDown = 0.94f, onClickLabel = "Go back", onClick = { navController.popBackStack() })
                        .padding(12.dp),
                )
                Text("Plot Details", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = WireSageDeep)
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .verticalScroll(rememberScrollState())
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                state.field?.let { field ->
                    DetailCard {
                        Text(field.name, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = WireSageDeep)
                        Text("Plot ID: ${field.id}", fontSize = 12.sp, color = WireTextMuted, modifier = Modifier.padding(top = 4.dp))
                        Spacer(Modifier.height(10.dp))
                        Text("Area: ${areaLabel(field.areaSqM)}", fontSize = 14.sp, color = WireTextPrimary)
                        Text("Crop: ${field.cropName.takeIf(String::isNotBlank) ?: "Unavailable"}", fontSize = 14.sp, color = WireTextPrimary)
                        Text("Variety: ${field.cropVariety.takeIf(String::isNotBlank) ?: "Unavailable"}", fontSize = 14.sp, color = WireTextPrimary)
                        Text("Sowing date: ${field.sowingDate.takeIf(String::isNotBlank) ?: "Unavailable"}", fontSize = 14.sp, color = WireTextPrimary)
                    }

                    DetailCard {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Agriculture, contentDescription = null, tint = WireSage, modifier = Modifier.size(22.dp))
                            Spacer(Modifier.padding(horizontal = 4.dp))
                            Text("Satellite NDVI", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = WireTextPrimary)
                            Spacer(Modifier.weight(1f))
                            Text(field.lastNdvi?.let { "%.2f".format(Locale.US, it) } ?: "Unavailable", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = WireSage)
                        }
                        Text(
                            text = when {
                                BuildConfig.REFERENCE_PREVIEW -> "Sample NDVI for visual reference only."
                                field.lastNdvi != null -> "Cached provider NDVI; freshness has not been verified."
                                else -> "No provider-backed NDVI value is available for this plot."
                            },
                            fontSize = 12.sp,
                            color = WireTextSecondary,
                            modifier = Modifier.padding(top = 6.dp),
                        )
                    }

                    DetailCard {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.WaterDrop, contentDescription = null, tint = WireSage, modifier = Modifier.size(22.dp))
                            Spacer(Modifier.padding(horizontal = 4.dp))
                            Text("Irrigation", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = WireTextPrimary)
                        }
                        Text(
                            "Irrigation scheduling is unavailable until a current provider reading is returned for this plot.",
                            fontSize = 13.sp,
                            color = WireTextSecondary,
                            modifier = Modifier.padding(top = 6.dp),
                        )
                    }
                } ?: DetailCard {
                    Icon(Icons.Default.CloudOff, contentDescription = null, tint = WireTextMuted, modifier = Modifier.size(28.dp))
                    Text("Plot details unavailable", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = WireTextPrimary, modifier = Modifier.padding(top = 8.dp))
                    Text("The selected plot is not available in the local cache or provider response.", fontSize = 13.sp, color = WireTextSecondary, modifier = Modifier.padding(top = 4.dp))
                }
                state.error?.let { error ->
                    Text(error, fontSize = 12.sp, color = WireTextSecondary)
                }
                Spacer(Modifier.height(18.dp))
            }
        }
        LoadingOverlay(isLoading = state.isLoading)
    }
}

@Composable
private fun DetailCard(content: @Composable () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = WireSurface),
        border = androidx.compose.foundation.BorderStroke(1.dp, WireBorder.copy(alpha = 0.65f)),
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            content()
        }
    }
}

private fun areaLabel(areaSqM: Float): String {
    if (areaSqM <= 0f) return "Unavailable"
    val acres = areaSqM / 4046.8564f
    return "%.1f acres (%.0f m²)".format(Locale.US, acres, areaSqM)
}
