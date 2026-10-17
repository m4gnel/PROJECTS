package com.agrisage.app.data.repository

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.FarmerDto
import com.agrisage.app.data.remote.dto.RegisterRequest
import com.agrisage.app.data.remote.dto.TokenResponse
import com.agrisage.app.data.remote.dto.UpdateFarmerRequest
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import retrofit2.Response
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepository @Inject constructor(
    private val apiService: ApiService,
    private val dataStore: DataStore<Preferences>
) {
    companion object {
        val TOKEN_KEY = stringPreferencesKey("auth_token")
        val FARMER_ID_KEY = stringPreferencesKey("farmer_id")
        val LANGUAGE_KEY = stringPreferencesKey("selected_language")
    }

    val authToken: Flow<String?> = dataStore.data.map { it[TOKEN_KEY] }
    val selectedLanguage: Flow<String> = dataStore.data.map { it[LANGUAGE_KEY] ?: "ml" }

    suspend fun register(request: RegisterRequest): Response<TokenResponse> {
        val response = apiService.register(request)
        if (response.isSuccessful && response.body() != null) {
            val token = response.body()!!
            dataStore.edit { prefs ->
                prefs[TOKEN_KEY] = token.accessToken
                prefs[FARMER_ID_KEY] = token.farmerId
            }
        }
        return response
    }

    suspend fun login(phone: String, pass: String): Response<TokenResponse> {
        val response = apiService.login(username = phone, password = pass)
        if (response.isSuccessful && response.body() != null) {
            val token = response.body()!!
            dataStore.edit { prefs ->
                prefs[TOKEN_KEY] = token.accessToken
                prefs[FARMER_ID_KEY] = token.farmerId
            }
        }
        return response
    }

    suspend fun getProfile(): Response<FarmerDto> = apiService.getMyProfile()

    suspend fun updateProfile(request: UpdateFarmerRequest): Response<FarmerDto> =
        apiService.updateProfile(request)

    suspend fun setLanguage(lang: String) {
        dataStore.edit { it[LANGUAGE_KEY] = lang }
    }

    suspend fun logout() {
        dataStore.edit {
            it.remove(TOKEN_KEY)
            it.remove(FARMER_ID_KEY)
        }
    }
}
