package com.agrisage.app

import android.app.Application
import androidx.work.*
import com.agrisage.app.data.sync.SyncWorker
import dagger.hilt.android.HiltAndroidApp
import java.util.concurrent.TimeUnit

@HiltAndroidApp
class AgriSAGEApplication : Application() {

    override fun onCreate() {
        super.onCreate()
        setupPeriodicSyncWorker()
    }

    private fun setupPeriodicSyncWorker() {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()

        val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
            .setConstraints(constraints)
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 1, TimeUnit.MINUTES)
            .build()

        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "AgriSAGE_PeriodicSync",
            ExistingPeriodicWorkPolicy.KEEP,
            syncRequest
        )
    }
}

typealias AgriSageApplication = AgriSAGEApplication

