package com.agrisage.app.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import kotlin.math.cos
import kotlin.math.sin

enum class WeatherVisualMode {
    SUNNY, PARTLY_CLOUDY, WINDY, RAINY, RAINBOW
}

/**
 * High-fidelity Illustrated Farm Scene replicated from reference reels (DailyFlutterUI).
 * Renders an animated landscape featuring:
 * - Rolling green pastures & layered hills
 * - Radiant sun with soft atmospheric glow
 * - 7-layer vibrant rainbow arc
 * - Iconic red barn with white X-doors & silver grain silo
 * - Grazing Holstein dairy cows
 * - Tilled soil agricultural field furrows with crop sprouts
 * - Spinning wind turbines
 * - Irrigation pond with reflective water highlights
 */
@Composable
fun FarmIllustration(
    modifier: Modifier = Modifier.fillMaxWidth().height(220.dp),
    weatherMode: WeatherVisualMode = WeatherVisualMode.RAINBOW,
    isAnimated: Boolean = true
) {
    val infiniteTransition = rememberInfiniteTransition(label = "farm_animation")

    // Turbine rotation angle
    val turbineAngle by if (isAnimated) {
        infiniteTransition.animateFloat(
            initialValue = 0f,
            targetValue = 360f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 4000, easing = LinearEasing),
                repeatMode = RepeatMode.Restart
            ),
            label = "turbine_spin"
        )
    } else {
        remember { mutableFloatStateOf(0f) }
    }

    // Gentle sun pulse
    val sunPulse by if (isAnimated) {
        infiniteTransition.animateFloat(
            initialValue = 0.95f,
            targetValue = 1.05f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 2400, easing = FastOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ),
            label = "sun_pulse"
        )
    } else {
        remember { mutableFloatStateOf(1f) }
    }

    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height

        // 1. Sky Gradient
        val skyColors = when (weatherMode) {
            WeatherVisualMode.RAINY -> listOf(Color(0xFF64748B), Color(0xFF94A3B8), Color(0xFFCBD5E1))
            WeatherVisualMode.WINDY -> listOf(Color(0xFF7DD3FC), Color(0xFFBAE6FD), Color(0xFFE2E8F0))
            else -> listOf(Color(0xFF38BDF8), Color(0xFF7DD3FC), Color(0xFFE0F2FE))
        }
        drawRect(
            brush = Brush.verticalGradient(skyColors, startY = 0f, endY = h * 0.75f)
        )

        // 2. Radiant Sun
        val sunCenter = Offset(w * 0.38f, h * 0.28f)
        val sunRadius = 26.dp.toPx() * sunPulse

        // Sun halo / glow
        drawCircle(
            color = Color(0xFFFDE047).copy(alpha = 0.25f),
            radius = sunRadius * 1.8f,
            center = sunCenter
        )
        drawCircle(
            color = Color(0xFFFBBF24).copy(alpha = 0.45f),
            radius = sunRadius * 1.35f,
            center = sunCenter
        )
        drawCircle(
            brush = Brush.radialGradient(
                colors = listOf(Color(0xFFFFFBEB), Color(0xFFFDE047), Color(0xFFF59E0B)),
                center = sunCenter,
                radius = sunRadius
            ),
            radius = sunRadius,
            center = sunCenter
        )

        // 3. Vibrant 7-Layer Rainbow Arc (active during RAINBOW or default mode)
        if (weatherMode == WeatherVisualMode.RAINBOW || weatherMode == WeatherVisualMode.PARTLY_CLOUDY) {
            val rainbowCenter = Offset(w * 0.58f, h * 0.95f)
            val rainbowColors = listOf(
                Color(0xFFEF4444).copy(alpha = 0.45f), // Red
                Color(0xFFF97316).copy(alpha = 0.45f), // Orange
                Color(0xFFFBBF24).copy(alpha = 0.50f), // Yellow
                Color(0xFF22C55E).copy(alpha = 0.45f), // Green
                Color(0xFF06B6D4).copy(alpha = 0.45f), // Cyan
                Color(0xFF3B82F6).copy(alpha = 0.45f), // Blue
                Color(0xFF8B5CF6).copy(alpha = 0.40f)  // Violet
            )
            val baseRadius = w * 0.46f
            val arcThickness = 3.5.dp.toPx()

            rainbowColors.forEachIndexed { i, color ->
                drawArc(
                    color = color,
                    startAngle = 175f,
                    sweepAngle = 105f,
                    useCenter = false,
                    topLeft = Offset(rainbowCenter.x - baseRadius + (i * arcThickness), rainbowCenter.y - baseRadius + (i * arcThickness)),
                    size = Size((baseRadius - (i * arcThickness)) * 2, (baseRadius - (i * arcThickness)) * 2),
                    style = Stroke(width = arcThickness)
                )
            }
        }

        // 4. Soft Clouds
        drawCloud(Offset(w * 0.18f, h * 0.22f), scale = 1.0f)
        drawCloud(Offset(w * 0.76f, h * 0.26f), scale = 1.15f)
        drawCloud(Offset(w * 0.48f, h * 0.18f), scale = 0.85f)

        // 5. Distant Wind Turbines
        drawWindTurbine(Offset(w * 0.14f, h * 0.38f), heightPx = 48.dp.toPx(), angle = turbineAngle)
        drawWindTurbine(Offset(w * 0.22f, h * 0.42f), heightPx = 36.dp.toPx(), angle = -turbineAngle * 1.2f)
        drawWindTurbine(Offset(w * 0.88f, h * 0.40f), heightPx = 42.dp.toPx(), angle = turbineAngle * 0.9f)

        // 6. Layered Green Hills (Background & Midground)
        // Far Hill (Dark Pine)
        val farHillPath = Path().apply {
            moveTo(0f, h * 0.54f)
            cubicTo(w * 0.25f, h * 0.42f, w * 0.55f, h * 0.58f, w, h * 0.48f)
            lineTo(w, h)
            lineTo(0f, h)
            close()
        }
        drawPath(farHillPath, color = Color(0xFF2D6A4F))

        // Mid Hill (Medium Green)
        val midHillPath = Path().apply {
            moveTo(0f, h * 0.62f)
            cubicTo(w * 0.35f, h * 0.68f, w * 0.65f, h * 0.50f, w, h * 0.58f)
            lineTo(w, h)
            lineTo(0f, h)
            close()
        }
        drawPath(midHillPath, color = Color(0xFF40916C))

        // 7. Iconic Red Barn & Silo (Right-Center)
        val barnX = w * 0.62f
        val barnY = h * 0.46f
        val barnW = 46.dp.toPx()
        val barnH = 34.dp.toPx()

        // Silver Silo
        val siloX = barnX + barnW + 2.dp.toPx()
        val siloW = 12.dp.toPx()
        val siloH = 38.dp.toPx()
        // Silo body
        drawRect(color = Color(0xFFCBD5E1), topLeft = Offset(siloX, barnY - 6.dp.toPx()), size = Size(siloW, siloH))
        // Silo dome
        drawArc(
            color = Color(0xFF94A3B8),
            startAngle = 180f,
            sweepAngle = 180f,
            useCenter = true,
            topLeft = Offset(siloX, barnY - 12.dp.toPx()),
            size = Size(siloW, 12.dp.toPx())
        )

        // Barn Body
        drawRect(
            color = Color(0xFFB91C1C),
            topLeft = Offset(barnX, barnY + 8.dp.toPx()),
            size = Size(barnW, barnH - 8.dp.toPx())
        )
        // Barn Gambrel Roof
        val roofPath = Path().apply {
            moveTo(barnX - 3.dp.toPx(), barnY + 8.dp.toPx())
            lineTo(barnX + barnW * 0.2f, barnY)
            lineTo(barnX + barnW * 0.8f, barnY)
            lineTo(barnX + barnW + 3.dp.toPx(), barnY + 8.dp.toPx())
            close()
        }
        drawPath(roofPath, color = Color(0xFF991B1B))
        // Barn white roof trim line
        drawPath(roofPath, color = Color.White, style = Stroke(width = 1.2.dp.toPx()))

        // Barn White Door with 'X'
        val doorW = 14.dp.toPx()
        val doorH = 16.dp.toPx()
        val doorX = barnX + (barnW - doorW) / 2
        val doorY = barnY + barnH - doorH
        drawRect(color = Color.White, topLeft = Offset(doorX, doorY), size = Size(doorW, doorH), style = Stroke(1.5.dp.toPx()))
        drawLine(Color.White, Offset(doorX, doorY), Offset(doorX + doorW, doorY + doorH), strokeWidth = 1.5.dp.toPx())
        drawLine(Color.White, Offset(doorX, doorY + doorH), Offset(doorX + doorW, doorY), strokeWidth = 1.5.dp.toPx())

        // 8. Foreground Lush Pasture Hill
        val foreHillPath = Path().apply {
            moveTo(0f, h * 0.68f)
            cubicTo(w * 0.30f, h * 0.58f, w * 0.70f, h * 0.72f, w, h * 0.66f)
            lineTo(w, h)
            lineTo(0f, h)
            close()
        }
        drawPath(foreHillPath, color = Color(0xFF52B788))

        // 9. Irrigation Pond (Lower Left)
        val pondCenter = Offset(w * 0.20f, h * 0.82f)
        drawOval(
            brush = Brush.radialGradient(
                colors = listOf(Color(0xFF67E8F9), Color(0xFF0284C7)),
                center = pondCenter,
                radius = 42.dp.toPx()
            ),
            topLeft = Offset(w * 0.08f, h * 0.76f),
            size = Size(74.dp.toPx(), 32.dp.toPx())
        )
        // Water ripples
        drawArc(
            color = Color.White.copy(alpha = 0.6f),
            startAngle = 200f,
            sweepAngle = 120f,
            useCenter = false,
            topLeft = Offset(w * 0.12f, h * 0.79f),
            size = Size(36.dp.toPx(), 12.dp.toPx()),
            style = Stroke(1.5.dp.toPx())
        )

        // 10. Tilled Crop Furrows (Bottom Center & Right)
        val cropFieldPath = Path().apply {
            moveTo(w * 0.38f, h * 0.76f)
            lineTo(w * 0.96f, h * 0.72f)
            lineTo(w * 0.98f, h)
            lineTo(w * 0.32f, h)
            close()
        }
        drawPath(cropFieldPath, color = Color(0xFF78350F))

        // Furrow lines with crop seedlings
        for (f in 0..4) {
            val startY = h * 0.80f + (f * 10.dp.toPx())
            val furrowPath = Path().apply {
                moveTo(w * 0.36f + (f * 4.dp.toPx()), startY)
                quadraticTo(w * 0.65f, startY - 4.dp.toPx(), w * 0.95f, startY + 2.dp.toPx())
            }
            drawPath(furrowPath, color = Color(0xFF92400E), style = Stroke(2.5.dp.toPx()))

            // Crop sprouts along each furrow
            for (p in 0..6) {
                val plantX = w * (0.42f + (p * 0.08f))
                val plantY = startY - 2.dp.toPx()
                drawCircle(color = Color(0xFF4ADE80), radius = 2.dp.toPx(), center = Offset(plantX, plantY))
                drawCircle(color = Color(0xFF22C55E), radius = 1.3.dp.toPx(), center = Offset(plantX + 2.dp.toPx(), plantY - 2.dp.toPx()))
            }
        }

        // 11. Grazing Dairy Cows (Holstein Black & White)
        drawCow(Offset(w * 0.16f, h * 0.68f), scale = 0.95f)
        drawCow(Offset(w * 0.28f, h * 0.70f), scale = 0.85f)

        // 12. Soft Pine Trees on Hills
        drawPineTree(Offset(w * 0.06f, h * 0.62f), size = 18.dp.toPx())
        drawPineTree(Offset(w * 0.10f, h * 0.60f), size = 22.dp.toPx())
        drawPineTree(Offset(w * 0.54f, h * 0.56f), size = 16.dp.toPx())
        drawPineTree(Offset(w * 0.84f, h * 0.60f), size = 20.dp.toPx())

        // 13. Farmer Character in Straw Hat (Signature Reel 2 Foreground Element)
        drawFarmer(Offset(w * 0.86f, h * 0.56f), scale = 1.15f)
    }
}

