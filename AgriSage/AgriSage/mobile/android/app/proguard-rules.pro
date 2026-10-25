# Agri-SAGE release shrinking rules.
# Retrofit/Gson DTO fields are kept because the backend contract is keyed by
# JSON names rather than Kotlin property names. Room and Hilt contribute their
# own consumer rules through their dependencies.
-keepattributes RuntimeVisibleAnnotations,RuntimeVisibleParameterAnnotations,AnnotationDefault,Signature
-keep class com.agrisage.app.data.remote.dto.** { *; }
-keep class com.agrisage.app.data.local.entity.** { *; }
-keep class com.agrisage.app.data.local.entities.** { *; }
-keepclassmembers class com.agrisage.app.data.remote.dto.** {
    @com.google.gson.annotations.SerializedName <fields>;
}
-keep interface com.agrisage.app.data.remote.ApiService { *; }
-keep interface com.agrisage.app.data.remote.AuthRefreshApi { *; }
-keep class com.agrisage.app.AgriSageFirebaseMessagingService { *; }

# Gson can encounter generic collection types in sync payloads.
-keep class com.google.gson.reflect.TypeToken { *; }
-keep class * extends com.google.gson.reflect.TypeToken
