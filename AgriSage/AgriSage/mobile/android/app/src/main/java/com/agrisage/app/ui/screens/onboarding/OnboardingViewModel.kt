package com.agrisage.app.ui.screens.onboarding

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
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
    val phone: String = "",
    val village: String = "",
    val district: String = "",
    val otp: String = "",
    val otpSent: Boolean = false,
    val notice: String? = null,
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

    fun updatePhone(phone: String) {
        _uiState.update { it.copy(phone = phone.filter(Char::isDigit).take(10)) }
    }

    fun updateVillage(village: String) {
        _uiState.update { it.copy(village = village) }
    }

    fun updateDistrict(district: String) {
        _uiState.update { it.copy(district = district) }
    }

    fun updateOtp(otp: String) {
        _uiState.update { it.copy(otp = otp.filter(Char::isDigit).take(6)) }
    }

    fun nextPage() {
        _uiState.update { it.copy(currentPage = (it.currentPage + 1).coerceAtMost(2)) }
    }

    fun previousPage() {
        _uiState.update { it.copy(currentPage = (it.currentPage - 1).coerceAtLeast(0)) }
    }

    fun completeOnboarding(onSuccess: () -> Unit) {
        val current = _uiState.value
        val phone = current.phone.trim()
        if (phone.length != 10) {
            _uiState.update { it.copy(error = "Enter a valid 10-digit mobile number.", notice = null) }
            return
        }
        if (current.otpSent && current.otp.length != 6) {
            _uiState.update { it.copy(error = "Enter the 6-digit verification code.", notice = null) }
            return
        }

        _uiState.update { it.copy(isLoading = true, error = null, notice = null) }
        viewModelScope.launch {
            try {
                val internationalPhone = "+91$phone"
                if (!current.otpSent) {
                    val response = authRepository.sendOtp(internationalPhone)
                    if (!response.isSuccessful) {
                        throw IllegalStateException("Could not send verification code (${response.code()}).")
                    }
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            otpSent = true,
                            notice = "Verification code sent. Enter it to finish setup."
                        )
                    }
                } else {
                    val response = authRepository.verifyOtp(
                        phone = internationalPhone,
                        otp = current.otp,
                        name = current.farmerName.trim().ifBlank { null },
                    )
                    if (!response.isSuccessful) {
                        throw IllegalStateException("Verification failed (${response.code()}).")
                    }
                    authRepository.persistOnboardingProfile(
                        name = current.farmerName.trim(),
                        phone = internationalPhone,
                        district = current.district.trim(),
                        language = current.selectedLanguage,
                    )
                    _uiState.update { it.copy(isLoading = false) }
                    onSuccess()
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isLoading = false, error = e.message ?: "Authentication could not be completed.") }
            }
        }
    }
}
