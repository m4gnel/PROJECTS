package com.agrisage.app.ui.screens.fields

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
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
import com.agrisage.app.navigation.Screen
import com.agrisage.app.ui.components.FieldCard
import com.agrisage.app.ui.components.LoadingOverlay
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireGold
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSageLight
import com.agrisage.app.ui.theme.WireSurface
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireWhite

@Composable
fun FieldsScreen(
    navController: NavHostController,
    viewModel: FieldsViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    var newFieldName by remember { mutableStateOf("") }
    var newFieldArea by remember { mutableStateOf("2500") }

    Box(modifier = Modifier.fillMaxSize().background(WireWhite)) {
        LazyColumn(
            modifier = Modifier.fillMaxSize()
        ) {
            // Header Top Bar in SageDeep
            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(WireSageDeep)
                        .padding(horizontal = 20.dp, vertical = 18.dp)
                ) {
                    Text(
                        text = "📍 My Fields",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color.White
                    )
                    Text(
                        text = "Satellite monitoring & plot registry",
                        fontSize = 12.sp,
                        color = Color.White.copy(alpha = 0.75f),
                        modifier = Modifier.padding(top = 2.dp)
                    )

                    Spacer(modifier = Modifier.height(14.dp))

                    // Satellite map placeholder
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(110.dp),
                        shape = RoundedCornerShape(14.dp),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .background(
                                    brush = Brush.linearGradient(
                                        colors = listOf(WireSageDeep, WireSageLight)
                                    )
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(text = "📍", fontSize = 28.sp)
                                Text(
                                    text = "Satellite Field View (NASA / Sentinel)",
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = Color.White.copy(alpha = 0.85f),
                                    modifier = Modifier.padding(top = 4.dp)
                                )
                            }
                        }
                    }
                }
            }

            item {
                Column(modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 4.dp)) {
                    Text(
                        text = "REGISTERED PLOTS (${state.fields.size})",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        color = WireTextMuted,
                        letterSpacing = 1.sp
                    )
                }
            }

            items(state.fields) { field ->
                Box(modifier = Modifier.padding(horizontal = 16.dp)) {
                    FieldCard(
                        name = field.name,
                        areaSqM = field.areaSqM,
                        cropName = field.cropName,
                        lastNdvi = field.lastNdvi,
                        onClick = { navController.navigate(Screen.FieldDetail(field.id)) }
                    )
                }
            }

            // + Add New Field card
            item {
                Box(modifier = Modifier.padding(horizontal = 16.dp, vertical = 6.dp)) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { viewModel.showAddDialog() },
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = WireSurface),
                        border = BorderStroke(1.5.dp, WireBorder)
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 14.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = "+ Add New Field",
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = WireTextMuted
                            )
                        }
                    }
                }
            }

            item {
                Spacer(modifier = Modifier.height(72.dp))
            }
        }

        // Add Field FAB in Gold
        FloatingActionButton(
            onClick = { viewModel.showAddDialog() },
            containerColor = WireGold,
            contentColor = Color.White,
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(20.dp)
        ) {
            Icon(imageVector = Icons.Default.Add, contentDescription = "Add Field")
        }

        // Add Dialog
        if (state.showAddDialog) {
            AlertDialog(
                onDismissRequest = { viewModel.hideAddDialog() },
                title = { Text("Add New Field Plot", fontWeight = FontWeight.Bold) },
                text = {
                    Column {
                        OutlinedTextField(
                            value = newFieldName,
                            onValueChange = { newFieldName = it },
                            label = { Text("Field Name (e.g. West Grove)") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        OutlinedTextField(
                            value = newFieldArea,
                            onValueChange = { newFieldArea = it },
                            label = { Text("Area in sq meters") },
                            modifier = Modifier.fillMaxWidth()
                        )
                    }
                },
                confirmButton = {
                    Button(
                        onClick = {
                            val area = newFieldArea.toFloatOrNull() ?: 2000f
                            viewModel.addField(newFieldName.ifBlank { "Field Plot" }, area, 10.165, 76.401)
                            newFieldName = ""
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = WireSage)
                    ) {
                        Text("Add Plot")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { viewModel.hideAddDialog() }) {
                        Text("Cancel")
                    }
                }
            )
        }

        LoadingOverlay(isLoading = state.isLoading)
    }
}
