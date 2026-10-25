package com.agrisage.app.ui.screens.advisor

import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.speech.RecognizerIntent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Grass
import androidx.compose.material.icons.filled.BugReport
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.ui.components.ChatBubble
import com.agrisage.app.ui.components.tactilePress
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireLeafPale
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSurface
import com.agrisage.app.ui.theme.WireSurface2
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireTextSecondary
import com.agrisage.app.ui.theme.WireWhite

private val AdvisorBackground = Color(0xFFF8FCF9)

private data class AdvisorPrompt(
    val label: String,
    val icon: ImageVector,
)

private val advisorPrompts = listOf(
    AdvisorPrompt("My crop is yellowing", Icons.Default.Eco),
    AdvisorPrompt("When should I irrigate?", Icons.Default.WaterDrop),
    AdvisorPrompt("Pest on my paddy", Icons.Default.BugReport),
)

@Composable
fun AdvisorScreen(
    navController: NavHostController,
    viewModel: AdvisorViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()
    val speechLauncher = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        viewModel.stopVoiceRecording()
        if (result.resultCode == Activity.RESULT_OK) {
            result.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                ?.firstOrNull()?.takeIf(String::isNotBlank)?.let(viewModel::updateInput)
        }
    }
    LaunchedEffect(state.messages.size, state.isTyping) {
        if (state.messages.isNotEmpty()) {
            listState.animateScrollToItem(state.messages.lastIndex + if (state.isTyping) 1 else 0)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(AdvisorBackground)
    ) {
        AdvisorHeader(
            selectedLanguage = state.selectedLanguage,
            onBack = { navController.popBackStack() },
            onLanguageSelected = viewModel::selectLanguage,
        )

        if (state.messages.isEmpty()) {
            AdvisorEmptyState(
                modifier = Modifier.weight(1f),
                onPromptSelected = viewModel::updateInput,
            )
        } else {
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 12.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(state.messages, key = { it.id }) { message ->
                    ChatBubble(message = message.content, isUser = message.isFromUser)
                }
                if (state.isTyping) {
                    item {
                        Text(
                            text = "Agri-SAGE is analyzing the available provider data…",
                            color = WireTextSecondary,
                            fontSize = 12.sp,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
                        )
                    }
                }
            }
        }

        state.error?.let { error ->
            Text(
                text = error,
                color = WireAlert,
                fontSize = 12.sp,
                lineHeight = 16.sp,
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 4.dp),
            )
        }

        AdvisorComposer(
            input = state.currentInput,
            selectedLanguage = state.selectedLanguage,
            isRecording = state.isVoiceRecording,
            isSending = state.isTyping,
            onInputChanged = viewModel::updateInput,
            onVoiceClick = {
                if (!state.isVoiceRecording) {
                    try {
                        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                            putExtra(RecognizerIntent.EXTRA_LANGUAGE, state.selectedLanguage)
                            putExtra(RecognizerIntent.EXTRA_PROMPT, "Dictate a question; review it before sending")
                            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
                        }
                        speechLauncher.launch(intent)
                        viewModel.startVoiceRecording()
                    } catch (_: ActivityNotFoundException) {
                        viewModel.voiceInputUnavailable()
                    } catch (_: SecurityException) {
                        viewModel.voiceInputUnavailable()
                    }
                }
            },
            onSend = viewModel::sendMessage,
        )
    }
}

@Composable
private fun AdvisorHeader(
    selectedLanguage: String,
    onBack: () -> Unit,
    onLanguageSelected: (String) -> Unit,
) {
    Surface(color = WireSageDeep, contentColor = Color.White) {
        BoxWithConstraints {
            val compact = maxWidth < 380.dp
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth().statusBarsPadding()
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    IconButton(onClick = onBack, modifier = Modifier.size(48.dp)) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                    Icon(Icons.Default.SmartToy, contentDescription = null, tint = Color.White, modifier = Modifier.size(19.dp))
                    Spacer(Modifier.width(6.dp))
                    Text("Advisor", fontSize = 18.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                    if (!compact) AdvisorLanguageChips(selectedLanguage, onLanguageSelected)
                }
                if (compact) {
                    Row(Modifier.fillMaxWidth().padding(horizontal = 12.dp), horizontalArrangement = Arrangement.End) {
                        AdvisorLanguageChips(selectedLanguage, onLanguageSelected)
                    }
                }
            }
        }
    }
}

