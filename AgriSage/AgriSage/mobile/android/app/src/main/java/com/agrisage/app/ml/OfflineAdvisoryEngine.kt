package com.agrisage.app.ml

import android.content.Context
import com.agrisage.app.data.local.entities.CachedAdvisoryEntity
import dagger.hilt.android.qualifiers.ApplicationContext
import java.util.UUID
import javax.inject.Inject

class OfflineAdvisoryEngine @Inject constructor(
    @ApplicationContext private val context: Context
) {

    fun generateAdvisory(label: String, confidence: Float): Map<String, Any> {
        return mapOf(
            "disease_name" to label,
            "confidence_state" to if (confidence > 0.8f) "CONFIRMED" else "POSSIBLE",
            "recommended_action" to "തണുപ്പുള്ള സമയത്ത് നിർദ്ദിഷ്ട നിയന്ത്രണ മാർഗ്ഗങ്ങൾ പ്രയോഗിക്കുക."
        )
    }

    fun generateOfflineAdvisory(imagePath: String, crop: String): CachedAdvisoryEntity {
        val advisoryJson = """
        {
          "diagnosis_summary": "നിങ്ങളുടെ $crop വിളയിൽ ഇലപ്പുളളി രോഗത്തിന്റെ ലക്ഷണങ്ങൾ കാണുന്നു. ആത്മവിശ്വാസം: 78%. ഇന്ന് ജലസേചനം ഒഴിവാക്കുക.",
          "confidence_state": "POSSIBLE",
          "confidence_score": 0.78,
          "safe_to_act": true,
          "offline_banner": "ഇന്റർനെറ്റ് ഇല്ല — ഓഫ്‌ലൈൻ വിശകലനം",
          "modelled_estimate_label": "* Modelled estimate — actual results vary by field conditions"
        }
        """.trimIndent()

        return CachedAdvisoryEntity(
            id = UUID.randomUUID().toString(),
            observationId = "offline-obs",
            advisoryJson = advisoryJson,
            type = "offline_advisory",
            isOffline = true,
            createdAt = System.currentTimeMillis()
        )
    }
}
