package com.agrisage.app.ui.screens.advisor

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import com.agrisage.app.ui.components.ChatBubble
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireLeafPale
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSurface
import com.agrisage.app.ui.theme.WireSurface2
import com.agrisage.app.ui.theme.WireTextMuted
import com.agrisage.app.ui.theme.WireWhite

@Composable
fun AdvisorScreen(
    navController: NavHostController,
    viewModel: AdvisorViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()

    LaunchedEffect(state.messages.size) {
        if (state.messages.isNotEmpty()) {
            listState.animateScrollToItem(state.messages.size - 1)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(WireWhite)
    ) {
        // Top Header in Sage
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(WireSage)
                .padding(horizontal = 16.dp, vertical = 14.dp)
        ) {
            Text(
                text = "🤖 Farm Advisor",
                fontSize = 18.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color.White
            )
            Text(
                text = "14 AI agents · Responds in ${state.selectedLanguage.uppercase()}",
                fontSize = 12.sp,
                color = Color.White.copy(alpha = 0.8f),
                modifier = Modifier.padding(top = 2.dp)
            )
        }

        // Language Selector Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(WireSurface)
                .padding(horizontal = 12.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            listOf("ml" to "ML", "en" to "EN", "ta" to "TA", "hi" to "HI").forEach { (code, label) ->
                val isSel = state.selectedLanguage == code
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (isSel) WireSage else WireSurface2)
                        .clickable { viewModel.selectLanguage(code) }
                        .padding(horizontal = 12.dp, vertical = 5.dp)
                ) {
                    Text(
                        text = label,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = if (isSel) Color.White else WireSageDeep
                    )
                }
            }
        }

        // Chat Messages List
        LazyColumn(
            state = listState,
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 8.dp)
        ) {
            items(state.messages) { msg ->
                ChatBubble(
                    message = msg.content,
                    isUser = msg.isFromUser
                )
            }

            if (state.isTyping) {
                item {
                    Text(
                        text = "🌿 Agri-SAGE is analyzing across 14 agents...",
                        fontSize = 12.sp,
                        color = WireLeaf,
                        fontWeight = FontWeight.Medium,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp)
                    )
                }
            }
        }

        // Bottom Input Row
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color.White)
                .padding(horizontal = 10.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Voice button
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(if (state.isVoiceRecording) WireAlert else WireLeafPale)
                    .clickable {
                        if (state.isVoiceRecording) viewModel.stopVoiceRecording() else viewModel.startVoiceRecording()
                    },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Mic,
                    contentDescription = "Voice Input",
                    tint = if (state.isVoiceRecording) Color.White else WireSageDeep,
                    modifier = Modifier.size(20.dp)
                )
            }

            Spacer(modifier = Modifier.width(8.dp))

            // Text input
            OutlinedTextField(
                value = state.currentInput,
                onValueChange = { viewModel.updateInput(it) },
                placeholder = { Text("Ask in any language...", fontSize = 13.sp, color = WireTextMuted) },
                modifier = Modifier
                    .weight(1f)
                    .height(50.dp),
                shape = RoundedCornerShape(12.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = WireSage,
                    unfocusedBorderColor = WireBorder,
                    focusedContainerColor = WireSurface,
                    unfocusedContainerColor = WireSurface
                ),
                maxLines = 2
            )

            Spacer(modifier = Modifier.width(8.dp))

            // Send button
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(WireSage)
                    .clickable { viewModel.sendMessage() },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.Send,
                    contentDescription = "Send",
                    tint = Color.White,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
    }
}