@Composable
private fun AdvisorLanguageChips(selectedLanguage: String, onLanguageSelected: (String) -> Unit) {
    Row {
        listOf("en" to "EN", "hi" to "HI", "ml" to "ML", "ta" to "TA").forEach { (code, label) ->
            val selected = selectedLanguage == code
            Box(
                modifier = Modifier.size(48.dp).selectable(
                    selected = selected,
                    role = Role.RadioButton,
                    onClick = { onLanguageSelected(code) },
                ),
                contentAlignment = Alignment.Center,
            ) {
                Surface(
                    color = if (selected) Color(0xFF55C58C) else Color.White.copy(alpha = 0.20f),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier
                        .padding(start = 4.dp)
                        .height(32.dp),
                ) {
                    Box(
                        modifier = Modifier.padding(horizontal = 10.dp),
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(
                            text = label,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            color = if (selected) WireSageDeep else Color.White,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun AdvisorEmptyState(
    modifier: Modifier = Modifier,
    onPromptSelected: (String) -> Unit,
) {
    BoxWithConstraints(modifier = modifier.fillMaxWidth()) {
    val viewportHeight = maxHeight
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .heightIn(min = viewportHeight)
            .padding(horizontal = 20.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Surface(
            color = Color.Transparent,
            modifier = Modifier.size(72.dp),
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.Grass,
                    contentDescription = "Farm advisor",
                    tint = Color(0xFF8AAE2F),
                    modifier = Modifier.size(62.dp),
                )
            }
        }
        Spacer(Modifier.height(22.dp))
        Text(
            text = "Ask me anything about your farm",
            fontSize = 18.sp,
            fontWeight = FontWeight.Bold,
            color = WireSageDeep,
        )
        Spacer(Modifier.height(24.dp))
        advisorPrompts.forEach { prompt ->
            Surface(
                color = AdvisorBackground,
                shape = RoundedCornerShape(8.dp),
                border = BorderStroke(1.dp, WireTextPrimary.copy(alpha = 0.75f)),
                modifier = Modifier
                    .padding(vertical = 5.dp)
                    .heightIn(min = 48.dp)
                    .tactilePress(
                        scaleDown = 0.97f,
                        onClickLabel = "Use prompt ${prompt.label}",
                        onClick = { onPromptSelected(prompt.label) },
                    ),
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(prompt.label, fontSize = 13.sp, color = WireTextPrimary)
                    Spacer(Modifier.width(7.dp))
                    Icon(prompt.icon, contentDescription = null, tint = WireSage, modifier = Modifier.size(17.dp))
                }
            }
        }
    }
    }
}

@Composable
private fun AdvisorComposer(
    input: String,
    selectedLanguage: String,
    isRecording: Boolean,
    isSending: Boolean,
    onInputChanged: (String) -> Unit,
    onVoiceClick: () -> Unit,
    onSend: () -> Unit,
) {
    Surface(
        color = Color.White,
        shadowElevation = 6.dp,
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 8.dp),
        ) {
            Text(
                text = "Responding in: ${selectedLanguage.uppercase()} · Voice uses your device's speech service",
                color = WireTextMuted,
                fontSize = 10.sp,
                modifier = Modifier.padding(bottom = 8.dp),
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                OutlinedTextField(
                    value = input,
                    onValueChange = onInputChanged,
                    placeholder = { Text("Type or speak your question…", fontSize = 13.sp) },
                    modifier = Modifier
                        .weight(1f)
                        .heightIn(min = 56.dp),
                    singleLine = true,
                    shape = RoundedCornerShape(14.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = WireSage,
                        unfocusedBorderColor = WireTextPrimary.copy(alpha = 0.75f),
                        focusedContainerColor = Color.White,
                        unfocusedContainerColor = Color.White,
                    ),
                )
                Spacer(Modifier.width(8.dp))
                Surface(
                    color = if (isRecording) WireAlert else WireSage,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier
                        .size(48.dp)
                        .tactilePress(
                            scaleDown = 0.94f,
                            onClickLabel = if (isRecording) "Stop voice input" else "Start voice input",
                            onClick = onVoiceClick,
                        ),
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(Icons.Default.Mic, contentDescription = "Voice input", tint = Color.White)
                    }
                }
                Spacer(Modifier.width(8.dp))
                Surface(
                    color = if (input.isBlank() || isSending) WireSurface2 else WireSage,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier
                        .size(48.dp)
                        .tactilePress(
                            scaleDown = 0.94f,
                            onClickLabel = "Send question",
                            onClick = if (input.isBlank() || isSending) null else onSend,
                        ),
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            Icons.AutoMirrored.Filled.Send,
                            contentDescription = "Send",
                            tint = if (input.isBlank() || isSending) WireTextMuted else Color.White,
                        )
                    }
                }
            }
        }
    }
}
