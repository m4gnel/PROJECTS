package com.agrisage.app.ui.screens.fields

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.remote.dto.CreateFieldRequest
import com.agrisage.app.data.repository.FieldRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
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

    private val _uiState = MutableStateFlow(
        FieldsUiState(
            fields = listOf(
                FieldModel("f1", "South Paddy Field", 5000f, "Rice", "Jyothi", "2026-07-15", "good", 10.165, 76.401, 0.65f),
                FieldModel("f2", "North Coconut Grove", 2000f, "Coconut", "D×T Hybrid", "2024-06-01", "warning", 10.167, 76.399, 0.52f)
            )
        )
    )
    val uiState: StateFlow<FieldsUiState> = _uiState.asStateFlow()

    init {
        loadFields()
    }

    fun loadFields() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                fieldRepository.refreshFields()
            } catch (_: Exception) {}
            _uiState.update { it.copy(isLoading = false) }
        }
    }

    fun showAddDialog() {
        _uiState.update { it.copy(showAddDialog = true) }
    }

    fun hideAddDialog() {
        _uiState.update { it.copy(showAddDialog = false) }
    }

    fun addField(name: String, areaSqM: Float, lat: Double, lon: Double) {
        viewModelScope.launch {
            try {
                fieldRepository.addField(
                    CreateFieldRequest(
                        name = name,
                        areaSqM = areaSqM,
                        latitude = lat,
                        longitude = lon,
                        cropName = "Rice"
                    )
                )
            } catch (_: Exception) {}
            hideAddDialog()
            loadFields()
        }
    }

    fun deleteField(fieldId: String) {
        viewModelScope.launch {
            try {
                fieldRepository.deleteField(fieldId)
            } catch (_: Exception) {}
            _uiState.update { current ->
                current.copy(fields = current.fields.filter { it.id != fieldId })
            }
        }
    }
}
