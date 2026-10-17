package com.agrisage.app.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.unit.dp
import com.agrisage.app.ui.theme.*

@Composable
fun ConfidenceBadge(state: String) {
    val bgColor = when (state) {
        "CONFIRMED" -> ColorConfidenceConfirmed
        "LIKELY" -> ColorConfidenceLikely
        "POSSIBLE" -> ColorConfidencePossible
        "UNCERTAIN" -> ColorConfidenceUncertain
        "INSUFFICIENT_DATA" -> ColorConfidenceInsufficient
        "CONFLICTING_EVIDENCE" -> ColorConfidenceUncertain
        else -> ColorConfidenceInsufficient
    }

    Box(
        modifier = Modifier
            .height(32.dp)
            .background(bgColor, RoundedCornerShape(16.dp))
            .padding(horizontal = 16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = state,
            color = Color.White,
            style = MaterialTheme.typography.labelMedium
        )
    }
}

@Composable
fun RiskLevelBadge(level: String) {
    val bgColor = when (level.uppercase()) {
        "CRITICAL" -> ColorRiskCritical
        "HIGH" -> ColorRiskHigh
        "MEDIUM" -> ColorRiskMedium
        else -> ColorRiskLow
    }

    Box(
        modifier = Modifier
            .height(32.dp)
            .background(bgColor, RoundedCornerShape(16.dp))
            .padding(horizontal = 16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "RISK: ${level.uppercase()}",
            color = Color.White,
            style = MaterialTheme.typography.labelMedium
        )
    }
}

@Composable
fun EvidenceCard(items: List<String>, initialExpanded: Boolean = true) {
    var expanded by remember { mutableStateOf(initialExpanded) }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(ColorInfoBg, RoundedCornerShape(12.dp))
            .padding(start = 4.dp)
            .background(ColorPrimary, RoundedCornerShape(topStart = 12.dp, bottomStart = 12.dp))
            .padding(start = 4.dp)
            .background(ColorInfoBg, RoundedCornerShape(12.dp))
            .clickable { expanded = !expanded }
            .padding(16.dp)
    ) {
        Column {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Key Evidence", style = MaterialTheme.typography.headlineSmall)
                Icon(
                    imageVector = if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                    contentDescription = "Expand"
                )
            }

            AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.padding(top = 12.dp)) {
                    items.forEach { item ->
                        Row(modifier = Modifier.padding(vertical = 4.dp)) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = ColorPrimary
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(item, style = MaterialTheme.typography.bodyMedium)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ModelledEstimateLabel() {
    Text(
        text = "* Modelled estimate — actual results vary by field conditions",
        style = MaterialTheme.typography.bodySmall.copy(fontStyle = FontStyle.Italic),
        color = ColorOnSurfaceTertiary,
        modifier = Modifier.padding(top = 2.dp, bottom = 6.dp)
    )
}

@Composable
fun ActionCard(what: String, whenTime: String, how: String, sprayWindow: String?, costNote: String) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(ColorPrimaryLight, RoundedCornerShape(16.dp))
            .border(2.dp, ColorPrimary, RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            Text("Recommended Action", style = MaterialTheme.typography.headlineSmall, color = ColorPrimaryDark)
            Spacer(modifier = Modifier.height(12.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Build, contentDescription = null, tint = ColorPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text("WHAT: $what", style = MaterialTheme.typography.bodyLarge)
            }
            Spacer(modifier = Modifier.height(8.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.DateRange, contentDescription = null, tint = ColorPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text("WHEN: $whenTime", style = MaterialTheme.typography.bodyMedium)
            }
            Spacer(modifier = Modifier.height(8.dp))

            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Info, contentDescription = null, tint = ColorPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text("HOW: $how", style = MaterialTheme.typography.bodyMedium)
            }

            if (sprayWindow != null) {
                Spacer(modifier = Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.WbSunny, contentDescription = null, tint = ColorWarningText)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("SPRAY WINDOW: $sprayWindow", style = MaterialTheme.typography.bodyMedium)
                }
            }

            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.ShoppingCart, contentDescription = null, tint = ColorPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text("COST: $costNote", style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
fun ScenarioCard(
    label: String,
    action: String,
    expectedYield: Double,
    cost: Double,
    netReturn: Double,
    isRecommended: Boolean
) {
    val borderColor = if (isRecommended) ColorPrimary else ColorOutline
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White, RoundedCornerShape(12.dp))
            .border(2.dp, borderColor, RoundedCornerShape(12.dp))
            .padding(16.dp)
    ) {
        Column {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(label, style = MaterialTheme.typography.headlineSmall)
                if (isRecommended) {
                    Text("RECOMMENDED", color = ColorPrimary, style = MaterialTheme.typography.labelLarge)
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text("Action: $action", style = MaterialTheme.typography.bodyMedium)
            Spacer(modifier = Modifier.height(8.dp))

            Text("Expected Yield: $expectedYield kg/ha", style = MaterialTheme.typography.bodyLarge)
            ModelledEstimateLabel()

            Text("Net Return: ₹$netReturn", style = MaterialTheme.typography.bodyLarge)
            ModelledEstimateLabel()

            Text("Cost: ₹$cost", style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
fun FeedbackRow(onThumbsUp: () -> Unit, onThumbsDown: () -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text("Was this advisory helpful?", style = MaterialTheme.typography.bodyMedium)
        Row {
            IconButton(onClick = onThumbsUp, modifier = Modifier.size(48.dp)) {
                Text("👍", style = MaterialTheme.typography.headlineMedium)
            }
            IconButton(onClick = onThumbsDown, modifier = Modifier.size(48.dp)) {
                Text("👎", style = MaterialTheme.typography.headlineMedium)
            }
        }
    }
}
