package com.agrisage.app.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material3.Icon
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Fill
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.cos
import kotlin.math.sin

enum class FarmZone(val id: String, val title: String, val emoji: String) {
    OVERVIEW("overview", "Overview", "🗺️"),
    FARM_HOUSE("farm_house", "Farm House", "🏠"),
    TOMATO_FIELD("tomatoes", "Tomato Field", "🍅"),
    VEGETABLE_FIELD("vegetables", "Vegetable Field", "🥦"),
    CORN_FIELD("corn", "Corn Field", "🌽"),
    ANIMAL_AREA("animals", "Animal Area", "🐮"),
    WATER_TANK("water", "Water Tank", "💧"),
    STORAGE("storage", "Storage", "🏭")
}

/**
 * Deterministic 1:1 replication of the interactive top-down aerial Farm Map from Reference Video 2.
 * Renders 7 zones with responsive sub-pixel geometry, micro-animations, and interactive zone selection.
 */
@Composable
fun FarmMapCanvas(
    selectedZone: FarmZone,
    onZoneSelected: (FarmZone) -> Unit,
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "farm_map_animation")
    val waterPhase by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 6.28318f,
        animationSpec = infiniteRepeatable(
            animation = tween(2600, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "water_ripple"
    )
    val smokeOffset by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "chimney_smoke"
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(350.dp)
            .shadow(4.dp, RoundedCornerShape(24.dp))
            .clip(RoundedCornerShape(24.dp))
            .background(Color(0xFF86D17C))
            .border(1.dp, Color(0xFFE2E8F0), RoundedCornerShape(24.dp))
    ) {
        // Base Canvas for Ground, Roads, Plots and Details
        Canvas(modifier = Modifier.fillMaxSize()) {
            val w = size.width
            val h = size.height

            // 1. Draw sand/dirt pathways dividing the farm
            drawRoadways(w, h)

            // 2. Zone 1: Farm House (Top-Left)
            drawFarmHouse(w * 0.02f, h * 0.02f, w * 0.35f, h * 0.30f, smokeOffset)

            // 3. Zone 2: Tomato Field (Top-Right)
            drawTomatoField(w * 0.40f, h * 0.02f, w * 0.58f, h * 0.30f)

            // 4. Zone 3: Vegetable Field (Middle-Left)
            drawVegetableField(w * 0.02f, h * 0.34f, w * 0.35f, h * 0.30f)

            // 5. Zone 4: Corn Field (Middle-Right)
            drawCornField(w * 0.40f, h * 0.34f, w * 0.58f, h * 0.30f)

            // 6. Zone 5: Animal Area (Bottom-Left)
            drawAnimalArea(w * 0.02f, h * 0.66f, w * 0.54f, h * 0.32f)

            // 7. Zone 6: Water Tank & Pond (Bottom-Right Upper)
            drawWaterPondAndTank(w * 0.58f, h * 0.66f, w * 0.40f, h * 0.16f, waterPhase)

            // 8. Zone 7: Storage & Silos (Bottom-Right Lower)
            drawStorageAndSilos(w * 0.58f, h * 0.83f, w * 0.40f, h * 0.15f)
        }

        // Zone Click Overlay Boxes with Glowing White Pill Border on Selection
        // Zone 1: Farm House
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.36f)
                .fillMaxHeight(0.31f)
                .align(Alignment.TopStart)
                .padding(4.dp),
            isSelected = selectedZone == FarmZone.FARM_HOUSE,
            label = "🏠 House",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.FARM_HOUSE,
            onClick = { onZoneSelected(FarmZone.FARM_HOUSE) }
        )

        // Zone 2: Tomato Field
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.60f)
                .fillMaxHeight(0.31f)
                .align(Alignment.TopEnd)
                .padding(4.dp),
            isSelected = selectedZone == FarmZone.TOMATO_FIELD,
            label = "🍅 Tomatoes",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.TOMATO_FIELD,
            onClick = { onZoneSelected(FarmZone.TOMATO_FIELD) }
        )

        // Zone 3: Vegetable Field
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.36f)
                .fillMaxHeight(0.31f)
                .align(Alignment.CenterStart)
                .padding(4.dp),
            isSelected = selectedZone == FarmZone.VEGETABLE_FIELD,
            label = "🥦 Vegetables",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.VEGETABLE_FIELD,
            onClick = { onZoneSelected(FarmZone.VEGETABLE_FIELD) }
        )

        // Zone 4: Corn Field
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.60f)
                .fillMaxHeight(0.31f)
                .align(Alignment.CenterEnd)
                .padding(4.dp),
            isSelected = selectedZone == FarmZone.CORN_FIELD,
            label = "🌽 Corn",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.CORN_FIELD,
            onClick = { onZoneSelected(FarmZone.CORN_FIELD) }
        )

        // Zone 5: Animal Area
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.55f)
                .fillMaxHeight(0.34f)
                .align(Alignment.BottomStart)
                .padding(4.dp),
            isSelected = selectedZone == FarmZone.ANIMAL_AREA,
            label = "🐮 Animals",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.ANIMAL_AREA,
            onClick = { onZoneSelected(FarmZone.ANIMAL_AREA) }
        )

        // Zone 6: Water Tank
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.43f)
                .fillMaxHeight(0.18f)
                .align(Alignment.BottomEnd)
                .padding(bottom = 60.dp, end = 4.dp),
            isSelected = selectedZone == FarmZone.WATER_TANK,
            label = "💧 Water",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.WATER_TANK,
            onClick = { onZoneSelected(FarmZone.WATER_TANK) }
        )

        // Zone 7: Storage
        ZoneHitBox(
            modifier = Modifier
                .fillMaxWidth(0.43f)
                .fillMaxHeight(0.16f)
                .align(Alignment.BottomEnd)
                .padding(4.dp),
            isSelected = selectedZone == FarmZone.STORAGE,
            label = "🏭 Storage",
            showLabel = selectedZone == FarmZone.OVERVIEW || selectedZone == FarmZone.STORAGE,
            onClick = { onZoneSelected(FarmZone.STORAGE) }
        )

        // Top-Right Expand Button
        Surface(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(10.dp)
                .size(32.dp)
                .tactilePress(scaleDown = 0.90f) {
                    onZoneSelected(FarmZone.OVERVIEW)
                },
            shape = CircleShape,
            color = Color.White.copy(alpha = 0.92f),
            shadowElevation = 2.dp
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.Fullscreen,
                    contentDescription = "Reset map",
                    tint = Color(0xFF1E293B),
                    modifier = Modifier.size(18.dp)
                )
            }
        }
    }
}

