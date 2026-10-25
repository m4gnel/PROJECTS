package com.agrisage.app.data.repository

import com.agrisage.app.data.local.dao.FieldDao
import com.agrisage.app.data.local.entity.FieldEntity
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.CreateFieldRequest
import com.agrisage.app.data.remote.dto.FieldDto
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class FieldRepository @Inject constructor(
    private val apiService: ApiService,
    private val fieldDao: FieldDao
) {
    fun getLocalFields(): Flow<List<FieldEntity>> = fieldDao.getAllFields()
    fun getFieldById(id: String): Flow<FieldEntity?> = fieldDao.getFieldById(id)

    suspend fun refreshFields(): Response<List<FieldDto>> {
        val response = apiService.getFields()
        if (response.isSuccessful && response.body() != null) {
            val entities = response.body()!!.map { dto ->
                FieldEntity(
                    id = dto.id,
                    farmerId = dto.farmerId,
                    name = dto.name,
                    areaSqM = dto.areaSqM,
                    cropName = dto.activeCrop?.cropName ?: "",
                    cropVariety = dto.activeCrop?.variety ?: "",
                    sowingDate = dto.activeCrop?.sowingDate ?: "",
                    latitude = dto.latitude,
                    longitude = dto.longitude,
                    lastNdvi = dto.lastNdvi ?: 0f,
                    updatedAt = System.currentTimeMillis()
                )
            }
            fieldDao.deleteAll()
            fieldDao.insertFields(entities)
        }
        return response
    }

    suspend fun addField(request: CreateFieldRequest): Response<FieldDto> {
        val response = apiService.createField(request)
        if (response.isSuccessful && response.body() != null) {
            val dto = response.body()!!
            val entity = FieldEntity(
                id = dto.id,
                farmerId = dto.farmerId,
                name = dto.name,
                areaSqM = dto.areaSqM,
                cropName = dto.activeCrop?.cropName ?: "",
                cropVariety = dto.activeCrop?.variety ?: "",
                sowingDate = dto.activeCrop?.sowingDate ?: "",
                latitude = dto.latitude,
                longitude = dto.longitude,
                lastNdvi = dto.lastNdvi ?: 0f,
                updatedAt = System.currentTimeMillis()
            )
            fieldDao.insertField(entity)
        }
        return response
    }

    suspend fun deleteField(fieldId: String): Response<Unit> {
        val response = apiService.deleteField(fieldId)
        if (response.isSuccessful) {
            fieldDao.deleteField(fieldId)
        }
        return response
    }
}
