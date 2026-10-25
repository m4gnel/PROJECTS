package com.agrisage.app.ui.screens.fields

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.local.entity.FieldEntity
import com.agrisage.app.data.repository.FieldRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class FieldDetailUiState(
    val field: FieldModel? = null,
    val isLoading: Boolean = true,
    val error: String? = null,
)

@HiltViewModel
class FieldDetailViewModel @Inject constructor(
    private val fieldRepository: FieldRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(FieldDetailUiState())
    val uiState: StateFlow<FieldDetailUiState> = _uiState.asStateFlow()

    fun load(fieldId: String) {
        if (BuildConfig.REFERENCE_PREVIEW) {
            _uiState.value = FieldDetailUiState(field = debugPreview(fieldId), isLoading = false)
            return
        }
        if (!_uiState.value.isLoading && _uiState.value.field?.id == fieldId) return

        viewModelScope.launch {
            _uiState.value = FieldDetailUiState(isLoading = true)
            fieldRepository.getFieldById(fieldId)
                .catch { error ->
                    _uiState.value = FieldDetailUiState(
                        field = debugPreview(fieldId),
                        isLoading = false,
                        error = error.message ?: "Field details are unavailable.",
                    )
                }
                .collect { entity ->
                    val field = entity?.toFieldModel() ?: debugPreview(fieldId)
                    _uiState.value = FieldDetailUiState(
                        field = field,
                        isLoading = false,
                        error = if (field == null) "Field details are unavailable." else null,
                    )
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
        lastNdvi = lastNdvi.takeIf { it > 0f },
    )

    private fun debugPreview(fieldId: String): FieldModel? {
        if (!BuildConfig.REFERENCE_PREVIEW) return null
        return when (fieldId) {
            "reference-north-paddy" -> FieldModel(
                id = fieldId,
                name = "North Paddy Field",
                areaSqM = 2.5f * 4046.86f,
                cropName = "Paddy",
                cropVariety = "Jyothi",
                sowingDate = "2026-07-15",
                healthStatus = "good",
                latitude = 10.165,
                longitude = 76.401,
                lastNdvi = 0.78f,
            )
            "reference-coconut-grove" -> FieldModel(
                id = fieldId,
                name = "Coconut & Fruit Grove",
                areaSqM = 1.2f * 4046.86f,
                cropName = "Coconut & fruit",
                cropVariety = "Mixed perennial",
                sowingDate = "2024-06-01",
                healthStatus = "warning",
                latitude = 10.167,
                longitude = 76.399,
                lastNdvi = 0.68f,
            )
            else -> null
        }
    }
}
