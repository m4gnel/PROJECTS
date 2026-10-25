package com.agrisage.app.data.remote

import com.agrisage.app.data.remote.dto.AuthResponse
import com.agrisage.app.data.remote.dto.LogoutResponse
import com.agrisage.app.data.remote.dto.RefreshTokenRequest
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

/** Retrofit surface used only by the non-authenticated OkHttp authenticator. */
interface AuthRefreshApi {
    @POST("auth/refresh")
    suspend fun refresh(@Body request: RefreshTokenRequest): Response<AuthResponse>

    @POST("auth/logout")
    suspend fun logout(@Body request: RefreshTokenRequest): Response<LogoutResponse>
}
