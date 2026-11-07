package com.aashis.bot

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = android.view.Gravity.CENTER
            setPadding(30, 30, 30, 30)
        }

        val title = TextView(this).apply {
            text = "AASHIS BOT"
            textSize = 25f
            gravity = android.view.Gravity.CENTER
        }

        val start = Button(this).apply {
            text = "START"
            textSize = 18f
            setOnClickListener {
                if (!Settings.canDrawOverlays(this@MainActivity)) {
                    val intent = Intent(
                        Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:$packageName")
                    )
                    startActivity(intent)
                } else {
                    startForegroundService(
                        Intent(this@MainActivity, FloatingService::class.java)
                    )
                    finish()
                }
            }
        }

        layout.addView(title)
        layout.addView(start)
        setContentView(layout)
    }
}
