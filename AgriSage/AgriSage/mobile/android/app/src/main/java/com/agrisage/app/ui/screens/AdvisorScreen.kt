package com.agrisage.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.agrisage.app.ui.theme.*

/**
 * Screen 4: AI Advisor Chat
 * Route: Advisor
 *
 * Per spec:
 * - TopBar: back arrow | "🤖 Farm Advisor" | language toggle chips
 * - Chat area (LazyColumn reversed): AI bubbles (left) + User bubbles (right)
 * - Input area: text field + mic + send button
 * - Empty state: suggestion chips
 */

data class ChatMessage(
    val id: String,
    val text: String,
    val isUser: Boolean,
    val timestamp: String,
    val sourceAgents: List<String> = emptyList()
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdvisorScreen(navController: NavController) {
    val languages = listOf("EN", "HI", "ML", "TA", "TE", "PA")
    var selectedLang by remember { mutableStateOf("EN") }
    var inputText by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    val messages = remember { mutableStateListOf<ChatMessage>() }
    val listState = rememberLazyListState()

    val suggestions = listOf(
        "My crop is yellowing 🌿",
        "When should I irrigate? 💧",
        "Pest on my paddy 🐛"
    )

    fun handleSendMessage(msg: String) {
        if (msg.isBlank()) return
        messages.add(0, ChatMessage(
            id = System.currentTimeMillis().toString(),
            text = msg.trim(),
            isUser = true,
            timestamp = "Now"
        ))
        val reply = when {
            msg.contains("yellowing", ignoreCase = true) ->
                "🌿 Leaf yellowing in rice indicates early Nitrogen deficiency. Apply 25kg Urea/acre between 6–9 AM when soil moisture is adequate. Avoid application during peak midday heat."
            msg.contains("irrigate", ignoreCase = true) ->
                "💧 Soil moisture in North Paddy Field is currently 68% (optimal). Next irrigation recommended Wednesday morning before 10 AM. Rain expected Thursday."
            msg.contains("pest", ignoreCase = true) ->
                "🐛 NBAIR alert: High Brown Planthopper (BPH) incidence in Ernakulam. Check plant base near water line. If >10 nymphs/hill, spray Triflumezopyrim 10% SC @ 94ml/acre."
            else ->
                "🌾 Based on real-time agrometeorological data for your farm, crop conditions are healthy. Keep 2–3 cm standing water and inspect for leaf blast spots."
        }
        messages.add(0, ChatMessage(
            id = (System.currentTimeMillis() + 10).toString(),
            text = reply,
            isUser = false,
            timestamp = "Just now",
            sourceAgents = listOf("CropAgent", "WeatherAgent")
        ))
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "🤖 Advisor",
                        fontWeight = FontWeight.Bold,
                        fontSize = 17.sp,
                        color = Color.White
                    )
                },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    val mainLangs = listOf("EN", "HI", "ML", "TA")
                    mainLangs.forEach { lang ->
                        val selected = selectedLang == lang
                        FilterChip(
                            selected = selected,
                            onClick = { selectedLang = lang },
                            label = { Text(lang, fontSize = 10.sp) },
                            modifier = Modifier.padding(end = 4.dp).height(26.dp),
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = Color(0xFF52B788),
                                selectedLabelColor = Color.White,
                                containerColor = Color.White.copy(alpha = 0.2f),
                                labelColor = Color.White,
                            )
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF1B4332))
            )
        },
        bottomBar = {
            // Input area
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shadowElevation = 8.dp,
                color = Color.White
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(
                        text = "Responding in: $selectedLang",
                        fontSize = 11.sp,
                        color = Color(0xFF6B7280),
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                    Row(
                        verticalAlignment = Alignment.Bottom,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        OutlinedTextField(
                            value = inputText,
                            onValueChange = { inputText = it },
                            placeholder = { Text("Type or speak your question...", fontSize = 14.sp) },
                            modifier = Modifier.weight(1f),
                            maxLines = 3,
                            shape = RoundedCornerShape(16.dp),
                            keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                            keyboardActions = KeyboardActions(
                                onSend = {
                                    if (inputText.isNotBlank()) {
                                        val msg = inputText
                                        inputText = ""
                                        handleSendMessage(msg)
                                    }
                                }
                            )
                        )
                        Spacer(Modifier.width(8.dp))
                        // Mic button
                        IconButton(
                            onClick = { handleSendMessage("When should I irrigate? 💧") },
                            modifier = Modifier
                                .size(48.dp)
                                .background(Color(0xFF40916C), RoundedCornerShape(12.dp))
                        ) {
                            Icon(Icons.Default.Mic, contentDescription = "Speak", tint = Color.White)
                        }
                        Spacer(Modifier.width(8.dp))
                        // Send button
                        IconButton(
                            onClick = {
                                if (inputText.isNotBlank()) {
                                    val msg = inputText
                                    inputText = ""
                                    handleSendMessage(msg)
                                }
                            },
                            enabled = inputText.isNotBlank(),
                            modifier = Modifier
                                .size(48.dp)
                                .background(
                                    if (inputText.isNotBlank()) Color(0xFF1B4332)
                                    else Color(0xFFE8F4E8),
                                    RoundedCornerShape(12.dp)
                                )
                        ) {
                            Icon(
                                Icons.Default.Send,
                                contentDescription = "Send",
                                tint = if (inputText.isNotBlank()) Color.White else Color(0xFF6B7280)
                            )
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(Color(0xFFF8FCF8))
        ) {
            if (messages.isEmpty() && !isLoading) {
                // Empty state with suggestion chips
                Column(
                    modifier = Modifier.align(Alignment.Center).padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text("🌾", fontSize = 48.sp)
                    Spacer(Modifier.height(12.dp))
                    Text(
                        "Ask me anything about your farm",
                        style = MaterialTheme.typography.headlineMedium,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF1B4332)
                    )
                    Spacer(Modifier.height(24.dp))
                    suggestions.forEach { suggestion ->
                        SuggestionChip(
                            onClick = { handleSendMessage(suggestion) },
                            label = { Text(suggestion) },
                            modifier = Modifier.padding(bottom = 8.dp)
                        )
                    }
                }
            } else {
                LazyColumn(
                    state = listState,
                    reverseLayout = true,
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    if (isLoading) {
                        item {
                            // Loading dots placeholder
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = 8.dp),
                                horizontalArrangement = Arrangement.Start
                            ) {
                                Surface(
                                    shape = RoundedCornerShape(16.dp),
                                    color = Color.White,
                                    shadowElevation = 2.dp
                                ) {
                                    Text(
                                        "⏳ Thinking...",
                                        modifier = Modifier.padding(12.dp),
                                        color = Color(0xFF6B7280)
                                    )
                                }
                            }
                        }
                    }
                    items(messages) { message ->
                        if (message.isUser) {
                            UserBubble(text = message.text, timestamp = message.timestamp)
                        } else {
                            AiBubble(
                                text = message.text,
                                timestamp = message.timestamp,
                                sourceAgents = message.sourceAgents,
                                onSpeak = { /* TODO: TTS */ }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun AiBubble(
    text: String,
    timestamp: String,
    sourceAgents: List<String>,
    onSpeak: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(end = 48.dp),
        horizontalArrangement = Arrangement.Start
    ) {
        Column {
            Surface(
                shape = RoundedCornerShape(4.dp, 16.dp, 16.dp, 16.dp),
                color = Color.White,
                shadowElevation = 2.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    // SageLeaf left border indicator
                    Row {
                        Box(
                            modifier = Modifier
                                .width(3.dp)
                                .height(48.dp)
                                .background(Color(0xFF52B788), RoundedCornerShape(2.dp))
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(
                            text = text,
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color(0xFF1B4332)
                        )
                    }
                    if (sourceAgents.isNotEmpty()) {
                        Spacer(Modifier.height(6.dp))
                        Text(
                            text = "📡 ${sourceAgents.joinToString(" + ")}",
                            fontSize = 10.sp,
                            color = Color(0xFF6B7280)
                        )
                    }
                    Text(timestamp, fontSize = 10.sp, color = Color(0xFF9CA3AF))
                }
            }
        }
    }
}

@Composable
fun UserBubble(text: String, timestamp: String) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(start = 48.dp),
        horizontalArrangement = Arrangement.End
    ) {
        Surface(
            shape = RoundedCornerShape(16.dp, 4.dp, 16.dp, 16.dp),
            color = Color(0xFF2D6A4F)
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                Text(text = text, color = Color.White, style = MaterialTheme.typography.bodyMedium)
                Text(timestamp, fontSize = 10.sp, color = Color.White.copy(alpha = 0.6f))
            }
        }
    }
}

@Preview(showBackground = true, widthDp = 360, heightDp = 800)
@Composable
fun AdvisorScreenPreview() {
    AdvisorScreen(navController = rememberNavController())
}
