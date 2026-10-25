package com.agrisage.app.ui.screens.alerts

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrisage.app.data.local.entity.AlertEntity
import com.agrisage.app.data.repository.AlertRepository
import com.agrisage.app.ui.screens.home.AlertItem
import com.agrisage.app.ui.screens.home.AlertSeverity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AlertsUiState(
    val allAlerts: List<AlertItem> = emptyList(),
    val filteredAlerts: List<AlertItem> = emptyList(),
    val selectedFilter: AlertSeverity? = null,
    val isLoading: Boolean = false,
    val unreadCount: Int = 0,
    val status: AlertsDataStatus = AlertsDataStatus.LOADING,
    val error: String? = null
)

enum class AlertsDataStatus { LOADING, AVAILABLE, UNAVAILABLE }

@HiltViewModel
class AlertsViewModel @Inject constructor(
    private val alertRepository: AlertRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AlertsUiState())
    val uiState: StateFlow<AlertsUiState> = _uiState.asStateFlow()

    init {
        observeLocalAlerts()
        refresh()
    }

    fun refresh() {
        if (_uiState.value.isLoading) return

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            val response = runCatching { alertRepository.refreshAlerts() }.getOrNull()
            _uiState.update { current ->
                val hasCachedAlerts = current.allAlerts.isNotEmpty()
                current.copy(
                    isLoading = false,
                    status = if (response?.isSuccessful == true || hasCachedAlerts) {
                        AlertsDataStatus.AVAILABLE
                    } else {
                        AlertsDataStatus.UNAVAILABLE
                    },
                    error = when {
                        response == null -> "Alert provider is unavailable."
                        !response.isSuccessful -> "Alerts could not be loaded."
                        else -> null
                    }
                )
            }
        }
    }

    fun filterBySeverity(severity: AlertSeverity?) {
        _uiState.update { current ->
            val filtered = if (severity == null) {
                current.allAlerts
            } else {
                current.allAlerts.filter { it.severity == severity }
            }
            current.copy(selectedFilter = severity, filteredAlerts = filtered)
        }
    }

    fun markAsRead(alertId: String) {
        viewModelScope.launch {
            alertRepository.markAsRead(alertId)
        }
    }

    fun markAllAsRead() {
        viewModelScope.launch {
            alertRepository.markAllAsRead()
            _uiState.update { it.copy(unreadCount = 0) }
        }
    }

    private fun observeLocalAlerts() {
        viewModelScope.launch {
            alertRepository.getLocalAlerts()
                .catch { error ->
                    _uiState.update {
                        it.copy(
                            status = if (it.allAlerts.isNotEmpty()) {
                                AlertsDataStatus.AVAILABLE
                            } else {
                                AlertsDataStatus.UNAVAILABLE
                            },
                            error = error.message ?: "Local alert data is unavailable."
                        )
                    }
                }
                .collect { entities ->
                    val alerts = entities.mapNotNull { it.toAlertItem() }
                    _uiState.update { current ->
                        current.copy(
                            allAlerts = alerts,
                            filteredAlerts = filterAlerts(alerts, current.selectedFilter),
                            unreadCount = alerts.count { !it.isRead },
                            status = if (alerts.isNotEmpty() || current.status == AlertsDataStatus.AVAILABLE) {
                                AlertsDataStatus.AVAILABLE
                            } else {
                                current.status
                            }
                        )
                    }
                }
        }
    }

    private fun filterAlerts(
        alerts: List<AlertItem>,
        severity: AlertSeverity?
    ): List<AlertItem> = severity?.let { selected ->
        alerts.filter { it.severity == selected }
    } ?: alerts

    private fun AlertEntity.toAlertItem(): AlertItem? {
        val alertId = id.trim().takeIf(String::isNotEmpty) ?: return null
        val alertTitle = title.trim().takeIf(String::isNotEmpty) ?: return null
        val alertMessage = message.trim().takeIf(String::isNotEmpty) ?: return null
        val displaySeverity = severity.trim().uppercase().takeIf(String::isNotEmpty) ?: return null
        val mappedSeverity = when (displaySeverity) {
            "CRITICAL" -> AlertSeverity.CRITICAL
            "WARNING", "HIGH", "MEDIUM" -> AlertSeverity.WARNING
            "SUCCESS" -> AlertSeverity.SUCCESS
            "INFO", "LOW" -> AlertSeverity.INFO
            else -> AlertSeverity.INFO
        }

        return AlertItem(
            id = alertId,
            severity = mappedSeverity,
            title = alertTitle,
            message = alertMessage,
            isRead = isRead,
            severityLabel = displaySeverity
        )
    }
}
