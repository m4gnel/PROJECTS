package com.agrisage.app.data.remote

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import com.agrisage.app.data.remote.dto.RefreshTokenRequest
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import okhttp3.Authenticator
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Rotates the refresh token once after an authenticated request receives 401.
 * A separate Retrofit/OkHttp client is used so the refresh call cannot recurse
 * through this authenticator. Concurrent 401s share one refresh operation.
 */
@Singleton
class TokenAuthenticator @Inject constructor(
    private val refreshApi: AuthRefreshApi,
    private val dataStore: DataStore<Preferences>,
) : Authenticator {

    private val refreshLock = Any()

    override fun authenticate(route: Route?, response: Response): Request? {
        if (responseCount(response) >= MAX_AUTH_ATTEMPTS) return null

        val failedAccessToken = response.request.header("Authorization")
            ?.removePrefix("Bearer ")
        synchronized(refreshLock) {
            val current = runBlocking { readSession() }

            // Another request may have refreshed while this response was in
            // flight. Reuse that token instead of rotating again.
            if (!current.accessToken.isNullOrBlank() && current.accessToken != failedAccessToken) {
                return response.request.newBuilder()
                    .header("Authorization", "Bearer ${current.accessToken}")
                    .build()
            }

            val refreshToken = current.refreshToken ?: return null
            val refreshed = runCatching {
                runBlocking { refreshApi.refresh(RefreshTokenRequest(refreshToken)) }
            }.getOrNull()

            val auth = refreshed?.takeIf { it.isSuccessful }?.body()
            if (auth == null || auth.accessToken.isBlank()) {
                runBlocking { clearSession() }
                return null
            }

            runBlocking {
                dataStore.edit { prefs ->
                    prefs[ACCESS_TOKEN_KEY] = auth.accessToken
                    auth.refreshToken?.takeIf(String::isNotBlank)?.let { prefs[REFRESH_TOKEN_KEY] = it }
                }
            }
            return response.request.newBuilder()
                .header("Authorization", "Bearer ${auth.accessToken}")
                .build()
        }
    }

    private suspend fun readSession(): Session {
        val prefs = dataStore.data.first()
        return Session(prefs[ACCESS_TOKEN_KEY], prefs[REFRESH_TOKEN_KEY])
    }

    private suspend fun clearSession() {
        dataStore.edit { prefs ->
            prefs.remove(ACCESS_TOKEN_KEY)
            prefs.remove(REFRESH_TOKEN_KEY)
            prefs.remove(FARMER_ID_KEY)
            prefs.remove(ONBOARDING_COMPLETED_KEY)
        }
    }

    private data class Session(val accessToken: String?, val refreshToken: String?)

    companion object {
        private const val MAX_AUTH_ATTEMPTS = 2
        val ACCESS_TOKEN_KEY = stringPreferencesKey("auth_token")
        val REFRESH_TOKEN_KEY = stringPreferencesKey("refresh_token")
        val FARMER_ID_KEY = stringPreferencesKey("farmer_id")
        val ONBOARDING_COMPLETED_KEY = androidx.datastore.preferences.core.booleanPreferencesKey("onboarding_completed")
    }

    private fun responseCount(response: Response): Int {
        var count = 1
        var prior = response.priorResponse
        while (prior != null) {
            count++
            prior = prior.priorResponse
        }
        return count
    }
}
