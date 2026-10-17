package com.agrisage.app.domain.usecase

import com.agrisage.app.data.local.entity.WeatherEntity
import com.agrisage.app.data.remote.dto.WeatherCurrentDto
import com.agrisage.app.data.repository.WeatherRepository
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import javax.inject.Inject

class GetWeatherUseCase @Inject constructor(
    private val weatherRepository: WeatherRepository
) {
    operator fun invoke(): Flow<WeatherEntity?> = weatherRepository.getCachedWeather()

    suspend fun refresh(lat: Double, lon: Double): Response<WeatherCurrentDto> =
        weatherRepository.fetchCurrentWeather(lat, lon)
}
