package com.agrisage.app.util

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "agrisage_preferences")

/**
 * DataStoreManager handles offline local state persistence including:
 * - Onboarding completion flag
 * - Selected language code (en, hi, ml, ta, te, kn)
 * - Farmer profile details (state, district, phone)
 * - JWT auth tokens
 */
@Singleton
class DataStoreManager @Inject constructor(
    private val context: Context
) {
    companion object {
        val KEY_ONBOARDING_COMPLETED = booleanPreferencesKey("onboarding_completed")
        val KEY_SELECTED_LANGUAGE = stringPreferencesKey("selected_language")
        val KEY_FARMER_NAME = stringPreferencesKey("farmer_name")
        val KEY_FARMER_PHONE = stringPreferencesKey("farmer_phone")
        val KEY_FARMER_STATE = stringPreferencesKey("farmer_state")
        val KEY_FARMER_DISTRICT = stringPreferencesKey("farmer_district")
        val KEY_AUTH_TOKEN = stringPreferencesKey("auth_token")
        val KEY_OFFLINE_MODE = booleanPreferencesKey("offline_mode")
    }

    val isOnboardingCompleted: Flow<Boolean> = context.dataStore.data.map { prefs ->
        prefs[KEY_ONBOARDING_COMPLETED] ?: false
    }

    val selectedLanguage: Flow<String> = context.dataStore.data.map { prefs ->
        prefs[KEY_SELECTED_LANGUAGE] ?: "ml" // Default to Malayalam per spec / system default
    }

    val farmerName: Flow<String> = context.dataStore.data.map { prefs ->
        prefs[KEY_FARMER_NAME] ?: ""
    }

    val authToken: Flow<String?> = context.dataStore.data.map { prefs ->
        prefs[KEY_AUTH_TOKEN]
    }

    suspend fun setOnboardingCompleted(completed: Boolean) {
        context.dataStore.edit { prefs ->
            prefs[KEY_ONBOARDING_COMPLETED] = completed
        }
    }

    suspend fun setLanguage(langCode: String) {
        context.dataStore.edit { prefs ->
            prefs[KEY_SELECTED_LANGUAGE] = langCode
        }
    }

    suspend fun saveFarmerProfile(name: String, phone: String, state: String, district: String) {
        context.dataStore.edit { prefs ->
            prefs[KEY_FARMER_NAME] = name
            prefs[KEY_FARMER_PHONE] = phone
            prefs[KEY_FARMER_STATE] = state
            prefs[KEY_FARMER_DISTRICT] = district
        }
    }

    suspend fun saveAuthToken(token: String) {
        context.dataStore.edit { prefs ->
            prefs[KEY_AUTH_TOKEN] = token
        }
    }

    suspend fun clear() {
        context.dataStore.edit { prefs ->
            prefs.clear()
        }
    }
}