private fun DrawScope.drawCloud(center: Offset, scale: Float) {
    val r = 14.dp.toPx() * scale
    val color = Color.White.copy(alpha = 0.92f)
    drawCircle(color, r, center)
    drawCircle(color, r * 1.35f, center + Offset(r * 0.9f, -r * 0.25f))
    drawCircle(color, r * 1.1f, center + Offset(r * 1.8f, 0f))
    drawCircle(color, r * 0.45f, center + Offset(r * 0.45f, r * 0.4f))
    drawCircle(color, r * 0.45f, center + Offset(r * 1.35f, r * 0.4f))
}

private fun DrawScope.drawWindTurbine(base: Offset, heightPx: Float, angle: Float) {
    val poleColor = Color.White.copy(alpha = 0.92f)
    val top = base - Offset(0f, heightPx)

    // Tower pole
    drawLine(poleColor, base, top, strokeWidth = 2.dp.toPx())
    // Center rotor hub
    drawCircle(Color(0xFFE2E8F0), 2.5.dp.toPx(), top)

    // 3 Rotor blades
    val bladeLength = heightPx * 0.45f
    for (i in 0..2) {
        val rad = Math.toRadians((angle + (i * 120)).toDouble())
        val bladeTip = Offset(
            top.x + (bladeLength * cos(rad)).toFloat(),
            top.y + (bladeLength * sin(rad)).toFloat()
        )
        drawLine(poleColor, top, bladeTip, strokeWidth = 1.4.dp.toPx())
    }
}

