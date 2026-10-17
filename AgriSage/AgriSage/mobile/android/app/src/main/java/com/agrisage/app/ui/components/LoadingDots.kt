package com.agrisage.app.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.agrisage.app.ui.theme.SageDeep

/**
 * Animated three-dot loading indicator for AI response streaming states in AdvisorScreen.
 */
@Composable
fun LoadingDots(
    modifier: Modifier = Modifier,
    dotSize: Dp = 10.dp,
    dotColor: Color = SageDeep,
    delayUnit: Int = 300
) {
    val dots = listOf(
        rememberInfiniteTransition(label = "dot1").animateFloat(
            initialValue = 0.2f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 600, easing = LinearEasing),
                repeatMode = RepeatMode.Reverse
            ), label = "alpha1"
        ),
        rememberInfiniteTransition(label = "dot2").animateFloat(
            initialValue = 0.2f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 600, delayMillis = delayUnit, easing = LinearEasing),
                repeatMode = RepeatMode.Reverse
            ), label = "alpha2"
        ),
        rememberInfiniteTransition(label = "dot3").animateFloat(
            initialValue = 0.2f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 600, delayMillis = delayUnit * 2, easing = LinearEasing),
                repeatMode = RepeatMode.Reverse
            ), label = "alpha3"
        )
    )

    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        dots.forEach { alphaAnim ->
            val alpha by alphaAnim
            Box(
                modifier = Modifier
                    .size(dotSize)
                    .clip(CircleShape)
                    .background(dotColor.copy(alpha = alpha))
            )
        }
    }
}
