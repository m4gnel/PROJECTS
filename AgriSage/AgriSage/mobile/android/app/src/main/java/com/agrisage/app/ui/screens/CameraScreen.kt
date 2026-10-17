package com.agrisage.app.ui.screens

import android.graphics.ImageFormat
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.agrisage.app.ui.theme.ColorPrimary

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CameraScreen(
    viewModel: CameraViewModel,
    onNavigateBack: () -> Unit,
    onPhotoCaptured: (String) -> Unit
) {
    val qualityLevel by viewModel.qualityLevel.collectAsState()
    val currentCrop by viewModel.currentCrop.collectAsState()
    val haptic = LocalHapticFeedback.current
    var showDialog by remember { mutableStateOf(false) }
    var rejectionMessage by remember { mutableStateOf("") }
    var showCropSheet by remember { mutableStateOf(false) }

    val barColor by animateColorAsState(
        targetValue = when (qualityLevel) {
            QualityLevel.GOOD -> Color(0xFF4CAF50)
            QualityLevel.OKAY -> Color(0xFFFF9800)
            QualityLevel.POOR -> Color(0xFFF44336)
        },
        animationSpec = tween(durationMillis = 200),
        label = "barColorAnimation"
    )

    val qualityMessage = when (qualityLevel) {
        QualityLevel.GOOD -> "Good — tap to capture"
        QualityLevel.OKAY -> "Hold steady for better results"
        QualityLevel.POOR -> "Image blurry — hold steady in bright light"
    }

    Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        // Camera Preview Placeholder / AndroidView
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text("CameraX Preview Window", color = Color.White)
        }

        // Top Controls: Close button & CropChip
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 40.dp, start = 16.dp, end = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = onNavigateBack,
                modifier = Modifier
                    .size(48.dp)
                    .background(Color.Black.copy(alpha = 0.5f), CircleShape)
            ) {
                Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White)
            }

            Surface(
                onClick = { showCropSheet = true },
                shape = RoundedCornerShape(16.dp),
                color = ColorPrimary,
                modifier = Modifier.padding(8.dp)
            ) {
                Text(
                    text = "Crop: ${currentCrop.replaceFirstChar { it.uppercase() }}",
                    color = Color.White,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                    style = MaterialTheme.typography.labelLarge
                )
            }
        }

        // Bottom Quality Indicator Bar & Controls
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .background(barColor)
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = qualityMessage,
                color = Color.White,
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )

            Spacer(modifier = Modifier.height(24.dp))

            // 80.dp Capture Button
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .align(Alignment.CenterHorizontally)
                    .background(Color.White, CircleShape)
                    .border(4.dp, ColorPrimary, CircleShape)
                    .clickable {
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        if (qualityLevel == QualityLevel.POOR) {
                            rejectionMessage = "Image quality is too low (blurred or poor light). Please hold steady in bright light."
                            showDialog = true
                        } else {
                            val dummyPath = "/tmp/captured_leaf.jpg"
                            viewModel.onCaptureComplete(dummyPath)
                            onPhotoCaptured(dummyPath)
                        }
                    }
            )

            Spacer(modifier = Modifier.height(48.dp))
        }

        if (showDialog) {
            AlertDialog(
                onDismissRequest = { showDialog = false },
                title = { Text("Photo Rejected") },
                text = { Text(rejectionMessage) },
                confirmButton = {
                    TextButton(onClick = { showDialog = false }) {
                        Text("Try Again")
                    }
                }
            )
        }

        if (showCropSheet) {
            ModalBottomSheet(onDismissRequest = { showCropSheet = false }) {
                Column(modifier = Modifier.padding(24.dp)) {
                    Text("Select Crop", style = MaterialTheme.typography.headlineSmall)
                    Spacer(modifier = Modifier.height(16.dp))
                    listOf("rice", "banana", "coconut", "tomato", "maize").forEach { crop ->
                        TextButton(
                            onClick = {
                                viewModel.onCropSelected(crop)
                                showCropSheet = false
                            },
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text(crop.replaceFirstChar { it.uppercase() }, style = MaterialTheme.typography.bodyLarge)
                        }
                    }
                }
            }
        }
    }
}

/**
 * Utility class for analyzing image quality from raw YUV byte data.
 * Used with CameraX ImageAnalysis callback when CameraX is integrated.
 */
class ImageQualityAnalyzer(private val onQualityAnalyzed: (QualityLevel) -> Unit) {
    fun analyze(bytes: ByteArray) {
        var sum = 0L
        for (b in bytes) {
            sum += (b.toInt() and 0xFF)
        }
        val mean = sum.toDouble() / bytes.size.coerceAtLeast(1)

        val quality = when {
            mean < 40.0 || mean > 220.0 -> QualityLevel.POOR
            else -> QualityLevel.GOOD
        }
        onQualityAnalyzed(quality)
    }
}
