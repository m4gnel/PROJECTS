package com.agrisage.app.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.agrisage.app.data.local.entity.FieldEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface FieldDao {
    @Query("SELECT * FROM fields ORDER BY updatedAt DESC")
    fun getAllFields(): Flow<List<FieldEntity>>

    @Query("SELECT * FROM fields WHERE id = :fieldId LIMIT 1")
    fun getFieldById(fieldId: String): Flow<FieldEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertFields(fields: List<FieldEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertField(field: FieldEntity)

    @Query("DELETE FROM fields WHERE id = :fieldId")
    suspend fun deleteField(fieldId: String)
}
