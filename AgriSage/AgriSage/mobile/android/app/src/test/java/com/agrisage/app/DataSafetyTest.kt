package com.agrisage.app

import com.agrisage.app.data.remote.dto.SyncUploadResponse
import com.agrisage.app.ui.screens.fields.validatePlotInput
import com.agrisage.app.ui.screens.fields.isReferencePlot
import com.agrisage.app.ui.screens.home.homeReferencePreviewData
import com.google.gson.Gson
import org.junit.Assert.*
import org.junit.Test

class DataSafetyTest {
    @Test
    fun normalDebugDoesNotSubstituteReferenceData() {
        assertFalse(BuildConfig.REFERENCE_PREVIEW)
        assertNull(homeReferencePreviewData)
        assertFalse(isReferencePlot("reference-north-paddy"))
        assertFalse(isReferencePlot("reference-coconut-grove"))
    }

    @Test
    fun anUploadCountIsNotProofOfPersistence() {
        val receipt = Gson().fromJson(
            """{"status":"success","processed_count":1}""",
            SyncUploadResponse::class.java,
        )
        assertFalse(receipt.confirmsPersistedObservation("observation-1"))
    }

    @Test
    fun onlyAnExactDurableAcknowledgementCanRemoveALocalObservation() {
        assertTrue(SyncUploadResponse("success", 1, listOf("observation-1"))
            .confirmsPersistedObservation("observation-1"))
        listOf(
            SyncUploadResponse(),
            SyncUploadResponse("success", 0, listOf("observation-1")),
            SyncUploadResponse("failed", 1, listOf("observation-1")),
            SyncUploadResponse("success", 1, listOf("another-observation")),
            SyncUploadResponse("success", 1, listOf("observation-1", "another")),
        ).forEach { assertFalse(it.confirmsPersistedObservation("observation-1")) }
        assertFalse(SyncUploadResponse("success", 1, listOf("")).confirmsPersistedObservation(""))
    }

    @Test
    fun invalidPlotAreaAndCoordinatesAreRejectedBeforeSubmission() {
        assertNull(validatePlotInput("My plot", 100f, 0.0, 0.0))
        assertNotNull(validatePlotInput(" ", 100f, 0.0, 0.0))
        listOf(Float.NaN, Float.POSITIVE_INFINITY, 0f, -1f).forEach {
            assertNotNull(validatePlotInput("My plot", it, 0.0, 0.0))
        }
        listOf(Double.NaN, Double.POSITIVE_INFINITY, -90.1, 90.1).forEach {
            assertNotNull(validatePlotInput("My plot", 100f, it, 0.0))
        }
        listOf(Double.NaN, Double.NEGATIVE_INFINITY, -180.1, 180.1).forEach {
            assertNotNull(validatePlotInput("My plot", 100f, 0.0, it))
        }
    }
}