private fun DrawScope.drawCow(origin: Offset, scale: Float) {
    val cowW = 20.dp.toPx() * scale
    val cowH = 12.dp.toPx() * scale

    // Cow White Body
    drawRoundRect(
        color = Color.White,
        topLeft = origin,
        size = Size(cowW, cowH),
        cornerRadius = androidx.compose.ui.geometry.CornerRadius(4.dp.toPx(), 4.dp.toPx())
    )
    // Black patches
    drawCircle(Color(0xFF1E293B), cowH * 0.32f, origin + Offset(cowW * 0.35f, cowH * 0.35f))
    drawCircle(Color(0xFF1E293B), cowH * 0.28f, origin + Offset(cowW * 0.70f, cowH * 0.55f))

    // Head
    val headR = cowH * 0.38f
    val headCenter = origin + Offset(-headR * 0.6f, cowH * 0.2f)
    drawCircle(Color.White, headR, headCenter)
    drawCircle(Color(0xFF1E293B), headR * 0.5f, headCenter - Offset(headR * 0.3f, headR * 0.2f))
    // Pink snout
    drawOval(
        color = Color(0xFFFBCFE8),
        topLeft = headCenter + Offset(-headR * 0.9f, 0f),
        size = Size(headR * 0.8f, headR * 0.7f)
    )

    // 4 Legs
    val legW = 2.dp.toPx() * scale
    val legH = 6.dp.toPx() * scale
    val legY = origin.y + cowH
    val x1 = origin.x + (2.dp.toPx() * scale)
    val x2 = origin.x + (6.dp.toPx() * scale)
    val x3 = origin.x + cowW - (7.dp.toPx() * scale)
    val x4 = origin.x + cowW - (3.dp.toPx() * scale)
    drawRect(Color.White, Offset(x1, legY), Size(legW, legH))
    drawRect(Color.White, Offset(x2, legY), Size(legW, legH))
    drawRect(Color.White, Offset(x3, legY), Size(legW, legH))
    drawRect(Color.White, Offset(x4, legY), Size(legW, legH))
}

