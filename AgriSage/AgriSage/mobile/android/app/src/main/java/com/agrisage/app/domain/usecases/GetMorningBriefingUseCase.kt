package com.agrisage.app.domain.usecases

import javax.inject.Inject

class GetMorningBriefingUseCase @Inject constructor() {
    suspend operator fun invoke(farmerName: String, crop: String): Map<String, Any> {
        return mapOf(
            "headline" to "നമസ്കാരം $farmerName, ഇന്നത്തെ കാർഷിക വിവരങ്ങൾ ($crop)",
            "spray_window_open" to true,
            "temp_c" to 28.5,
            "humidity_pct" to 78,
            "wind_speed_kmh" to 8.5
        )
    }
}
