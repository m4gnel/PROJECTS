package com.agrisage.app.domain.usecase

import com.agrisage.app.data.remote.dto.ChatRequest
import com.agrisage.app.data.remote.dto.ChatResponse
import com.agrisage.app.data.repository.ChatRepository
import retrofit2.Response
import javax.inject.Inject

class SendMessageUseCase @Inject constructor(
    private val chatRepository: ChatRepository
) {
    suspend operator fun invoke(request: ChatRequest): Response<ChatResponse> =
        chatRepository.sendMessage(request)
}
