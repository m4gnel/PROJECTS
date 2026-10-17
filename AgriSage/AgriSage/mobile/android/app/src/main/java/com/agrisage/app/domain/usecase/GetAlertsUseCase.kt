package com.agrisage.app.domain.usecase

import com.agrisage.app.data.local.entity.AlertEntity
import com.agrisage.app.data.remote.dto.AlertDto
import com.agrisage.app.data.repository.AlertRepository
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import javax.inject.Inject

class GetAlertsUseCase @Inject constructor(
    private val alertRepository: AlertRepository
) {
    operator fun invoke(): Flow<List<AlertEntity>> = alertRepository.getLocalAlerts()

    suspend fun refresh(): Response<List<AlertDto>> = alertRepository.refreshAlerts()
}