@Composable
private fun ZoneHitBox(
    modifier: Modifier,
    isSelected: Boolean,
    label: String,
    showLabel: Boolean,
    onClick: () -> Unit
) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .then(
                if (isSelected) {
                    Modifier
                        .border(3.dp, Color.White, RoundedCornerShape(16.dp))
                        .background(Color.White.copy(alpha = 0.12f))
                } else {
                    Modifier
                }
            )
            .clickable(onClick = onClick)
    ) {
        if (showLabel) {
            Surface(
                color = Color.White.copy(alpha = 0.95f),
                shape = RoundedCornerShape(12.dp),
                shadowElevation = 2.dp,
                modifier = Modifier
                    .align(Alignment.TopCenter)
                    .padding(top = 4.dp)
            ) {
                Text(
                    text = label,
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF18181B),
                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                )
            }
        }
    }
}

// ==========================================
// Vector Drawing Functions for Farm Zones
// ==========================================

private fun DrawScope.drawRoadways(w: Float, h: Float) {
    val roadColor = Color(0xFFE8D7B8)
    // Horizontal main road
    drawRect(
        color = roadColor,
        topLeft = Offset(0f, h * 0.315f),
        size = Size(w, h * 0.035f)
    )
    // Second horizontal road
    drawRect(
        color = roadColor,
        topLeft = Offset(0f, h * 0.635f),
        size = Size(w, h * 0.03f)
    )
    // Vertical road separating left & right plots
    drawRect(
        color = roadColor,
        topLeft = Offset(w * 0.365f, 0f),
        size = Size(w * 0.035f, h)
    )
}

