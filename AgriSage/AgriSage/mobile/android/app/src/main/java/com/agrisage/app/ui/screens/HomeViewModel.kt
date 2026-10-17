package com.agrisage.app.ui.screens

import androidx.lifecycle.ViewModel
import com.agrisage.app.data.local.entities.CachedAdvisoryEntity
import com.agrisage.app.data.local.entities.FarmEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject

enum class ConnectivityStatus {
    ONLINE, LIMITED, OFFLINE
}

@HiltViewModel
class HomeViewModel @Inject constructor() : ViewModel() {
    private val _activeFarm = MutableStateFlow<FarmEntity?>(null)
    val activeFarm: StateFlow<FarmEntity?> = _activeFarm.asStateFlow()

    private val _morningBriefing = MutableStateFlow<CachedAdvisoryEntity?>(null)
    val morningBriefing: StateFlow<CachedAdvisoryEntity?> = _morningBriefing.asStateFlow()

    private val _connectivityStatus = MutableStateFlow(ConnectivityStatus.ONLINE)
    val connectivityStatus: StateFlow<ConnectivityStatus> = _connectivityStatus.asStateFlow()

    fun updateConnectivity(status: ConnectivityStatus) {
        _connectivityStatus.value = status
    }
}
