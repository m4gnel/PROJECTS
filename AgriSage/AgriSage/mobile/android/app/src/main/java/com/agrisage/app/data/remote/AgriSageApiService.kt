package com.agrisage.app.data.remote

import retrofit2.Response
import retrofit2.http.*

interface AgriSageApiService {
    @GET("api/v1/health")
    suspend fun checkHealth(): Response<Map<String, Any>>

    @POST("api/v1/diagnose")
    suspend fun submitDiagnosis(
        @Body payload: Map<String, Any>
    ): Response<Map<String, Any>>

    @GET("api/v1/notifications/briefing")
    suspend fun getMorningBriefing(
        @Query("farmer_name") farmerName: String,
        @Query("crop") crop: String,
        @Query("language") language: String
    ): Response<Map<String, Any>>

    @POST("api/v1/sync/upload")
    suspend fun uploadSyncBatch(
        @Body payload: Map<String, Any>
    ): Response<Map<String, Any>>

    @GET("api/v1/sync/package")
    suspend fun getSyncPackage(
        @Query("crop") crop: String,
        @Query("language") language: String
    ): Response<Map<String, Any>>
}