private fun DrawScope.drawFarmHouse(x: Float, y: Float, w: Float, h: Float, smokeOffset: Float) {
    // Lawn container
    drawRoundRect(
        color = Color(0xFFA5DC96),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(16f, 16f)
    )

    // Driveway (tan gravel) & car
    drawRoundRect(
        color = Color(0xFFDDD2BA),
        topLeft = Offset(x + w * 0.68f, y + h * 0.45f),
        size = Size(w * 0.26f, h * 0.50f),
        cornerRadius = CornerRadius(8f, 8f)
    )
    // Blue Pickup Car
    drawRoundRect(
        color = Color(0xFF2563EB),
        topLeft = Offset(x + w * 0.72f, y + h * 0.55f),
        size = Size(w * 0.18f, h * 0.30f),
        cornerRadius = CornerRadius(6f, 6f)
    )
    // Car windshield
    drawRoundRect(
        color = Color(0xFF93C5FD),
        topLeft = Offset(x + w * 0.74f, y + h * 0.62f),
        size = Size(w * 0.14f, h * 0.10f),
        cornerRadius = CornerRadius(3f, 3f)
    )

    // Red Gabled Roof of House
    val roofPath = Path().apply {
        moveTo(x + w * 0.10f, y + h * 0.12f)
        lineTo(x + w * 0.60f, y + h * 0.12f)
        lineTo(x + w * 0.60f, y + h * 0.48f)
        lineTo(x + w * 0.10f, y + h * 0.48f)
        close()
    }
    drawPath(roofPath, color = Color(0xFFB91C1C))
    // Roof ridge line
    drawLine(
        color = Color(0xFF991B1B),
        start = Offset(x + w * 0.18f, y + h * 0.30f),
        end = Offset(x + w * 0.52f, y + h * 0.30f),
        strokeWidth = 3f
    )

    // Chimney & Animated Smoke
    drawRect(
        color = Color(0xFF64748B),
        topLeft = Offset(x + w * 0.50f, y + h * 0.14f),
        size = Size(w * 0.07f, h * 0.08f)
    )
    val smokeY = y + h * (0.12f - smokeOffset * 0.10f)
    drawCircle(
        color = Color.White.copy(alpha = 0.7f * (1f - smokeOffset)),
        radius = 5f + smokeOffset * 7f,
        center = Offset(x + w * 0.53f, smokeY)
    )

    // Front Wooden Deck / Porch
    drawRect(
        color = Color(0xFFD97706),
        topLeft = Offset(x + w * 0.22f, y + h * 0.48f),
        size = Size(w * 0.25f, h * 0.10f)
    )

    // Flower Bed
    drawRoundRect(
        color = Color(0xFF6B4226),
        topLeft = Offset(x + w * 0.10f, y + h * 0.62f),
        size = Size(w * 0.35f, h * 0.26f),
        cornerRadius = CornerRadius(6f, 6f)
    )
    for (i in 0..3) {
        drawCircle(Color(0xFFEC4899), 3f, Offset(x + w * (0.15f + i * 0.08f), y + h * 0.68f))
        drawCircle(Color(0xFFEAB308), 3f, Offset(x + w * (0.15f + i * 0.08f), y + h * 0.78f))
    }

    // Round Trees
    drawCircle(Color(0xFF15803D), 12f, Offset(x + w * 0.12f, y + h * 0.22f))
    drawCircle(Color(0xFF16A34A), 10f, Offset(x + w * 0.82f, y + h * 0.18f))
}

