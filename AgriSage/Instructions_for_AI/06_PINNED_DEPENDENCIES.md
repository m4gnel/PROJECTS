# 06_PINNED_DEPENDENCIES.md — Exact Dependency Files
# ⚠️ COPY THESE FILES VERBATIM. DO NOT CHANGE ANY VERSION NUMBER.

---

## backend/requirements.txt
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
asyncpg==0.29.0
alembic==1.13.2
pgvector==0.3.2
langgraph==1.0.8
langchain-core==0.3.15
langchain-google-genai==2.0.4
sentence-transformers==3.1.1
httpx==0.27.2
pydantic==2.9.2
pydantic-settings==2.5.2
apscheduler==3.10.4
websockets==13.1
feedparser==6.0.11
pypdf==4.3.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
```

## backend/requirements-dev.txt
```
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
pytest-cov==5.0.0
black==24.8.0
ruff==0.6.9
mypy==1.11.2
```

---

## android/gradle/libs.versions.toml
```toml
[versions]
kotlin = "2.0.0"
agp = "8.6.1"
composeBom = "2024.10.00"
navigationCompose = "2.8.5"
kotlinxSerializationJson = "1.7.3"
room = "2.7.0"
hilt = "2.51.1"
hiltNavigationCompose = "1.2.0"
retrofit = "2.11.0"
okhttp = "4.12.0"
coroutines = "1.9.0"
lifecycle = "2.8.6"
workmanager = "2.9.1"
datastore = "1.1.1"
coil = "2.7.0"
mapsCompose = "6.2.1"
firebaseMessaging = "24.0.2"
ksp = "2.0.0-1.0.23"

[libraries]
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-compose-material-icons = { group = "androidx.compose.material", name = "material-icons-extended" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version = "1.9.3" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerializationJson" }
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hiltNavigationCompose" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-converter-gson = { group = "com.squareup.retrofit2", name = "converter-gson", version.ref = "retrofit" }
okhttp = { group = "com.squareup.okhttp3", name = "okhttp", version.ref = "okhttp" }
okhttp-logging = { group = "com.squareup.okhttp3", name = "logging-interceptor", version.ref = "okhttp" }
kotlinx-coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycle" }
androidx-work-runtime-ktx = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "workmanager" }
androidx-datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }
coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }
maps-compose = { group = "com.google.maps.android", name = "maps-compose", version.ref = "mapsCompose" }
firebase-messaging-ktx = { group = "com.google.firebase", name = "firebase-messaging-ktx", version.ref = "firebaseMessaging" }
junit = { group = "junit", name = "junit", version = "4.13.2" }
androidx-test-ext-junit = { group = "androidx.test.ext", name = "junit", version = "1.2.1" }
androidx-test-espresso = { group = "androidx.test.espresso", name = "espresso-core", version = "3.6.1" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
google-services = { id = "com.google.gms.google-services", version = "4.4.2" }
```

---

## android/build.gradle.kts (PROJECT-LEVEL)
```kotlin
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.serialization) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.hilt) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.google.services) apply false
}
```

---

## android/app/build.gradle.kts (APP-LEVEL)
```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
    alias(libs.plugins.google.services)
}

android {
    namespace = "com.agrisage.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.agrisage.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        buildConfigField("String", "BASE_URL", "\"${System.getenv("RAILWAY_URL") ?: "http://10.0.2.2:8000"}\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = true
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
    androidTestImplementation(libs.androidx.test.ext.junit)
    androidTestImplementation(libs.androidx.test.espresso)
    androidTestImplementation(platform(libs.androidx.compose.bom))
}
```

---

## android/settings.gradle.kts
```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "AgriSage"
include(":app")
```

---

## backend/.env.example
```
# Backend environment variables — copy to .env and fill in
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/agrisage
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-jwt-secret-key-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1
NASA_EARTHDATA_BASE_URL=https://appeears.earthdatacloud.nasa.gov
DATA_GOV_IN_API_KEY=your-data-gov-in-key
NBAIR_RSS_URL=https://www.nbair.res.in/rss/pest-alerts.xml
NBSS_API_URL=https://www.nbsslup.in/api
KAU_PDF_DIR=./kau_pdfs
RAILWAY_URL=https://your-app.up.railway.app
ENVIRONMENT=development
```

---

## backend/railway.toml
```toml
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 60
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[services]]
name = "agrisage-backend"
```

---

## backend/Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
