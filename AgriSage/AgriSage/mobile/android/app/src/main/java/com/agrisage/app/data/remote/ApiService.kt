package com.agrisage.app.data.remote

import com.agrisage.app.data.remote.dto.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // Auth
    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<TokenResponse>

    @POST("auth/token")
    @FormUrlEncoded
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String
    ): Response<TokenResponse>

    // Farmer
    @GET("farmers/me")
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
    @POST("chat/")
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
    @GET("alerts/")
    suspend fun getAlerts(@Query("unread_only") unreadOnly: Boolean = false): Response<List<AlertDto>>

    @POST("alerts/mark-read")
    suspend fun markAlertsRead(@Body request: MarkReadRequest): Response<Unit>

    // Advisory
    @POST("advisory/ask")
    suspend fun askAdvisory(@Body request: AdvisoryRequest): Response<AdvisoryResponse>
}
