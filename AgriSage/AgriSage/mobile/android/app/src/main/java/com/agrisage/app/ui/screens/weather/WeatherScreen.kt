package com.agrisage.app.ui.screens.weather

import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSky
import com.agrisage.app.ui.theme.WireSkyPale
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireTextSecondary
import com.agrisage.app.ui.theme.WireWhite

@Composable
fun WeatherScreen(
    navController: NavHostController,
    viewModel: WeatherViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Box(modifier = Modifier.fillMaxSize().background(WireWhite)) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
        ) {
            // Sky Gradient Top Hero
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        brush = Brush.linearGradient(
                            colors = listOf(Color(0xFF1E96D0), Color(0xFF0E4F7A))
                        )
                    )
                    .padding(horizontal = 20.dp, vertical = 24.dp)
            ) {
                Text(
                    text = "📍 Kalady, Kerala",
                    fontSize = 13.sp,
                    color = Color.White.copy(alpha = 0.8f)
                )

                Spacer(modifier = Modifier.height(6.dp))

                Row(verticalAlignment = Alignment.Bottom) {
                    Text(
                        text = "%.0f°".format(state.currentTemp),
                        fontSize = 54.sp,
                        fontWeight = FontWeight.Black,
                        color = Color.White,
                        lineHeight = 54.sp
                    )
                    Text(
                        text = "C",
                        fontSize = 28.sp,
                        fontWeight = FontWeight.Normal,
                        color = Color.White.copy(alpha = 0.9f),
                        modifier = Modifier.padding(bottom = 6.dp)
                    )
                }

                Text(
                    text = if (state.currentCondition.isNotBlank()) state.currentCondition else "Partly Cloudy — Good for field work",
                    fontSize = 14.sp,
                    color = Color.White.copy(alpha = 0.9f),
                    modifier = Modifier.padding(top = 2.dp)
                )

                Spacer(modifier = Modifier.height(20.dp))

                // 4-Stat Row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    WeatherStatBox(valText = "${state.humidity}%", labelText = "Humidity")
                    WeatherStatBox(valText = "%.0f km/h".format(state.windKmh), labelText = "Wind")
                    WeatherStatBox(valText = "4mm", labelText = "Rain today")
                    WeatherStatBox(valText = "UV %.0f".format(state.uvIndex), labelText = "UV Index")
                }
            }

            // Body
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "7-DAY FORECAST",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = WireTextMuted,
                    letterSpacing = 1.sp,
                    modifier = Modifier.padding(bottom = 10.dp)
                )

                // 7-Day Forecast Row
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    if (state.forecast7Day.isNotEmpty()) {
                        items(state.forecast7Day) { day ->
                            val isToday = day == state.forecast7Day.firstOrNull()
                            Card(
                                modifier = Modifier.width(62.dp),
                                shape = RoundedCornerShape(10.dp),
                                colors = CardDefaults.cardColors(containerColor = Color.White),
                                border = BorderStroke(1.5.dp, if (isToday) WireSky else WireBorder),
                                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 10.dp, horizontal = 4.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = if (isToday) "Today" else day.date.take(3),
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = WireTextMuted
                                    )
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(text = if (day.rainfallMm > 0) "🌧️" else "⛅", fontSize = 20.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = "${day.maxTempC.toInt()}°",
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = WireSageDeep
                                    )
                                }
                            }
                        }
                    } else {
                        val mockDays = listOf(
                            Triple("Today", "⛅", "28°"),
                            Triple("Fri", "🌧️", "25°"),
                            Triple("Sat", "⛈️", "24°"),
                            Triple("Sun", "🌤️", "29°"),
                            Triple("Mon", "☀️", "31°")
                        )
                        items(mockDays) { (d, icon, temp) ->
                            val isToday = d == "Today"
                            Card(
                                modifier = Modifier.width(62.dp),
                                shape = RoundedCornerShape(10.dp),
                                colors = CardDefaults.cardColors(containerColor = Color.White),
                                border = BorderStroke(1.5.dp, if (isToday) WireSky else WireBorder),
                                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 10.dp, horizontal = 4.dp),
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Text(
                                        text = d,
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = WireTextMuted
                                    )
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(text = icon, fontSize = 20.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = temp,
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = WireSageDeep
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(18.dp))

                // Agri-SAGE Advisory Box
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = WireSkyPale),
                    border = BorderStroke(1.5.dp, WireSky)
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Text(
                            text = "🤖 Agri-SAGE Advisory",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            color = WireSky
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = if (state.agriAdvisory.isNotBlank()) state.agriAdvisory else "Rain expected Fri–Sat. Delay chemical spraying to Sunday. Ideal fertiliser window: today before 9 AM.",
                            fontSize = 12.sp,
                            color = WireTextSecondary,
                            lineHeight = 18.sp
                        )
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))
            }
        }

        LoadingOverlay(isLoading = state.isLoading)
    }
}

@Composable
private fun WeatherStatBox(valText: String, labelText: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = valText,
            fontSize = 15.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        Text(
            text = labelText,
            fontSize = 10.sp,
            color = Color.White.copy(alpha = 0.7f),
            modifier = Modifier.padding(top = 1.dp)
        )
    }
}