private fun DrawScope.drawTomatoField(x: Float, y: Float, w: Float, h: Float) {
    // Soil Plot
    drawRoundRect(
        color = Color(0xFF6B4226),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(16f, 16f)
    )

    // Blue Drip Irrigation Pipes
    drawLine(
        color = Color(0xFF38BDF8),
        start = Offset(x + w * 0.04f, y + h * 0.10f),
        end = Offset(x + w * 0.04f, y + h * 0.90f),
        strokeWidth = 2.5f
    )

    // 4 Rows of Tomato Plants with Bright Red Tomatoes
    val rowCount = 4
    for (r in 0 until rowCount) {
        val rowY = y + h * (0.16f + r * 0.22f)
        // Drip line feeder
        drawLine(
            color = Color(0xFF0284C7).copy(alpha = 0.6f),
            start = Offset(x + w * 0.04f, rowY),
            end = Offset(x + w * 0.94f, rowY),
            strokeWidth = 1.5f
        )
        // Plants in row
        val plantCount = 9
        for (c in 0 until plantCount) {
            val plantX = x + w * (0.10f + c * 0.095f)
            // Green foliage bush
            drawCircle(Color(0xFF15803D), 7f, Offset(plantX, rowY))
            drawCircle(Color(0xFF22C55E), 4.5f, Offset(plantX, rowY - 1.5f))
            // Red ripe tomatoes
            drawCircle(Color(0xFFEF4444), 2.5f, Offset(plantX - 2.5f, rowY + 2f))
            drawCircle(Color(0xFFEF4444), 2.5f, Offset(plantX + 2.5f, rowY - 1f))
        }
    }
}

private fun DrawScope.drawVegetableField(x: Float, y: Float, w: Float, h: Float) {
    // Dark Organic Soil Plot
    drawRoundRect(
        color = Color(0xFF533824),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(16f, 16f)
    )

    // Section 1: Cabbages (Upper half)
    for (r in 0..1) {
        val rowY = y + h * (0.18f + r * 0.20f)
        for (c in 0..4) {
            val colX = x + w * (0.14f + c * 0.18f)
            drawCircle(Color(0xFF4ADE80), 8f, Offset(colX, rowY))
            drawCircle(Color(0xFF16A34A), 4.5f, Offset(colX, rowY))
        }
    }

    // Dividing soil line
    drawLine(
        color = Color(0xFF3E2718),
        start = Offset(x + w * 0.06f, y + h * 0.52f),
        end = Offset(x + w * 0.94f, y + h * 0.52f),
        strokeWidth = 2f
    )

    // Section 2: Carrots (Lower half)
    for (r in 0..1) {
        val rowY = y + h * (0.64f + r * 0.20f)
        for (c in 0..5) {
            val colX = x + w * (0.12f + c * 0.15f)
            // Orange carrot crown peeking
            drawCircle(Color(0xFFEA580C), 4f, Offset(colX, rowY + 2f))
            // Green fern leafy top
            drawLine(
                color = Color(0xFF22C55E),
                start = Offset(colX, rowY),
                end = Offset(colX - 3f, rowY - 6f),
                strokeWidth = 2f
            )
            drawLine(
                color = Color(0xFF22C55E),
                start = Offset(colX, rowY),
                end = Offset(colX + 3f, rowY - 6f),
                strokeWidth = 2f
            )
        }
    }
}

