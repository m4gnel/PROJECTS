package com.agrisage.app.util

import android.content.Context
import android.content.Intent
import android.speech.RecognizerIntent

class SpeechRecognitionHelper(private val context: Context) {

    fun createRecognitionIntent(): Intent {
        return Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "ml-IN")
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "ml-IN")
            putExtra(RecognizerIntent.EXTRA_ONLY_RETURN_LANGUAGE_PREFERENCE, false)
            putExtra(RecognizerIntent.EXTRA_PROMPT, "സംസാരിക്കുക...") // "Speak..." in Malayalam
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
        }
    }

    fun extractResult(data: Intent?): String? {
        return data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull()
    }
}
