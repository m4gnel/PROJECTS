package com.agrisage.app.ui.screens.advisor

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.BuildConfig
import com.agrisage.app.data.remote.dto.ChatRequest
import com.agrisage.app.data.repository.AuthRepository
import com.agrisage.app.data.repository.ChatRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.UUID
import javax.inject.Inject

data class ChatMessage(
    val id: String,
    val content: String,
    val isFromUser: Boolean,
    val timestamp: Long,
    val language: String
)

data class AdvisorUiState(
    val messages: List<ChatMessage> = emptyList(),
    val currentInput: String = "",
    val isTyping: Boolean = false,
    val selectedLanguage: String = if (BuildConfig.REFERENCE_PREVIEW) "en" else "ml",
    val isVoiceRecording: Boolean = false,
    val sessionId: String = UUID.randomUUID().toString(),
    val error: String? = null
)

@HiltViewModel
class AdvisorViewModel @Inject constructor(
    private val chatRepository: ChatRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AdvisorUiState())
    val uiState: StateFlow<AdvisorUiState> = _uiState.asStateFlow()

    init {
        if (!BuildConfig.REFERENCE_PREVIEW) viewModelScope.launch {
            authRepository.selectedLanguage.collect { language ->
                _uiState.update { it.copy(selectedLanguage = language) }
            }
        }
    }

    fun updateInput(text: String) {
        _uiState.update { it.copy(currentInput = text) }
    }

    fun selectLanguage(lang: String) {
        _uiState.update { it.copy(selectedLanguage = lang) }
        if (!BuildConfig.REFERENCE_PREVIEW) viewModelScope.launch {
            authRepository.setLanguage(lang)
        }
    }

    fun startVoiceRecording() {
        _uiState.update { it.copy(isVoiceRecording = true) }
    }

    fun stopVoiceRecording() {
        _uiState.update { it.copy(isVoiceRecording = false) }
    }

    fun voiceInputUnavailable() {
        _uiState.update {
            it.copy(isVoiceRecording = false, error = "Speech input is unavailable on this device. Please type your question.")
        }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }

    fun sendMessage() {
        val snapshot = _uiState.value
        val input = snapshot.currentInput.trim()
        if (input.isBlank() || snapshot.isTyping) return
        if (BuildConfig.REFERENCE_PREVIEW) {
            _uiState.update { it.copy(error = "Reference preview does not send questions. Sign in to the normal app for live advice.") }
            return
        }

        // Reserve this send before launching; repeated taps cannot enqueue it twice.
        _uiState.update { it.copy(isTyping = true, error = null) }

        viewModelScope.launch {
            try {
                val farmerId = authRepository.currentFarmerId()?.takeIf(String::isNotBlank)
                if (farmerId == null) {
                    _setUnavailable("Sign in is required before asking the farm advisor.")
                    return@launch
                }

                val userMsg = ChatMessage(
                    id = UUID.randomUUID().toString(),
                    content = input,
                    isFromUser = true,
                    timestamp = System.currentTimeMillis(),
                    language = snapshot.selectedLanguage
                )

                _uiState.update {
                    it.copy(
                        messages = it.messages + userMsg,
                        currentInput = if (it.currentInput.trim() == input) "" else it.currentInput,
                        isTyping = true,
                        error = null
                    )
                }

                val req = ChatRequest(
                    sessionId = snapshot.sessionId,
                    message = input,
                    language = snapshot.selectedLanguage,
                    farmerId = farmerId,
                    district = authRepository.farmerDistrict.first()
                )
                val response = chatRepository.sendMessage(req)
                if (response.isSuccessful && !response.body()?.message.isNullOrBlank()) {
                    val body = response.body()!!
                    val aiMsg = ChatMessage(
                        id = UUID.randomUUID().toString(),
                        content = body.message,
                        isFromUser = false,
                        timestamp = System.currentTimeMillis(),
                        language = body.language
                    )
                    _uiState.update { it.copy(messages = it.messages + aiMsg, isTyping = false) }
                } else {
                    _setUnavailable("The farm advisor is unavailable right now. No offline recommendation was generated.", input)
                }
            } catch (cancelled: CancellationException) {
                throw cancelled
            } catch (_: Exception) {
                _setUnavailable("The farm advisor is unavailable right now. No offline recommendation was generated.", input)
            }
        }
    }

    private fun _setUnavailable(message: String, failedInput: String? = null) {
        _uiState.update {
            it.copy(isTyping = false, error = message,
                currentInput = it.currentInput.ifBlank { failedInput.orEmpty() })
        }
    }
}
