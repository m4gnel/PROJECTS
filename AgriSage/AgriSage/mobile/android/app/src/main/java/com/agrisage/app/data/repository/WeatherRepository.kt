package com.agrisage.app.data.repository

import com.agrisage.app.data.local.dao.WeatherDao
import com.agrisage.app.data.local.entity.WeatherEntity
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.WeatherCurrentDto
import com.agrisage.app.data.remote.dto.WeatherForecastDto
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class WeatherRepository @Inject constructor(
    private val apiService: ApiService,
    private val weatherDao: WeatherDao
) {
    fun getCachedWeather(): Flow<WeatherEntity?> = weatherDao.getLatestWeather()

    suspend fun fetchCurrentWeather(lat: Double, lon: Double): Response<WeatherCurrentDto> {
        val response = apiService.getCurrentWeather(lat, lon)
        if (response.isSuccessful && response.body() != null) {
            val dto = response.body()!!
            val entity = WeatherEntity(
                id = UUID.randomUUID().toString(),
                lat = dto.latitude,
                lon = dto.longitude,
                tempCelsius = dto.temperatureC,
                humidity = dto.humidityPercent,
                rainfallMm = dto.rainfallMm,
                windKmh = dto.windKmh,
                condition = dto.weatherCondition,
                fetchedAt = System.currentTimeMillis()
            )
            weatherDao.insertWeather(entity)
        }
        return response
    }

    suspend fun fetchForecast(lat: Double, lon: Double): Response<WeatherForecastDto> =
        apiService.getWeatherForecast(lat, lon)
}
