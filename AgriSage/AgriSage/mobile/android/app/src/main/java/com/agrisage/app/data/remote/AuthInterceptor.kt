package com.agrisage.app.data.remote

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
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
        val TOKEN_KEY = TokenAuthenticator.ACCESS_TOKEN_KEY
    }

    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()

        // OTP bootstrap and refresh do not require an access token. Match the
        // complete API path so a user-controlled path segment cannot bypass
        // authentication accidentally.
        val path = original.url.encodedPath
        if (path == "/api/v1/auth/send-otp" ||
            path == "/api/v1/auth/verify-otp" ||
            path == "/api/v1/auth/refresh"
        ) {
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
