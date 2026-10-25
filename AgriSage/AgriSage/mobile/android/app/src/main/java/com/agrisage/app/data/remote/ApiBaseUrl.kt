package com.agrisage.app.data.remote

import java.net.URI

/**
 * Normalizes the configured API origin into the Retrofit base URL.
 *
 * The backend exposes its mobile contract below /api/v1. Debug builds may use
 * the emulator's local HTTP endpoint; release builds are HTTPS-only.
 */
object ApiBaseUrl {
    fun normalized(raw: String, allowInsecureHttp: Boolean): String {
        val value = raw.trim().trimEnd('/')
        require(value.isNotEmpty()) { "API_BASE_URL is empty" }

        val uri = runCatching { URI(value) }
            .getOrElse { throw IllegalArgumentException("API_BASE_URL is not a valid URL", it) }
        val scheme = uri.scheme?.lowercase()
        require(scheme == "https" || (allowInsecureHttp && scheme == "http")) {
            "API_BASE_URL must use HTTPS outside debug builds"
        }
        require(!uri.host.isNullOrBlank()) { "API_BASE_URL must include a host" }
        require(uri.userInfo == null && uri.query == null && uri.fragment == null) {
            "API_BASE_URL must not include credentials, query parameters, or fragments"
        }

        val path = uri.path.trimEnd('/')
        require(path.isEmpty() || path == "/api/v1") {
            "API_BASE_URL path must be empty or /api/v1"
        }

        val authority = uri.rawAuthority
        val origin = "$scheme://$authority"
        return if (path == "/api/v1") "$origin/api/v1/" else "$origin/api/v1/"
    }
}
