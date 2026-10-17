package com.agrisage.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.agrisage.app.ui.components.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdvisoryResultScreen(
    advisoryId: String,
    viewModel: AdvisoryResultViewModel,
    onNavigateBack: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Advisory Details") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { /* Share */ }) {
                        Icon(Icons.Default.Share, contentDescription = "Share")
                    }
                }
            )
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 1. Badges
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    ConfidenceBadge(state = "CONFIRMED")
                    RiskLevelBadge(level = "HIGH")
                }
            }

            // 2. Diagnosis Summary
            item {
                Text(
                    text = "Rice Blast (Magnaporthe oryzae) detected with 92% confidence.",
                    style = MaterialTheme.typography.headlineSmall
                )
            }

            // 3. Evidence Card
            item {
                EvidenceCard(
                    items = listOf(
                        "Visual leaf lesions match blast symptoms",
                        "Weather DFI is 0.82 (High disease risk)",
                        "Crop stage is tillering (vulnerable period)"
                    )
                )
            }

            // 4. Scenarios
            item {
                Text("Scenarios Evaluated", style = MaterialTheme.typography.headlineSmall)
            }
            item {
                ScenarioCard(
                    label = "Scenario A: Fungicide Spray",
                    action = "Apply Tricyclazole 75 WP @ 0.6g/L water",
                    expectedYield = 4200.0,
                    cost = 450.0,
                    netReturn = 82000.0,
                    isRecommended = true
                )
            }
            item {
                ScenarioCard(
                    label = "Scenario B: Biological Control",
                    action = "Apply Pseudomonas fluorescens @ 10g/L",
                    expectedYield = 3800.0,
                    cost = 200.0,
                    netReturn = 74000.0,
                    isRecommended = false
                )
            }

            // 5. Recommended Action Card
            item {
                ActionCard(
                    what = "Apply Tricyclazole 75 WP at 0.6g per liter of water",
                    whenTime = "Today between 4:00 PM and 6:30 PM",
                    how = "Foliar spray covering upper and lower leaves evenly",
                    sprayWindow = "4:00 PM - 6:30 PM (No rain expected)",
                    costNote = "₹400 - ₹500 per acre"
                )
            }

            // 6. Feedback Row
            item {
                FeedbackRow(
                    onThumbsUp = { viewModel.submitFeedback(true) },
                    onThumbsDown = { viewModel.submitFeedback(false) }
                )
            }
        }
    }
}
