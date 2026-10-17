package com.agrisage.app.ui.screens.profile

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
    val offlineModeEnabled: Boolean = false,
    val notificationsEnabled: Boolean = true,
    val selectedLanguage: String = "ml",
    val isLoading: Boolean = false,
    val isSaving: Boolean = false
)

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val dataStore: DataStore<Preferences>
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        ProfileUiState(
            profile = FarmerProfile(
                id = "550e8400-e29b-41d4-a716-446655440000",
                name = "Rajan K",
                phone = "+91 98765 43210",
                village = "Kalady",
                district = "Ernakulam",
                totalFieldsSqM = 7000f,
                primaryCrop = "Paddy (Rice)",
                preferredLanguage = "ml"
            )
        )
    )
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    fun enableEditing() {
        _uiState.update { it.copy(isEditing = true) }
    }

    fun saveProfile(profile: FarmerProfile) {
        _uiState.update { it.copy(profile = profile, isEditing = false) }
    }

    fun toggleOfflineMode() {
        _uiState.update { it.copy(offlineModeEnabled = !it.offlineModeEnabled) }
    }

    fun toggleNotifications() {
        _uiState.update { it.copy(notificationsEnabled = !it.notificationsEnabled) }
    }

    fun changeLanguage(lang: String) {
        _uiState.update { it.copy(selectedLanguage = lang) }
        viewModelScope.launch {
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
