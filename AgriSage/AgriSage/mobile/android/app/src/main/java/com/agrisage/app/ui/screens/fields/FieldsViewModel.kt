package com.agrisage.app.ui.screens.fields

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.local.entity.FieldEntity
import com.agrisage.app.data.remote.dto.CreateFieldRequest
import com.agrisage.app.data.repository.FieldRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class FieldModel(
    val id: String,
    val name: String,
    val areaSqM: Float,
    val cropName: String,
    val cropVariety: String,
    val sowingDate: String,
    val healthStatus: String,  // "good", "warning", "critical"
    val latitude: Double,
    val longitude: Double,
    val lastNdvi: Float? = null
)

data class FieldsUiState(
    val fields: List<FieldModel> = emptyList(),
    val isLoading: Boolean = false,
    val showAddDialog: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class FieldsViewModel @Inject constructor(
    private val fieldRepository: FieldRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(FieldsUiState())
    val uiState: StateFlow<FieldsUiState> = _uiState.asStateFlow()

    init {
        if (!BuildConfig.REFERENCE_PREVIEW) {
            observeLocalFields()
            loadFields()
        }
    }

    private fun observeLocalFields() {
        viewModelScope.launch {
            fieldRepository.getLocalFields()
                .catch { error ->
                    _uiState.update {
                        it.copy(error = error.message ?: "Field data is unavailable right now.")
                    }
                }
                .collect { entities ->
                    _uiState.update { current ->
                        current.copy(fields = entities.map { entity -> entity.toFieldModel() })
                    }
                }
        }
    }

    fun loadFields() {
        if (BuildConfig.REFERENCE_PREVIEW || _uiState.value.isLoading) return
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val response = fieldRepository.refreshFields()
                if (!response.isSuccessful) {
                    _uiState.update { it.copy(error = "Field data is unavailable right now.") }
                }
            } catch (error: Exception) {
                _uiState.update {
                    it.copy(error = error.message ?: "Field data is unavailable right now.")
                }
            } finally {
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }

    fun showAddDialog() {
        _uiState.update {
            it.copy(showAddDialog = true, error = if (BuildConfig.REFERENCE_PREVIEW) {
                "Reference preview is read-only. Use the normal app to register a real plot."
            } else null)
        }
    }

    fun hideAddDialog() {
        _uiState.update { it.copy(showAddDialog = false) }
    }

    fun addField(name: String, areaSqM: Float, lat: Double, lon: Double) {
        if (BuildConfig.REFERENCE_PREVIEW || _uiState.value.isLoading) return
        validatePlotInput(name, areaSqM, lat, lon)?.let { error ->
            _uiState.update { it.copy(error = error) }
            return
        }
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val response = fieldRepository.addField(
                    CreateFieldRequest(
                        name = name,
                        areaSqM = areaSqM,
                        latitude = lat,
                        longitude = lon,
                        cropName = null
                    )
                )
                if (response.isSuccessful && response.body() != null) {
                    hideAddDialog()
                } else {
                    _uiState.update { it.copy(error = "The field could not be added.") }
                }
            } catch (error: Exception) {
                _uiState.update {
                    it.copy(error = error.message ?: "The field could not be added.")
                }
            } finally {
                _uiState.update { it.copy(isLoading = false) }
            }
        }
    }

    fun deleteField(fieldId: String) {
        if (BuildConfig.REFERENCE_PREVIEW) return
        viewModelScope.launch {
            try {
                val response = fieldRepository.deleteField(fieldId)
                if (!response.isSuccessful) {
                    _uiState.update { it.copy(error = "The field could not be deleted.") }
                } else {
                    _uiState.update { current ->
                        current.copy(fields = current.fields.filter { it.id != fieldId })
                    }
                }
            } catch (error: Exception) {
                _uiState.update {
                    it.copy(error = error.message ?: "The field could not be deleted.")
                }
            }
        }
    }

    private fun FieldEntity.toFieldModel(): FieldModel = FieldModel(
        id = id,
        name = name,
        areaSqM = areaSqM,
        cropName = cropName,
        cropVariety = cropVariety,
        sowingDate = sowingDate,
        healthStatus = "",
        latitude = latitude,
        longitude = longitude,
        lastNdvi = lastNdvi.takeIf { it > 0f }
    )
}

internal fun validatePlotInput(name: String, areaSqM: Float, lat: Double, lon: Double): String? = when {
    name.isBlank() -> "Enter a plot name"
    !areaSqM.isFinite() || areaSqM <= 0f -> "Enter a valid positive area"
    !lat.isFinite() || lat !in -90.0..90.0 -> "Enter the plot's latitude between −90 and 90"
    !lon.isFinite() || lon !in -180.0..180.0 -> "Enter the plot's longitude between −180 and 180"
    else -> null
}

internal fun isReferencePlot(plotId: String): Boolean =
    BuildConfig.REFERENCE_PREVIEW && (plotId == "reference-north-paddy" || plotId == "reference-coconut-grove")