private fun DrawScope.drawPineTree(base: Offset, size: Float) {
    // Trunk
    val trunkW = size * 0.15f
    val trunkH = size * 0.35f
    drawRect(Color(0xFF78350F), Offset(base.x - trunkW / 2, base.y - trunkH), Size(trunkW, trunkH))

    // Foliage
    val foliagePath = Path().apply {
        moveTo(base.x, base.y - size)
        lineTo(base.x + size * 0.45f, base.y - trunkH)
        lineTo(base.x - size * 0.45f, base.y - trunkH)
        close()
    }
    drawPath(foliagePath, color = Color(0xFF1B4332))
}

private fun DrawScope.drawFarmer(base: Offset, scale: Float) {
    // Body / Orange farmer shirt
    val bodyW = 32.dp.toPx() * scale
    val bodyH = 28.dp.toPx() * scale
    val bodyPath = Path().apply {
        moveTo(base.x - bodyW * 0.5f, base.y + bodyH)
        lineTo(base.x - bodyW * 0.30f, base.y + 6.dp.toPx() * scale)
        lineTo(base.x + bodyW * 0.30f, base.y + 6.dp.toPx() * scale)
        lineTo(base.x + bodyW * 0.5f, base.y + bodyH)
        close()
    }
    drawPath(bodyPath, color = Color(0xFFEA580C))

    // Neck
    drawRect(
        color = Color(0xFF78350F),
        topLeft = Offset(base.x - 3.dp.toPx() * scale, base.y),
        size = Size(6.dp.toPx() * scale, 8.dp.toPx() * scale)
    )

    // Wide Straw Conical Hat (Signature from Reel 2)
    val hatW = 42.dp.toPx() * scale
    val hatH = 18.dp.toPx() * scale
    val hatPath = Path().apply {
        moveTo(base.x, base.y - hatH)
        lineTo(base.x + hatW * 0.5f, base.y + 2.dp.toPx() * scale)
        lineTo(base.x - hatW * 0.5f, base.y + 2.dp.toPx() * scale)
        close()
    }
    drawPath(hatPath, color = Color(0xFFD97706))
    // Hat brim outline & cone crease
    drawPath(hatPath, color = Color(0xFFB45309), style = Stroke(1.2.dp.toPx() * scale))
    drawLine(Color(0xFF92400E), Offset(base.x, base.y - hatH), Offset(base.x, base.y + 2.dp.toPx() * scale), strokeWidth = 1.dp.toPx() * scale)
}
