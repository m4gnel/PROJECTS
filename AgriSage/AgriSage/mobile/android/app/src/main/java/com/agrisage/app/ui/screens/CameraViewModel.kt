package com.agrisage.app.ui.screens

import androidx.lifecycle.ViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject

enum class QualityLevel {
    GOOD, OKAY, POOR
}

@HiltViewModel
class CameraViewModel @Inject constructor() : ViewModel() {
    private val _currentCrop = MutableStateFlow("rice")
    val currentCrop: StateFlow<String> = _currentCrop.asStateFlow()

    private val _qualityLevel = MutableStateFlow(QualityLevel.GOOD)
    val qualityLevel: StateFlow<QualityLevel> = _qualityLevel.asStateFlow()

    private val _capturedImagePath = MutableStateFlow<String?>(null)
    val capturedImagePath: StateFlow<String?> = _capturedImagePath.asStateFlow()

    fun onCropSelected(crop: String) {
        _currentCrop.value = crop
    }

    fun updateQuality(level: QualityLevel) {
        _qualityLevel.value = level
    }

    fun onCaptureComplete(path: String) {
        _capturedImagePath.value = path
    }
}
