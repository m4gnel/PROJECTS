package com.agrisage.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.agrisage.app.navigation.Home
import com.agrisage.app.navigation.Onboarding
import com.agrisage.app.ui.theme.*

/**
 * Screen 2: Onboarding (3 steps)
 * Route: Onboarding(step=0,1,2)
 *
 * Step 0: Language selection (6 languages)
 * Step 1: Location (state, district, farm size)
 * Step 2: Crop selection (multi-select)
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OnboardingScreen(
    navController: NavController,
    step: Int,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFFAFDF8))
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        // Progress dots
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center
        ) {
            (0..2).forEach { dotIndex ->
                Box(
                    modifier = Modifier
                        .size(if (dotIndex == step) 10.dp else 8.dp)
                        .background(
                            if (dotIndex == step) Color(0xFF52B788)
                            else Color(0xFFE8F4E8),
                            RoundedCornerShape(50)
                        )
                )
                if (dotIndex < 2) Spacer(Modifier.width(8.dp))
            }
        }

        Spacer(Modifier.height(32.dp))

        when (step) {
            0 -> OnboardingStep0(navController)
            1 -> OnboardingStep1(navController)
            2 -> OnboardingStep2(navController)
        }
    }
}

// ── Step 0: Language Selection ─────────────────────────────────────────────────

@Composable
private fun OnboardingStep0(navController: NavController) {
    var selectedLang by remember { mutableStateOf("") }

    val languages = listOf(
        Triple("हिंदी", "Hindi", "hi"),
        Triple("English", "English", "en"),
        Triple("தமிழ்", "Tamil", "ta"),
        Triple("മലയാളം", "Malayalam", "ml"),
        Triple("తెలుగు", "Telugu", "te"),
        Triple("ਪੰਜਾਬੀ", "Punjabi", "pa"),
    )

    Text(
        text = "Choose your language",
        style = MaterialTheme.typography.headlineLarge,
        color = Color(0xFF1B4332),
        fontWeight = FontWeight.Bold
    )
    Spacer(Modifier.height(8.dp))
    Text(
        text = "Get advice in the language you're comfortable with",
        style = MaterialTheme.typography.bodyMedium,
        color = Color(0xFF6B7280)
    )
    Spacer(Modifier.height(24.dp))

    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.height(240.dp)
    ) {
        items(languages) { (native, english, code) ->
            val selected = selectedLang == code
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        if (selected) Color(0xFF52B788) else Color(0xFFE8F4E8),
                        RoundedCornerShape(16.dp)
                    )
                    .border(
                        1.dp,
                        if (selected) Color(0xFF2D6A4F) else Color.Transparent,
                        RoundedCornerShape(16.dp)
                    )
                    .clickable { selectedLang = code }
                    .padding(16.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = "🇮🇳",
                        fontSize = 24.sp
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        text = native,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = if (selected) Color.White else Color(0xFF1B4332)
                    )
                    Text(
                        text = english,
                        fontSize = 11.sp,
                        color = if (selected) Color.White.copy(alpha = 0.8f) else Color(0xFF6B7280)
                    )
                }
            }
        }
    }

    Spacer(Modifier.height(32.dp))

    Button(
        onClick = {
            // TODO: Save to DataStore selectedLang
            navController.navigate(Onboarding(step = 1))
        },
        enabled = selectedLang.isNotEmpty(),
        modifier = Modifier.fillMaxWidth().height(52.dp),
        shape = RoundedCornerShape(16.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2D6A4F))
    ) {
        Text("Continue", fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
    }
}

// ── Step 1: Location ───────────────────────────────────────────────────────────

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun OnboardingStep1(navController: NavController) {
    val indianStates = listOf(
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli",
        "Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    )

    var selectedState by remember { mutableStateOf("") }
    var district by remember { mutableStateOf("") }
    var farmSize by remember { mutableStateOf("") }
    var expandedState by remember { mutableStateOf(false) }

    Text(
        text = "Where is your farm?",
        style = MaterialTheme.typography.headlineLarge,
        color = Color(0xFF1B4332),
        fontWeight = FontWeight.Bold
    )
    Spacer(Modifier.height(24.dp))

    // State dropdown
    Text("State", style = MaterialTheme.typography.labelLarge, color = Color(0xFF1B4332))
    Spacer(Modifier.height(4.dp))
    ExposedDropdownMenuBox(
        expanded = expandedState,
        onExpandedChange = { expandedState = it }
    ) {
        OutlinedTextField(
            value = selectedState,
            onValueChange = {},
            readOnly = true,
            placeholder = { Text("Select State") },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedState) },
            modifier = Modifier.fillMaxWidth().menuAnchor()
        )
        ExposedDropdownMenu(
            expanded = expandedState,
            onDismissRequest = { expandedState = false },
            modifier = Modifier.height(250.dp)
        ) {
            indianStates.forEach { state ->
                DropdownMenuItem(
                    text = { Text(state) },
                    onClick = {
                        selectedState = state
                        expandedState = false
                    }
                )
            }
        }
    }

    Spacer(Modifier.height(12.dp))

    Text("District", style = MaterialTheme.typography.labelLarge, color = Color(0xFF1B4332))
    Spacer(Modifier.height(4.dp))
    OutlinedTextField(
        value = district,
        onValueChange = { district = it },
        placeholder = { Text("Enter District (e.g. Ludhiana)") },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true
    )

    Spacer(Modifier.height(12.dp))

    Text("Farm size (acres)", style = MaterialTheme.typography.labelLarge, color = Color(0xFF1B4332))
    Spacer(Modifier.height(4.dp))
    OutlinedTextField(
        value = farmSize,
        onValueChange = { farmSize = it },
        placeholder = { Text("e.g. 5.0") },
        modifier = Modifier.fillMaxWidth(),
        singleLine = true
    )

    Spacer(Modifier.height(16.dp))

    // GPS button
    OutlinedButton(
        onClick = {
            selectedState = "Punjab"
            district = "Ludhiana"
            farmSize = "5.0"
        },
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Icon(Icons.Default.LocationOn, contentDescription = null, tint = Color(0xFF2D6A4F))
        Spacer(Modifier.width(8.dp))
        Text("Use my location", color = Color(0xFF2D6A4F))
    }

    Spacer(Modifier.height(32.dp))

    Button(
        onClick = {
            // TODO: Save to DataStore
            navController.navigate(Onboarding(step = 2))
        },
        enabled = selectedState.isNotEmpty() && district.isNotEmpty(),
        modifier = Modifier.fillMaxWidth().height(52.dp),
        shape = RoundedCornerShape(16.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2D6A4F))
    ) {
        Text("Continue", fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
    }
}

// ── Step 2: Crop Selection ─────────────────────────────────────────────────────

@Composable
private fun OnboardingStep2(navController: NavController) {
    val allCrops = listOf(
        // National crops per master spec
        "🌾 Wheat" to "Wheat",         "🌾 Rice/Paddy" to "Rice",
        "🌿 Cotton" to "Cotton",         "🎋 Sugarcane" to "Sugarcane",
        "🌽 Maize" to "Maize",           "🟤 Soybean" to "Soybean",
        "🌻 Mustard" to "Mustard",       "🥜 Groundnut" to "Groundnut",
        "🌻 Sunflower" to "Sunflower",   "🧅 Onion" to "Onion",
        "🥔 Potato" to "Potato",         "🍅 Tomato" to "Tomato",
        "🌶️ Chilli" to "Chilli",         "💛 Turmeric" to "Turmeric",
        "🫚 Ginger" to "Ginger",         "🧄 Garlic" to "Garlic",
        "🫛 Peas" to "Peas",             "🫘 Lentils" to "Lentils",
        "🥥 Coconut" to "Coconut",       "🍌 Banana" to "Banana",
        "🥭 Mango" to "Mango",           "🍎 Pomegranate" to "Pomegranate",
        "🍇 Grapes" to "Grapes",         "🍈 Papaya" to "Papaya",
        "🌴 Rubber" to "Rubber",          "🫛 Cardamom" to "Cardamom",
        "🌿 Pepper" to "Pepper",          "🍵 Tea" to "Tea",
        "☕ Coffee" to "Coffee",           "🌿 Arecanut" to "Arecanut",
    )

    val selected = remember { mutableStateListOf<String>() }

    Text(
        text = "What do you grow?",
        style = MaterialTheme.typography.headlineLarge,
        color = Color(0xFF1B4332),
        fontWeight = FontWeight.Bold
    )
    Spacer(Modifier.height(4.dp))
    Text(
        text = "Select all that apply — you can change this later",
        style = MaterialTheme.typography.bodyMedium,
        color = Color(0xFF6B7280)
    )
    Spacer(Modifier.height(16.dp))

    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
        modifier = Modifier.height(400.dp)
    ) {
        items(allCrops) { (emoji_label, cropName) ->
            val isSelected = selected.contains(cropName)
            FilterChip(
                selected = isSelected,
                onClick = {
                    if (isSelected) selected.remove(cropName)
                    else selected.add(cropName)
                },
                label = { Text(emoji_label, fontSize = 12.sp) },
                leadingIcon = if (isSelected) {
                    { Icon(Icons.Default.Check, null, Modifier.size(16.dp)) }
                } else null,
                modifier = Modifier.fillMaxWidth(),
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = Color(0xFF52B788),
                    selectedLabelColor = Color.White,
                )
            )
        }
    }

    Spacer(Modifier.height(24.dp))

    Button(
        onClick = {
            // TODO: Save selected crops to DataStore, set onboarding_complete = true
            navController.navigate(Home) {
                popUpTo(Onboarding(step = 0)) { inclusive = true }
            }
        },
        enabled = selected.isNotEmpty(),
        modifier = Modifier.fillMaxWidth().height(52.dp),
        shape = RoundedCornerShape(16.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2D6A4F))
    ) {
        Text("Start Farming with AI 🌾", fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 800)
@Composable
fun OnboardingStep0Preview() {
    OnboardingScreen(navController = rememberNavController(), step = 0)
}

@Preview(showBackground = true, widthDp = 360, heightDp = 800)
@Composable
fun OnboardingStep1Preview() {
    OnboardingScreen(navController = rememberNavController(), step = 1)
}

@Preview(showBackground = true, widthDp = 360, heightDp = 800)
@Composable
fun OnboardingStep2Preview() {
    OnboardingScreen(navController = rememberNavController(), step = 2)
}
