package com.agrisage.app.data.repository

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.AuthRefreshApi
import com.agrisage.app.data.remote.TokenAuthenticator
import com.agrisage.app.data.remote.dto.AuthResponse
import com.agrisage.app.data.remote.dto.FarmerDto
import com.agrisage.app.data.remote.dto.RefreshTokenRequest
import com.agrisage.app.data.remote.dto.SendOtpRequest
import com.agrisage.app.data.remote.dto.SendOtpResponse
import com.agrisage.app.data.remote.dto.UpdateFarmerRequest
import com.agrisage.app.data.remote.dto.VerifyOtpRequest
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import retrofit2.Response
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepository @Inject constructor(
    private val apiService: ApiService,
    private val authRefreshApi: AuthRefreshApi,
    private val dataStore: DataStore<Preferences>
) {
    companion object {
        val TOKEN_KEY = TokenAuthenticator.ACCESS_TOKEN_KEY
        val REFRESH_TOKEN_KEY = TokenAuthenticator.REFRESH_TOKEN_KEY
        val FARMER_ID_KEY = stringPreferencesKey("farmer_id")
        val LANGUAGE_KEY = stringPreferencesKey("selected_language")
        val ONBOARDING_COMPLETED_KEY = TokenAuthenticator.ONBOARDING_COMPLETED_KEY
        val FARMER_NAME_KEY = stringPreferencesKey("farmer_name")
        val FARMER_PHONE_KEY = stringPreferencesKey("farmer_phone")
        val FARMER_DISTRICT_KEY = stringPreferencesKey("farmer_district")
    }

    val authToken: Flow<String?> = dataStore.data.map { it[TOKEN_KEY] }
    val refreshToken: Flow<String?> = dataStore.data.map { it[REFRESH_TOKEN_KEY] }
    val farmerId: Flow<String?> = dataStore.data.map { it[FARMER_ID_KEY] }
    val farmerName: Flow<String> = dataStore.data.map { it[FARMER_NAME_KEY].orEmpty() }
    val farmerDistrict: Flow<String> = dataStore.data.map { it[FARMER_DISTRICT_KEY].orEmpty() }
    val selectedLanguage: Flow<String> = dataStore.data.map { it[LANGUAGE_KEY] ?: "ml" }

    suspend fun sendOtp(phone: String): Response<SendOtpResponse> =
        apiService.sendOtp(SendOtpRequest(phone))

    suspend fun verifyOtp(phone: String, otp: String, name: String?): Response<AuthResponse> {
        val response = apiService.verifyOtp(VerifyOtpRequest(phone = phone, otp = otp, name = name))
        if (response.isSuccessful && response.body() != null) {
            val auth = response.body()!!
            require(auth.accessToken.isNotBlank()) { "Authentication response did not include an access token" }
            dataStore.edit { prefs ->
                prefs[TOKEN_KEY] = auth.accessToken
                auth.refreshToken?.takeIf(String::isNotBlank)?.let { prefs[REFRESH_TOKEN_KEY] = it }
                auth.user?.id?.let { prefs[FARMER_ID_KEY] = it }
                auth.user?.language?.takeIf(String::isNotBlank)?.let { prefs[LANGUAGE_KEY] = it }
            }
        }
        return response
    }

    suspend fun getProfile(): Response<FarmerDto> {
        val response = apiService.getMyProfile()
        if (response.isSuccessful) {
            response.body()?.let { profile ->
                dataStore.edit { prefs ->
                    prefs[FARMER_ID_KEY] = profile.id
                    prefs[FARMER_NAME_KEY] = profile.name
                    prefs[FARMER_PHONE_KEY] = profile.phone
                    profile.district?.let { prefs[FARMER_DISTRICT_KEY] = it }
                    // Preserve an explicit device language preference across refreshes.
                    if (prefs[LANGUAGE_KEY] == null) prefs[LANGUAGE_KEY] = profile.preferredLanguage
                }
            }
        }
        return response
    }

    suspend fun updateProfile(request: UpdateFarmerRequest): Response<FarmerDto> {
        val response = apiService.updateProfile(request)
        if (response.isSuccessful) response.body()?.let { profile ->
            dataStore.edit { prefs ->
                prefs[FARMER_NAME_KEY] = profile.name
                prefs[FARMER_PHONE_KEY] = profile.phone
                prefs[FARMER_DISTRICT_KEY] = profile.district.orEmpty()
                prefs[LANGUAGE_KEY] = profile.preferredLanguage
            }
        }
        return response
    }

    suspend fun setLanguage(lang: String) {
        dataStore.edit { it[LANGUAGE_KEY] = lang }
    }

    suspend fun persistOnboardingProfile(name: String, phone: String, district: String, language: String) {
        dataStore.edit { prefs ->
            prefs[ONBOARDING_COMPLETED_KEY] = true
            prefs[FARMER_NAME_KEY] = name
            prefs[FARMER_PHONE_KEY] = phone
            prefs[FARMER_DISTRICT_KEY] = district
            prefs[LANGUAGE_KEY] = language
        }
    }

    suspend fun hasSession(): Boolean = dataStore.data.first().let { prefs ->
        !prefs[TOKEN_KEY].isNullOrBlank() || !prefs[REFRESH_TOKEN_KEY].isNullOrBlank()
    }

    suspend fun refreshSession(): Boolean {
        val currentRefreshToken = dataStore.data.first()[REFRESH_TOKEN_KEY]
            ?.takeIf(String::isNotBlank)
            ?: return false
        val response = runCatching {
            authRefreshApi.refresh(RefreshTokenRequest(currentRefreshToken))
        }.getOrNull()
        val auth = response?.takeIf { it.isSuccessful }?.body()
        if (auth == null || auth.accessToken.isBlank()) {
            clearSession()
            return false
        }
        dataStore.edit { prefs ->
            prefs[TOKEN_KEY] = auth.accessToken
            auth.refreshToken?.takeIf(String::isNotBlank)?.let { prefs[REFRESH_TOKEN_KEY] = it }
            auth.user?.id?.let { prefs[FARMER_ID_KEY] = it }
        }
        return true
    }

    suspend fun currentFarmerId(): String? = dataStore.data.first()[FARMER_ID_KEY]

    suspend fun logout() {
        val currentRefreshToken = dataStore.data.first()[REFRESH_TOKEN_KEY]
        if (!currentRefreshToken.isNullOrBlank()) {
            runCatching {
                authRefreshApi.logout(
                    RefreshTokenRequest(currentRefreshToken)
                )
            }
        }
        clearSession()
    }

    suspend fun clearSession() {
        dataStore.edit {
            it.remove(TOKEN_KEY)
            it.remove(REFRESH_TOKEN_KEY)
            it.remove(FARMER_ID_KEY)
            it.remove(ONBOARDING_COMPLETED_KEY)
            it.remove(FARMER_NAME_KEY)
            it.remove(FARMER_PHONE_KEY)
            it.remove(FARMER_DISTRICT_KEY)
        }
    }
}
