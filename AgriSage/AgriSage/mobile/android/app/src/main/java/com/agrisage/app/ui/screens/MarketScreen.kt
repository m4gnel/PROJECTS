package com.agrisage.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.TrendingDown
import androidx.compose.material.icons.filled.TrendingUp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.agrisage.app.navigation.Advisor
import com.agrisage.app.navigation.Home
import com.agrisage.app.navigation.Profile
import com.agrisage.app.navigation.Weather
import com.agrisage.app.ui.components.AgriBottomNav
import com.agrisage.app.ui.theme.SageDeep

data class MarketPriceItem(
    val id: String,
    val cropName: String,
    val variety: String,
    val mandi: String,
    val currentPrice: Int,
    val priceChange: Int,
    val isUp: Boolean,
    val recommendation: String, // "SELL NOW" or "HOLD"
    val recommendationDetail: String,
    val category: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MarketScreen(navController: NavController) {
    var selectedCategory by remember { mutableStateOf("All") }
    val categories = listOf("All", "Cereals", "Vegetables", "Spices", "Oilseeds")

    val marketItems = listOf(
        MarketPriceItem(
            id = "1",
            cropName = "Paddy / Rice",
            variety = "Pusa 1121",
            mandi = "Ludhiana APMC",
            currentPrice = 4350,
            priceChange = 120,
            isUp = true,
            recommendation = "SELL NOW",
            recommendationDetail = "Peak mandi demand. Prices expected to taper off next week.",
            category = "Cereals"
        ),
        MarketPriceItem(
            id = "2",
            cropName = "Wheat",
            variety = "Sharbati / PBW 725",
            mandi = "Khanna Mandi",
            currentPrice = 2480,
            priceChange = -30,
            isUp = false,
            recommendation = "HOLD",
            recommendationDetail = "Govt procurement opens in 5 days. Expected +₹150 gain.",
            category = "Cereals"
        ),
        MarketPriceItem(
            id = "3",
            cropName = "Tomato",
            variety = "Hybrid Red",
            mandi = "Azadpur Mandi",
            currentPrice = 3200,
            priceChange = 400,
            isUp = true,
            recommendation = "SELL NOW",
            recommendationDetail = "Strong retail demand in urban hubs.",
            category = "Vegetables"
        ),
        MarketPriceItem(
            id = "4",
            cropName = "Cotton",
            variety = "Medium Staple",
            mandi = "Bhatinda APMC",
            currentPrice = 7100,
            priceChange = -80,
            isUp = false,
            recommendation = "HOLD",
            recommendationDetail = "Textile mill buying expected to pick up next fortnight.",
            category = "Oilseeds"
        ),
        MarketPriceItem(
            id = "5",
            cropName = "Red Chilli",
            variety = "Teja / Guntur",
            mandi = "Guntur Mandi",
            currentPrice = 18500,
            priceChange = 650,
            isUp = true,
            recommendation = "SELL NOW",
            recommendationDetail = "High export demand to South East Asia.",
            category = "Spices"
        )
    )

    val filteredItems = if (selectedCategory == "All") marketItems else marketItems.filter { it.category == selectedCategory }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("📈 APMC Market Prices", fontWeight = FontWeight.Bold, color = Color.White, fontSize = 17.sp)
                        Text("Real-time Mandi Rates & AI Sell/Hold Advice", fontSize = 11.sp, color = Color.White.copy(alpha = 0.8f))
                    }
                },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = SageDeep)
            )
        },
        bottomBar = {
            AgriBottomNav(
                currentRoute = "market",
                onNavigate = { route ->
                    when (route) {
                        "home" -> navController.navigate(Home) { popUpTo(Home) { inclusive = true } }
                        "advisor" -> navController.navigate(Advisor)
                        "weather" -> navController.navigate(Weather)
                        "profile" -> navController.navigate(Profile)
                    }
                }
            )
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(Color(0xFFFAFDF8))
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item { Spacer(Modifier.height(4.dp)) }

            // Location Mandi Status Banner
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(14.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFE8F4E8))
                ) {
                    Row(
                        modifier = Modifier.padding(14.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Text("📍 Punjab & North APMC Mandis", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = Color(0xFF1B4332))
                            Text("Updated Today · 6:00 AM Govt Agmarknet Feed", fontSize = 11.sp, color = Color(0xFF555555))
                        }
                        Badge(containerColor = Color(0xFF2D6A4F)) {
                            Text("LIVE", color = Color.White, modifier = Modifier.padding(horizontal = 4.dp))
                        }
                    }
                }
            }

            // Category Filter Chips Row
            item {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(categories) { category ->
                        val selected = selectedCategory == category
                        FilterChip(
                            selected = selected,
                            onClick = { selectedCategory = category },
                            label = { Text(category, fontSize = 12.sp) },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = Color(0xFF2D6A4F),
                                selectedLabelColor = Color.White
                            )
                        )
                    }
                }
            }

            // Market Price Cards
            items(filteredItems) { item ->
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(item.cropName, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color(0xFF1B4332))
                                Text("${item.variety} · ${item.mandi}", fontSize = 12.sp, color = Color(0xFF666666))
                            }

                            // SELL NOW / HOLD AI Badge
                            val badgeBg = if (item.recommendation == "SELL NOW") Color(0xFF2D6A4F) else Color(0xFFE65100)
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = badgeBg.copy(alpha = 0.15f),
                                border = androidx.compose.foundation.BorderStroke(1.dp, badgeBg)
                            ) {
                                Text(
                                    text = item.recommendation,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = badgeBg,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }

                        Spacer(Modifier.height(12.dp))

                        // Price & Trend Row
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.Bottom
                        ) {
                            Column {
                                Text("Mandi Price", fontSize = 10.sp, color = Color.Gray)
                                Text("₹${item.currentPrice} / qtl", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1B4332))
                            }

                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = if (item.isUp) Icons.Default.TrendingUp else Icons.Default.TrendingDown,
                                    contentDescription = null,
                                    tint = if (item.isUp) Color(0xFF2D6A4F) else Color(0xFFD32F2F),
                                    modifier = Modifier.size(18.dp)
                                )
                                Spacer(Modifier.width(4.dp))
                                Text(
                                    text = "${if (item.isUp) "+" else ""}₹${item.priceChange}",
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = if (item.isUp) Color(0xFF2D6A4F) else Color(0xFFD32F2F)
                                )
                            }
                        }

                        Spacer(Modifier.height(8.dp))
                        Text(item.recommendationDetail, fontSize = 11.sp, color = Color(0xFF444444))

                        Spacer(Modifier.height(12.dp))

                        // Ask AI Action
                        OutlinedButton(
                            onClick = { navController.navigate(Advisor) },
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(10.dp),
                            border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF2D6A4F))
                        ) {
                            Text("Ask AI Market Advice →", fontSize = 12.sp, color = Color(0xFF2D6A4F), fontWeight = FontWeight.SemiBold)
                        }
                    }
                }
            }

            item { Spacer(Modifier.height(16.dp)) }
        }
    }
}
