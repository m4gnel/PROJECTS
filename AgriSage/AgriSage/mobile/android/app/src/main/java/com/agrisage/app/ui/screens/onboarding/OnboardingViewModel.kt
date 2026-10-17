package com.agrisage.app.ui.screens.onboarding

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.remote.dto.RegisterRequest
import com.agrisage.app.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class OnboardingUiState(
    val currentPage: Int = 0,        // 0, 1, 2
    val selectedLanguage: String = "ml",  // "ml", "en", "ta", "hi"
    val farmerName: String = "",
    val village: String = "",
    val district: String = "",
    val isLoading: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class OnboardingViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val dataStore: DataStore<Preferences>
) : ViewModel() {

    private val _uiState = MutableStateFlow(OnboardingUiState())
    val uiState: StateFlow<OnboardingUiState> = _uiState.asStateFlow()

    fun selectLanguage(lang: String) {
        _uiState.update { it.copy(selectedLanguage = lang) }
        viewModelScope.launch {
            authRepository.setLanguage(lang)
        }
    }

    fun updateName(name: String) {
        _uiState.update { it.copy(farmerName = name) }
    }

    fun updateVillage(village: String) {
        _uiState.update { it.copy(village = village) }
    }

    fun updateDistrict(district: String) {
        _uiState.update { it.copy(district = district) }
    }

    fun nextPage() {
        _uiState.update { it.copy(currentPage = (it.currentPage + 1).coerceAtMost(2)) }
    }

    fun previousPage() {
        _uiState.update { it.copy(currentPage = (it.currentPage - 1).coerceAtLeast(0)) }
    }

    fun completeOnboarding(onSuccess: () -> Unit) {
        val current = _uiState.value
        _uiState.update { it.copy(isLoading = true, error = null) }
        viewModelScope.launch {
            try {
                // Register default or provided details
                val phone = "9847" + (100000..999999).random()
                val request = RegisterRequest(
                    phone = phone,
                    name = current.farmerName.ifBlank { "Kerala Farmer" },
                    password = "farmer_pass_123",
                    village = current.village.ifBlank { "Kalady" },
                    district = current.district.ifBlank { "Ernakulam" },
                    preferredLanguage = current.selectedLanguage,
                    latitude = 10.1632,
                    longitude = 76.3986
                )
                authRepository.register(request)
                _uiState.update { it.copy(isLoading = false) }
                onSuccess()
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.message) }
                onSuccess() // Allow navigation even on offline fallback
            }
        }
    }
}
