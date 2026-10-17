package com.agrisage.app.ui.screens.advisor

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.remote.dto.ChatRequest
import com.agrisage.app.data.repository.ChatRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
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
    val selectedLanguage: String = "ml",
    val isVoiceRecording: Boolean = false,
    val sessionId: String = UUID.randomUUID().toString(),
    val error: String? = null
)

@HiltViewModel
class AdvisorViewModel @Inject constructor(
    private val chatRepository: ChatRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(
        AdvisorUiState(
            messages = listOf(
                ChatMessage(
                    id = "welcome",
                    content = "നമസ്കാരം! ഞാൻ അഗ്രി-സേജ് AI അഡ്വൈസർ. ഇന്ന് താങ്കളുടെ കൃഷിയെക്കുറിച്ച് എന്ത് സംശയമാണ് ചോദിക്കാനുള്ളത്?",
                    isFromUser = false,
                    timestamp = System.currentTimeMillis(),
                    language = "ml"
                )
            )
        )
    )
    val uiState: StateFlow<AdvisorUiState> = _uiState.asStateFlow()

    fun updateInput(text: String) {
        _uiState.update { it.copy(currentInput = text) }
    }

    fun selectLanguage(lang: String) {
        _uiState.update { it.copy(selectedLanguage = lang) }
    }

    fun startVoiceRecording() {
        _uiState.update { it.copy(isVoiceRecording = true) }
    }

    fun stopVoiceRecording() {
        _uiState.update { it.copy(isVoiceRecording = false) }
    }

    fun clearError() {
        _uiState.update { it.copy(error = null) }
    }

    fun sendMessage() {
        val input = _uiState.value.currentInput.trim()
        if (input.isBlank()) return

        val userMsg = ChatMessage(
            id = UUID.randomUUID().toString(),
            content = input,
            isFromUser = true,
            timestamp = System.currentTimeMillis(),
            language = _uiState.value.selectedLanguage
        )

        _uiState.update {
            it.copy(
                messages = it.messages + userMsg,
                currentInput = "",
                isTyping = true,
                error = null
            )
        }

        viewModelScope.launch {
            try {
                val req = ChatRequest(
                    sessionId = _uiState.value.sessionId,
                    message = input,
                    language = _uiState.value.selectedLanguage,
                    farmerId = "farmer-default-id",
                    latitude = 10.165,
                    longitude = 76.401
                )
                val response = chatRepository.sendMessage(req)
                if (response.isSuccessful && response.body() != null) {
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
                    _fallbackOfflineResponse(input)
                }
            } catch (e: Exception) {
                _fallbackOfflineResponse(input)
            }
        }
    }

    private fun _fallbackOfflineResponse(query: String) {
        val offlineAnswer = when {
            query.contains("വളം", ignoreCase = true) || query.contains("fertilizer", ignoreCase = true) ->
                "നെൽകൃഷിക്ക് വളം നൽകുമ്പോൾ: NPK 14-14-14 ഫോർമുലേഷൻ ഹെക്ടറിന് 25 കി.ഗ്രാം ശുപാർശ ചെയ്യുന്നു. മഴയ്ക്ക് മുൻപ് വളം നൽകരുത്."
            query.contains("രോഗം", ignoreCase = true) || query.contains("pest", ignoreCase = true) ->
                "കീടബാധ നിയന്ത്രണം: പ്രാദേശിക കാർഷിക സർവ്വകലാശാലയുടെ നിർദ്ദേശപ്രകാരം വേപ്പെണ്ണ എമൽഷൻ തളിക്കുക."
            else ->
                "താങ്കളുടെ ചോദ്യം ലഭിച്ചു. പ്രാദേശിക കാലാവസ്ഥയും കാർഷിക സർവകലാശാലാ ഡാറ്റയും അനുസരിച്ച് വിവരങ്ങൾ ലഭ്യമാക്കുന്നു."
        }

        val aiMsg = ChatMessage(
            id = UUID.randomUUID().toString(),
            content = offlineAnswer,
            isFromUser = false,
            timestamp = System.currentTimeMillis(),
            language = _uiState.value.selectedLanguage
        )
        _uiState.update { it.copy(messages = it.messages + aiMsg, isTyping = false) }
    }
}
