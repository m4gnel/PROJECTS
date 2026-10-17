package com.agrisage.app.domain.usecase

import com.agrisage.app.data.local.entity.FieldEntity
import com.agrisage.app.data.remote.dto.FieldDto
import com.agrisage.app.data.repository.FieldRepository
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import javax.inject.Inject

class GetFieldsUseCase @Inject constructor(
    private val fieldRepository: FieldRepository
) {
    operator fun invoke(): Flow<List<FieldEntity>> = fieldRepository.getLocalFields()

    suspend fun refresh(): Response<List<FieldDto>> = fieldRepository.refreshFields()
}