private fun DrawScope.drawCornField(x: Float, y: Float, w: Float, h: Float) {
    // Golden Corn Field Ground
    drawRoundRect(
        color = Color(0xFF75512B),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(16f, 16f)
    )

    // Vertical Rows of Tall Corn Stalks
    val colCount = 8
    for (c in 0 until colCount) {
        val colX = x + w * (0.08f + c * 0.118f)
        val rowCount = 5
        for (r in 0 until rowCount) {
            val stalkY = y + h * (0.12f + r * 0.18f)
            // Green stalk
            drawLine(
                color = Color(0xFF65A30D),
                start = Offset(colX, stalkY + 8f),
                end = Offset(colX, stalkY - 8f),
                strokeWidth = 2f
            )
            // Golden tassel top
            drawCircle(Color(0xFFEAB308), 3f, Offset(colX, stalkY - 8f))
            // Leaves
            drawLine(Color(0xFF84CC16), Offset(colX, stalkY), Offset(colX - 4f, stalkY - 2f), 1.5f)
            drawLine(Color(0xFF84CC16), Offset(colX, stalkY + 2f), Offset(colX + 4f, stalkY), 1.5f)
        }
    }

    // Red Farm Tractor parked at top left headland
    val tracX = x - w * 0.05f
    val tracY = y + h * 0.42f
    drawRoundRect(
        color = Color(0xFFDC2626),
        topLeft = Offset(tracX, tracY),
        size = Size(16f, 22f),
        cornerRadius = CornerRadius(4f, 4f)
    )
    // Tractor black wheels
    drawCircle(Color(0xFF1E293B), 4f, Offset(tracX - 1f, tracY + 5f))
    drawCircle(Color(0xFF1E293B), 5f, Offset(tracX - 1f, tracY + 17f))
}

private fun DrawScope.drawAnimalArea(x: Float, y: Float, w: Float, h: Float) {
    // Lush green pasture
    drawRoundRect(
        color = Color(0xFFA3E635),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(16f, 16f)
    )

    // Wooden Post Fence
    drawRoundRect(
        color = Color(0xFF854D0E),
        topLeft = Offset(x + 4f, y + 4f),
        size = Size(w - 8f, h - 8f),
        cornerRadius = CornerRadius(12f, 12f),
        style = Stroke(width = 2.5f)
    )

    // Red Barn / Shed (Top-Left inside pasture)
    drawRect(
        color = Color(0xFFB91C1C),
        topLeft = Offset(x + w * 0.08f, y + h * 0.12f),
        size = Size(w * 0.28f, h * 0.38f)
    )
    // White X on barn door
    val barnX = x + w * 0.08f
    val barnY = y + h * 0.12f
    val barnW = w * 0.28f
    val barnH = h * 0.38f
    drawLine(Color.White, Offset(barnX + 4f, barnY + 4f), Offset(barnX + barnW - 4f, barnY + barnH - 4f), 2f)
    drawLine(Color.White, Offset(barnX + barnW - 4f, barnY + 4f), Offset(barnX + 4f, barnY + barnH - 4f), 2f)

    // Round Hay Feeder (Center of pasture)
    val feederX = x + w * 0.52f
    val feederY = y + h * 0.45f
    drawCircle(Color(0xFFEAB308), 12f, Offset(feederX, feederY))
    drawCircle(Color(0xFFCA8A04), 8f, Offset(feederX, feederY))

    // Blue Water Trough
    drawRoundRect(
        color = Color(0xFF38BDF8),
        topLeft = Offset(x + w * 0.76f, y + h * 0.10f),
        size = Size(w * 0.18f, h * 0.15f),
        cornerRadius = CornerRadius(4f, 4f)
    )

    // Black & White Spotted Dairy Cows
    drawHolsteinCow(x + w * 0.62f, y + h * 0.24f)
    drawHolsteinCow(x + w * 0.72f, y + h * 0.56f)
    drawHolsteinCow(x + w * 0.32f, y + h * 0.74f)
    drawHolsteinCow(x + w * 0.58f, y + h * 0.78f)
}

private fun DrawScope.drawHolsteinCow(cx: Float, cy: Float) {
    // White cow body oval
    drawOval(
        color = Color.White,
        topLeft = Offset(cx - 9f, cy - 6f),
        size = Size(18f, 12f)
    )
    // Black spots
    drawCircle(Color(0xFF1E293B), 3.5f, Offset(cx - 2f, cy - 2f))
    drawCircle(Color(0xFF1E293B), 2.5f, Offset(cx + 4f, cy + 2f))
    drawCircle(Color(0xFF1E293B), 2f, Offset(cx - 5f, cy + 3f))
    // Head with ears
    drawCircle(Color.White, 4f, Offset(cx + 8f, cy - 1f))
    drawCircle(Color(0xFF1E293B), 2f, Offset(cx + 9f, cy - 3f))
}

