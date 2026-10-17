package com.agrisage.app.data.repository

import com.agrisage.app.data.local.dao.ChatDao
import com.agrisage.app.data.local.entity.ChatMessageEntity
import com.agrisage.app.data.remote.ApiService
import com.agrisage.app.data.remote.dto.AdvisoryRequest
import com.agrisage.app.data.remote.dto.AdvisoryResponse
import com.agrisage.app.data.remote.dto.ChatRequest
import com.agrisage.app.data.remote.dto.ChatResponse
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ChatRepository @Inject constructor(
    private val apiService: ApiService,
    private val chatDao: ChatDao
) {
    fun getMessages(sessionId: String): Flow<List<ChatMessageEntity>> =
        chatDao.getMessagesForSession(sessionId)

    suspend fun saveMessage(sessionId: String, content: String, isFromUser: Boolean, language: String) {
        val entity = ChatMessageEntity(
            id = UUID.randomUUID().toString(),
            sessionId = sessionId,
            content = content,
            isFromUser = isFromUser,
            language = language,
            timestamp = System.currentTimeMillis()
        )
        chatDao.insertMessage(entity)
    }

    suspend fun sendMessage(request: ChatRequest): Response<ChatResponse> {
        val response = apiService.sendMessage(request)
        if (response.isSuccessful && response.body() != null) {
            val body = response.body()!!
            saveMessage(
                sessionId = body.sessionId,
                content = body.message,
                isFromUser = false,
                language = body.language
            )
        }
        return response
    }

    suspend fun askAdvisory(request: AdvisoryRequest): Response<AdvisoryResponse> =
        apiService.askAdvisory(request)
}
