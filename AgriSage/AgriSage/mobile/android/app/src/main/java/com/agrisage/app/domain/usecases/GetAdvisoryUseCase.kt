package com.agrisage.app.domain.usecases

import com.agrisage.app.ml.OfflineAdvisoryEngine
import javax.inject.Inject

class GetAdvisoryUseCase @Inject constructor(
    private val offlineEngine: OfflineAdvisoryEngine
) {
    suspend operator fun invoke(crop: String, label: String, confidence: Float): Map<String, Any> {
        val result = offlineEngine.generateAdvisory(label, confidence)
        return mapOf(
            "crop" to crop,
            "disease_name" to (result["disease_name"] ?: label),
            "confidence_state" to (result["confidence_state"] ?: "LIKELY"),
            "recommended_action" to (result["recommended_action"] ?: ""),
            "treatment_cost_inr" to 600.0,
            "statutory_disclaimer" to "* Modelled estimate"
        )
    }
}
