package com.agrisage.app

import com.agrisage.app.ui.screens.advisor.AdvisorUiState
import com.agrisage.app.ui.screens.advisor.ChatMessage
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class AdvisorViewModelTest {

    @Test
    fun testAdvisorUiState() {
        val msg = ChatMessage(
            id = "1",
            content = "നമസ്കാരം",
            isFromUser = true,
            timestamp = 1000L,
            language = "ml"
        )
        val state = AdvisorUiState(
            messages = listOf(msg),
            selectedLanguage = "ml",
            isTyping = false
        )

        assertEquals(1, state.messages.size)
        assertEquals("ml", state.selectedLanguage)
        assertFalse(state.isTyping)
        assertEquals("നമസ്കാരം", state.messages.first().content)
    }
}
