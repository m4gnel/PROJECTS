package com.agrisage.app.di

import android.content.Context
import androidx.room.Room
import com.agrisage.app.data.local.AppDatabase
import com.agrisage.app.data.local.dao.AlertDao
import com.agrisage.app.data.local.dao.ChatDao
import com.agrisage.app.data.local.dao.FieldDao
import com.agrisage.app.data.local.dao.WeatherDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "agrisage_app_db"
        ).fallbackToDestructiveMigration().build()
    }

    @Provides
    fun provideWeatherDao(db: AppDatabase): WeatherDao = db.weatherDao()

    @Provides
    fun provideAlertDao(db: AppDatabase): AlertDao = db.alertDao()

    @Provides
    fun provideChatDao(db: AppDatabase): ChatDao = db.chatDao()

    @Provides
    fun provideFieldDao(db: AppDatabase): FieldDao = db.fieldDao()
}
