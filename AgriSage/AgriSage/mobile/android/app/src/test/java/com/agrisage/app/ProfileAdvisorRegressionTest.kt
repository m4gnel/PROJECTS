package com.agrisage.app

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.edit
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelStore
import com.agrisage.app.data.local.dao.ChatDao
import com.agrisage.app.data.local.entity.ChatMessageEntity
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.AuthRefreshApi
import com.agrisage.app.data.remote.dto.ChatRequest
import com.agrisage.app.data.remote.dto.ChatResponse
import com.agrisage.app.data.remote.dto.FarmerDto
import com.agrisage.app.data.remote.dto.UpdateFarmerRequest
import com.agrisage.app.data.repository.AuthRepository
import com.agrisage.app.data.repository.ChatRepository
import com.agrisage.app.ui.screens.advisor.AdvisorViewModel
import com.agrisage.app.ui.screens.profile.ProfileViewModel
import java.lang.reflect.Proxy
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.After
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import retrofit2.Response

@OptIn(ExperimentalCoroutinesApi::class)
class ProfileAdvisorRegressionTest {
    private val store = ViewModelStore()
    private val preferences = MemoryPreferences()
    private val original = FarmerDto("farmer-1", "test-phone", "Original", district = "District")
    private var profileResult: Response<FarmerDto> = Response.success(original)
    private var saveSucceeds = true
    private var chatResult: Response<ChatResponse> = Response.success(ChatResponse(message = "Provider reply"))
    private val sentQuestions = mutableListOf<ChatRequest>()
    private val savedRequests = mutableListOf<UpdateFarmerRequest>()
    private val api = proxy<ApiService> { method, args ->
        when (method) {
            "getMyProfile" -> profileResult
            "updateProfile" -> {
                val request = args[0] as UpdateFarmerRequest
                savedRequests += request
                if (saveSucceeds) Response.success(original.copy(
                    name = request.name.orEmpty(), district = request.district,
                    preferredLanguage = request.preferredLanguage,
                )) else Response.error<FarmerDto>(503, "{}".toResponseBody())
            }
            "sendMessage" -> {
                sentQuestions += args[0] as ChatRequest
                chatResult
            }
            else -> error("Unexpected API call: $method")
        }
    }
    private val auth = AuthRepository(api, proxy<AuthRefreshApi> { method, _ ->
        error("Unexpected refresh API call: $method")
    }, preferences)
    private val chatDao = object : ChatDao {
        override fun getMessagesForSession(sessionId: String) = flowOf(emptyList<ChatMessageEntity>())
        override suspend fun insertMessage(message: ChatMessageEntity) = Unit
        override suspend fun clearSession(sessionId: String) = Unit
    }

    @Before fun setup() { Dispatchers.setMain(StandardTestDispatcher()) }
    @After fun tearDown() { store.clear(); Dispatchers.resetMain() }

    private fun advisor() = keep(AdvisorViewModel(ChatRepository(api, chatDao), auth))
    private fun profile() = keep(ProfileViewModel(auth))
    private fun <T : ViewModel> keep(model: T): T {
        store.put(model::class.java.name, model)
        return model
    }

    @Test fun signedOutSendRetainsTheDraftWithoutCreatingAChatTurn() = runTest {
        val model = advisor()
        model.updateInput("My crop is yellowing")
        model.sendMessage()
        advanceUntilIdle()
        assertEquals("My crop is yellowing", model.uiState.value.currentInput)
        assertTrue(model.uiState.value.messages.isEmpty())
        assertTrue(sentQuestions.isEmpty())
        assertFalse(model.uiState.value.isTyping)
        assertTrue(model.uiState.value.error.orEmpty().contains("Sign in"))
    }

