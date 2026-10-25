package com.agrisage.app.ui.screens

import androidx.lifecycle.ViewModel
import com.agrisage.app.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.first
import javax.inject.Inject

@HiltViewModel
class SplashViewModel @Inject constructor(
    private val authRepository: AuthRepository,
) : ViewModel() {
    suspend fun restoreSession(): Boolean {
        if (!authRepository.hasSession()) return false
        return !authRepository.authToken.first().isNullOrBlank() || authRepository.refreshSession()
    }
}
