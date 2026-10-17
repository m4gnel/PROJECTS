package com.agrisage.app.data.remote

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import okhttp3.Interceptor
import okhttp3.Response
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthInterceptor @Inject constructor(
    private val dataStore: DataStore<Preferences>
) : Interceptor {

    companion object {
        val TOKEN_KEY = stringPreferencesKey("auth_token")
    }

    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()

        // Skip adding token for register and login endpoints
        val path = original.url.encodedPath
        if (path.contains("auth/register") || path.contains("auth/token")) {
            return chain.proceed(original)
        }

        val token = runBlocking {
            val prefs = dataStore.data.first()
            prefs[TOKEN_KEY]
        }

        val request = if (!token.isNullOrBlank()) {
            original.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            original
        }

        return chain.proceed(request)
    }
}
