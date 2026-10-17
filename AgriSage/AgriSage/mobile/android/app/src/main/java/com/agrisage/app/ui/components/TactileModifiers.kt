package com.agrisage.app.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.waitForUpOrCancellation
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.scale
import androidx.compose.ui.input.pointer.pointerInput
import kotlinx.coroutines.launch

/**
 * Hardware-accelerated tactile press animation modifier.
 * Implements 1:1 micro-spring scale physics (scale 0.96 on press, snappy bounce-back on release).
 */
fun Modifier.tactilePress(
    scaleDown: Float = 0.96f,
    onClick: (() -> Unit)? = null
): Modifier = composed {
    val scale = remember { Animatable(1f) }
    val scope = rememberCoroutineScope()

    this
        .scale(scale.value)
        .pointerInput(Unit) {
            while (true) {
                awaitPointerEventScope {
                    awaitFirstDown(requireUnconsumed = false)
                    scope.launch {
                        scale.animateTo(
                            targetValue = scaleDown,
                            animationSpec = tween(durationMillis = 100)
                        )
                    }
                    val up = waitForUpOrCancellation()
                    scope.launch {
                        scale.animateTo(
                            targetValue = 1f,
                            animationSpec = spring(
                                dampingRatio = Spring.DampingRatioMediumBouncy,
                                stiffness = Spring.StiffnessMediumLow
                            )
                        )
                    }
                    if (up != null && onClick != null) {
                        onClick()
                    }
                }
            }
        }
}
