package com.agrisage.app.ui.components

import android.content.Context
import android.provider.Settings
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.snap
import androidx.compose.animation.core.spring
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.scale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.Role

/**
 * Shared press feedback for interactive cards and custom controls.
 *
 * The click action is provided by Compose's clickable modifier so the control
 * exposes an accessibility action and button role. Scale feedback is skipped
 * when Android's animator or transition scale is disabled (the system's
 * reduced-motion signal).
 */
fun Modifier.tactilePress(
    scaleDown: Float = 0.96f,
    onClickLabel: String? = null,
    onClick: (() -> Unit)? = null
): Modifier = composed {
    val context = LocalContext.current
    val reducedMotion = remember(context) { systemAnimationsDisabled(context) }
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()
    val targetScale = if (isPressed && !reducedMotion) scaleDown.coerceIn(0.9f, 1f) else 1f
    val animatedScale by animateFloatAsState(
        targetValue = targetScale,
        animationSpec = if (reducedMotion) {
            snap()
        } else {
            spring(
                dampingRatio = Spring.DampingRatioMediumBouncy,
                stiffness = Spring.StiffnessMediumLow
            )
        },
        label = "tactilePressScale"
    )

    this
        .scale(animatedScale)
        .then(
            if (onClick == null) {
                Modifier
            } else {
                Modifier.clickable(
                    interactionSource = interactionSource,
                    indication = null,
                    role = Role.Button,
                    onClickLabel = onClickLabel,
                    onClick = onClick
                )
            }
        )
}

private fun systemAnimationsDisabled(context: Context): Boolean {
    val resolver = context.contentResolver
    val animatorScale = Settings.Global.getFloat(
        resolver,
        Settings.Global.ANIMATOR_DURATION_SCALE,
        1f
    )
    val transitionScale = Settings.Global.getFloat(
        resolver,
        Settings.Global.TRANSITION_ANIMATION_SCALE,
        1f
    )
    return animatorScale <= 0f || transitionScale <= 0f
}
