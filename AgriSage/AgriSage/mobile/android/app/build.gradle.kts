import java.net.URI
import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
}

// google-services.json is deliberately a developer/CI secret and is not part
// of a clean checkout. Apply the plugin only when a real file is supplied;
// release tasks below fail closed instead of silently shipping without FCM.
// Reference fixtures are opt-in and installed separately from a real account.
val referencePreview = providers.gradleProperty("referencePreview")
    .map { it.toBooleanStrict() }.getOrElse(false)
if (referencePreview) {
    // Keep the verified real-data APK/reports when assembling the visual preview.
    layout.buildDirectory.set(layout.projectDirectory.dir("build/reference-preview"))
}
val googleServicesFile = file("google-services.json")
val hasGoogleServices = googleServicesFile.isFile
if (hasGoogleServices && !referencePreview) {
    apply(plugin = "com.google.gms.google-services")
}

val localProperties = Properties().apply {
    rootProject.file("local.properties").takeIf { it.isFile }?.inputStream()?.use(::load)
}

fun configuredValue(name: String): String? = sequenceOf(
    providers.gradleProperty(name).orNull,
    providers.environmentVariable(name).orNull,
    localProperties.getProperty(name),
).mapNotNull { it?.trim()?.takeIf(String::isNotEmpty) }.firstOrNull()

val configuredApiBaseUrl = configuredValue("API_BASE_URL")
    ?: configuredValue("apiBaseUrl")
val releaseTaskRequested = gradle.startParameter.taskNames.any { taskName ->
    taskName.contains("release", ignoreCase = true)
}

fun requireReleaseHttpsBaseUrl(value: String): String {
    val parsed = runCatching { URI(value) }.getOrElse {
        throw GradleException("API_BASE_URL must be a valid HTTPS URL for release builds")
    }
    val host = parsed.host?.lowercase()
    require(parsed.scheme.equals("https", ignoreCase = true)) {
        "API_BASE_URL must use HTTPS for release builds"
    }
    require(!host.isNullOrBlank()) { "API_BASE_URL must include a host for release builds" }
    require(host !in setOf("localhost", "127.0.0.1", "10.0.2.2")) {
        "API_BASE_URL must not point at a local development host in release builds"
    }
    require(parsed.userInfo == null && parsed.query == null && parsed.fragment == null) {
        "API_BASE_URL must not contain credentials, query parameters, or fragments"
    }
    return value.trimEnd('/')
}

val debugApiBaseUrl = configuredApiBaseUrl?.trimEnd('/') ?: "http://10.0.2.2:8000"
val releaseApiBaseUrl = if (releaseTaskRequested) {
    configuredApiBaseUrl?.let(::requireReleaseHttpsBaseUrl)
} else {
    configuredApiBaseUrl?.trimEnd('/')
}

fun buildConfigString(value: String): String =
    "\"${value.replace("\\", "\\\\").replace("\"", "\\\"")}\""

val releaseStoreFile = configuredValue("RELEASE_STORE_FILE")
val releaseStorePassword = configuredValue("RELEASE_STORE_PASSWORD")
val releaseKeyAlias = configuredValue("RELEASE_KEY_ALIAS")
val releaseKeyPassword = configuredValue("RELEASE_KEY_PASSWORD")
val hasReleaseSigning = listOf(
    releaseStoreFile,
    releaseStorePassword,
    releaseKeyAlias,
    releaseKeyPassword,
).all { !it.isNullOrBlank() }

if (releaseTaskRequested) {
    check(!referencePreview) { "Reference preview cannot be used for a release build" }
    check(releaseApiBaseUrl != null) {
        "Release builds require API_BASE_URL (Gradle property or environment variable) using HTTPS"
    }
    check(hasGoogleServices) {
        "Release builds require app/google-services.json from the Firebase project for com.agrisage.app"
    }
    check(hasReleaseSigning) {
        "Release builds require RELEASE_STORE_FILE, RELEASE_STORE_PASSWORD, RELEASE_KEY_ALIAS, and RELEASE_KEY_PASSWORD"
    }
    check(file(releaseStoreFile!!).isFile) {
        "RELEASE_STORE_FILE does not exist: $releaseStoreFile"
    }
}

android {
    namespace = "com.agrisage.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.agrisage.app"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        buildConfigField("String", "BASE_URL", buildConfigString(debugApiBaseUrl))
        buildConfigField("boolean", "REFERENCE_PREVIEW", "false")
        manifestPlaceholders["appLabel"] = "@string/app_name"
    }

    signingConfigs {
        create("release") {
            if (hasReleaseSigning) {
                storeFile = file(releaseStoreFile!!)
                storePassword = releaseStorePassword
                keyAlias = releaseKeyAlias
                keyPassword = releaseKeyPassword
            }
        }
    }

    buildTypes {
        debug {
            // Debug builds may target the Android emulator's local HTTP host.
            buildConfigField("String", "BASE_URL", buildConfigString(debugApiBaseUrl))
            buildConfigField("boolean", "REFERENCE_PREVIEW", referencePreview.toString())
            if (referencePreview) {
                applicationIdSuffix = ".preview"
                versionNameSuffix = "-reference"
                manifestPlaceholders["appLabel"] = "Agri-SAGE Reference"
            }
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            isDebuggable = false
            buildConfigField("String", "BASE_URL", buildConfigString(releaseApiBaseUrl ?: debugApiBaseUrl))
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.material.icons)
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.navigation.compose)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.hilt.navigation.compose)
    implementation(libs.androidx.hilt.work)
    ksp(libs.androidx.hilt.compiler)
    implementation(libs.retrofit)
    implementation(libs.retrofit.converter.gson)
    implementation(libs.okhttp)
    implementation(libs.okhttp.logging)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.work.runtime.ktx)
    implementation(libs.androidx.datastore.preferences)
    implementation(libs.coil.compose)
    implementation(libs.maps.compose)
    implementation(libs.firebase.messaging.ktx)

    debugImplementation(libs.androidx.compose.ui.tooling)

    testImplementation(libs.junit)
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:${libs.versions.coroutines.get()}")
    androidTestImplementation(libs.androidx.test.ext.junit)
    androidTestImplementation(libs.androidx.test.espresso)
    androidTestImplementation(platform(libs.androidx.compose.bom))
}
