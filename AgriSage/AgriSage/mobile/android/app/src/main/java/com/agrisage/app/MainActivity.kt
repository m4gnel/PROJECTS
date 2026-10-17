package com.agrisage.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.navigation.compose.rememberNavController
import com.agrisage.app.navigation.AgriSageNavGraph
import com.agrisage.app.ui.theme.AgriSageTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AgriSageTheme {
                val navController = rememberNavController()
                AgriSageNavGraph(navController = navController)
            }
        }
    }
}