    @Test fun repeatedSendUsesOneRequestAndTheOriginalLanguage() = runTest {
        preferences.edit { it[AuthRepository.FARMER_ID_KEY] = "farmer-1" }
        val model = advisor()
        model.updateInput("When should I irrigate?")
        model.sendMessage()
        model.sendMessage()
        model.selectLanguage("en")
        advanceUntilIdle()
        assertEquals(1, sentQuestions.size)
        assertEquals("ml", sentQuestions.single().language)
        assertEquals("farmer-1", sentQuestions.single().farmerId)
        assertEquals(2, model.uiState.value.messages.size)
        assertFalse(model.uiState.value.isTyping)
    }

    @Test fun providerFailureRestoresDraftWithoutInventingAdvice() = runTest {
        preferences.edit { it[AuthRepository.FARMER_ID_KEY] = "farmer-1" }
        chatResult = Response.error(503, "{}".toResponseBody())
        val model = advisor()
        model.updateInput("Pest on my paddy")
        model.sendMessage()
        advanceUntilIdle()
        assertEquals("Pest on my paddy", model.uiState.value.currentInput)
        assertTrue(model.uiState.value.messages.all { it.isFromUser })
        assertNotNull(model.uiState.value.error)
        assertFalse(model.uiState.value.isTyping)
    }

    @Test fun profileSaveWaitsForProviderAndUpdatesTheSharedIdentity() = runTest {
        val model = profile()
        advanceUntilIdle()
        model.enableEditing()
        val edited = model.uiState.value.profile!!.copy(name = " Updated ", district = "New district")
        model.saveProfile(edited)
        assertEquals("Original", model.uiState.value.profile!!.name)
        assertTrue(model.uiState.value.isSaving)
        advanceUntilIdle()
        assertEquals("Updated", model.uiState.value.profile!!.name)
        assertEquals("Updated", auth.farmerName.first())
        assertEquals("New district", auth.farmerDistrict.first())
        assertFalse(model.uiState.value.isEditing)
        assertFalse(model.uiState.value.isSaving)
        assertEquals(1, savedRequests.size)
    }

    @Test fun failedProfileSaveLeavesExistingIdentityAndEditorIntact() = runTest {
        val model = profile()
        advanceUntilIdle()
        model.enableEditing()
        saveSucceeds = false
        model.saveProfile(model.uiState.value.profile!!.copy(name = "Unsaved"))
        advanceUntilIdle()
        assertEquals("Original", model.uiState.value.profile!!.name)
        assertEquals("Original", auth.farmerName.first())
        assertTrue(model.uiState.value.isEditing)
        assertFalse(model.uiState.value.isSaving)
        assertNotNull(model.uiState.value.error)
    }

    @Test fun profileRefreshDoesNotOverwriteDeviceLanguageChoice() = runTest {
        auth.setLanguage("ta")
        val model = profile()
        advanceUntilIdle()
        assertEquals("ta", model.uiState.value.selectedLanguage)
        assertEquals("ta", auth.selectedLanguage.first())
        model.changeLanguage("en")
        advanceUntilIdle()
        model.loadProfile()
        advanceUntilIdle()
        assertEquals("en", model.uiState.value.selectedLanguage)
        assertEquals("en", auth.selectedLanguage.first())
    }

    @Test fun failedProfileRefreshKeepsLastLoadedProfileButShowsError() = runTest {
        val model = profile()
        advanceUntilIdle()
        profileResult = Response.error(503, "{}".toResponseBody())
        model.loadProfile()
        advanceUntilIdle()
        assertEquals("Original", model.uiState.value.profile!!.name)
        assertFalse(model.uiState.value.isLoading)
        assertNotNull(model.uiState.value.error)
    }

    private class MemoryPreferences : DataStore<Preferences> {
        override val data = MutableStateFlow(emptyPreferences())
        override suspend fun updateData(transform: suspend (Preferences) -> Preferences): Preferences {
            data.value = transform(data.value)
            return data.value
        }
    }

    private inline fun <reified T> proxy(crossinline call: (String, Array<out Any?>) -> Any?): T =
        Proxy.newProxyInstance(T::class.java.classLoader, arrayOf(T::class.java)) { _, method, args ->
            call(method.name, args ?: emptyArray())
        } as T
}