private fun DrawScope.drawWaterPondAndTank(x: Float, y: Float, w: Float, h: Float, waterPhase: Float) {
    // Water Zone Background
    drawRoundRect(
        color = Color(0xFF86EFAC),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(14f, 14f)
    )

    // Circular Industrial Water Tank (Left)
    val tankCenterX = x + w * 0.28f
    val tankCenterY = y + h * 0.50f
    val tankRadius = h * 0.40f
    // Steel Outer Rim
    drawCircle(Color(0xFF94A3B8), tankRadius, Offset(tankCenterX, tankCenterY))
    // Blue Water Core
    drawCircle(Color(0xFF0284C7), tankRadius * 0.82f, Offset(tankCenterX, tankCenterY))
    // Concentric Wave Ripple
    val rippleR = (tankRadius * 0.55f) + sin(waterPhase) * 2f
    drawCircle(Color(0xFF38BDF8).copy(alpha = 0.5f), rippleR, Offset(tankCenterX, tankCenterY), style = Stroke(2f))

    // Connecting Pipe
    drawLine(
        color = Color(0xFF64748B),
        start = Offset(tankCenterX + tankRadius, tankCenterY),
        end = Offset(x + w * 0.64f, tankCenterY),
        strokeWidth = 3f
    )

    // Natural Blue Pond with Lily Pads (Right)
    val pondCenterX = x + w * 0.72f
    val pondCenterY = y + h * 0.50f
    drawOval(
        color = Color(0xFF38BDF8),
        topLeft = Offset(pondCenterX - w * 0.22f, pondCenterY - h * 0.38f),
        size = Size(w * 0.44f, h * 0.76f)
    )
    // Floating Green Lily Pads
    drawCircle(Color(0xFF16A34A), 4.5f, Offset(pondCenterX - 6f, pondCenterY - 4f))
    drawCircle(Color(0xFF15803D), 3.5f, Offset(pondCenterX + 8f, pondCenterY + 5f))
}

private fun DrawScope.drawStorageAndSilos(x: Float, y: Float, w: Float, h: Float) {
    // Storage Yard Pavement
    drawRoundRect(
        color = Color(0xFFCBD5E1),
        topLeft = Offset(x, y),
        size = Size(w, h),
        cornerRadius = CornerRadius(14f, 14f)
    )

    // Gray Warehouse Building with Corrugated Roof
    drawRoundRect(
        color = Color(0xFF475569),
        topLeft = Offset(x + w * 0.08f, y + h * 0.18f),
        size = Size(w * 0.48f, h * 0.65f),
        cornerRadius = CornerRadius(6f, 6f)
    )
    // Skylights
    drawRect(Color(0xFF94A3B8), Offset(x + w * 0.16f, y + h * 0.32f), Size(w * 0.12f, h * 0.22f))
    drawRect(Color(0xFF94A3B8), Offset(x + w * 0.34f, y + h * 0.32f), Size(w * 0.12f, h * 0.22f))

    // Two Cylindrical Metal Silos with Conical Tops
    val silo1X = x + w * 0.70f
    val silo1Y = y + h * 0.35f
    drawCircle(Color(0xFF94A3B8), 12f, Offset(silo1X, silo1Y))
    drawCircle(Color(0xFFE2E8F0), 8f, Offset(silo1X, silo1Y))

    val silo2X = x + w * 0.70f
    val silo2Y = y + h * 0.75f
    drawCircle(Color(0xFF94A3B8), 12f, Offset(silo2X, silo2Y))
    drawCircle(Color(0xFFE2E8F0), 8f, Offset(silo2X, silo2Y))
}
