package com.agrisage.app.util

/**
 * India-wide fallback used only before the farmer grants location access.
 * Device coordinates and the farmer's selected location always take priority.
 */
object LocationDefaults {
    const val latitude = 22.5937
    const val longitude = 78.9629
    const val state = "India"
}
