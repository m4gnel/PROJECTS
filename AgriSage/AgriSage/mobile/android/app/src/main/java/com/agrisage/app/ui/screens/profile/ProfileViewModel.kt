package com.agrisage.app.ui.screens.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.remote.dto.FarmerDto
import com.agrisage.app.data.remote.dto.UpdateFarmerRequest
import com.agrisage.app.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class FarmerProfile(
    val id: String,
    val name: String,
    val phone: String,
    val village: String,
    val district: String,
    val totalFieldsSqM: Float,
    val primaryCrop: String,
    val preferredLanguage: String
)

data class ProfileUiState(
    val profile: FarmerProfile? = null,
    val isEditing: Boolean = false,
    val selectedLanguage: String = "ml",
    val isLoading: Boolean = false,
    val isSaving: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    init {
        if (!BuildConfig.REFERENCE_PREVIEW) {
            viewModelScope.launch {
                authRepository.selectedLanguage.collect { language ->
                    _uiState.update { it.copy(selectedLanguage = language) }
                }
            }
            loadProfile()
        }
    }

    fun loadProfile() {
        if (BuildConfig.REFERENCE_PREVIEW || _uiState.value.isLoading || _uiState.value.isSaving) return
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val response = runCatching { authRepository.getProfile() }.getOrNull()
            val profile = response?.takeIf { it.isSuccessful }?.body()?.toProfile()
            _uiState.update {
                it.copy(
                    profile = profile ?: it.profile,
                    isLoading = false,
                    error = when {
                        profile != null -> null
                        response == null -> "Profile provider is unavailable."
                        !response.isSuccessful -> "Profile data could not be loaded."
                        else -> "Profile data is unavailable."
                    }
                )
            }
        }
    }

    fun enableEditing() {
        if (_uiState.value.profile != null && !BuildConfig.REFERENCE_PREVIEW) {
            _uiState.update { it.copy(isEditing = true, error = null) }
        }
    }

    fun saveProfile(profile: FarmerProfile) {
        if (BuildConfig.REFERENCE_PREVIEW || _uiState.value.isSaving) return
        if (profile.name.isBlank()) {
            _uiState.update { it.copy(error = "Enter your name.") }
            return
        }
        _uiState.update { it.copy(isSaving = true, error = null) }
        viewModelScope.launch {
            try {
                val response = authRepository.updateProfile(UpdateFarmerRequest(
                    name = profile.name.trim(),
                    district = profile.district.trim(),
                    preferredLanguage = _uiState.value.selectedLanguage,
                ))
                val saved = response.takeIf { it.isSuccessful }?.body()?.toProfile()
                if (saved != null) {
                    _uiState.update { it.copy(profile = saved, isEditing = false) }
                } else {
                    _uiState.update { it.copy(error = "Profile was not saved. Check your connection and try again.") }
                }
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (_: Exception) {
                _uiState.update { it.copy(error = "Profile was not saved. Your edits are still here.") }
            } finally {
                _uiState.update { it.copy(isSaving = false) }
            }
        }
    }

    fun cancelEditing() {
        if (!_uiState.value.isSaving) _uiState.update { it.copy(isEditing = false, error = null) }
    }

    fun changeLanguage(lang: String) {
        _uiState.update { it.copy(selectedLanguage = lang) }
        if (!BuildConfig.REFERENCE_PREVIEW) viewModelScope.launch {
            authRepository.setLanguage(lang)
        }
    }

    fun logout(onLoggedOut: () -> Unit) {
        viewModelScope.launch {
            authRepository.logout()
            onLoggedOut()
        }
    }
}

private fun FarmerDto.toProfile() = FarmerProfile(
    id = id, name = name, phone = phone, village = village.orEmpty(),
    district = district.orEmpty(), totalFieldsSqM = 0f, primaryCrop = "",
    preferredLanguage = preferredLanguage,
)
