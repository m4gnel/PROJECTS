package com.agrisage.app.data.remote

import com.agrisage.app.data.remote.dto.*
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {

    // Auth
    @POST("auth/send-otp")
    suspend fun sendOtp(@Body request: SendOtpRequest): Response<SendOtpResponse>

    @POST("auth/verify-otp")
    suspend fun verifyOtp(@Body request: VerifyOtpRequest): Response<AuthResponse>

    @POST("auth/refresh")
    suspend fun refresh(@Body request: RefreshTokenRequest): Response<AuthResponse>

    // Farmer
    @GET("auth/me")
    suspend fun getMyProfile(): Response<FarmerDto>

    @PUT("farmers/me")
    suspend fun updateProfile(@Body request: UpdateFarmerRequest): Response<FarmerDto>

    // Fields
    @GET("fields/")
    suspend fun getFields(): Response<List<FieldDto>>

    @POST("fields/")
    suspend fun createField(@Body request: CreateFieldRequest): Response<FieldDto>

    @DELETE("fields/{fieldId}")
    suspend fun deleteField(@Path("fieldId") fieldId: String): Response<Unit>

    // Chat
    @POST("advisory")
    suspend fun sendMessage(@Body request: ChatRequest): Response<ChatResponse>

    // Weather
    @GET("weather/current")
    suspend fun getCurrentWeather(
        @Query("lat") lat: Double,
        @Query("lon") lon: Double
    ): Response<WeatherCurrentDto>

    @GET("weather/forecast")
    suspend fun getWeatherForecast(
        @Query("lat") lat: Double,
        @Query("lon") lon: Double
    ): Response<WeatherForecastDto>

    // Alerts
    @GET("notifications")
    suspend fun getAlerts(@Query("unread_only") unreadOnly: Boolean = false): Response<List<AlertDto>>

    // Advisory
    @POST("advisory")
    suspend fun askAdvisory(@Body request: AdvisoryRequest): Response<AdvisoryResponse>

    // Offline observation sync
    @POST("sync/upload")
    suspend fun uploadSyncBatch(@Body request: SyncUploadRequest): Response<SyncUploadResponse>
}
