package com.aashis.bot

import android.app.*
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.WindowManager
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast

class FloatingService : Service() {
    private var windowManager: WindowManager? = null
    private var panel: LinearLayout? = null

    override fun onCreate() {
        super.onCreate()
        createNotification()
        showFloatingPanel()
    }

    private fun createNotification() {
        val channelId = "aashis_bot_service"
        val manager = getSystemService(NotificationManager::class.java)
        manager.createNotificationChannel(
            NotificationChannel(
                channelId,
                "AASHIS BOT",
                NotificationManager.IMPORTANCE_LOW
            )
        )

        val notification = Notification.Builder(this, channelId)
            .setContentTitle("AASHIS BOT")
            .setContentText("Floating control is active")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .build()

        startForeground(1, notification)
    }

    private fun showFloatingPanel() {
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager

        val box = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(14, 10, 14, 10)
            setBackgroundColor(Color.rgb(25, 25, 25))
        }

        val title = TextView(this).apply {
            text = "AASHIS BOT"
            textSize = 14f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
        }

        val start = TextView(this).apply {
            text = "START"
            textSize = 15f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            setPadding(18, 10, 18, 10)
            setBackgroundColor(Color.rgb(20, 130, 70))
            setOnClickListener {
                text = "STARTED"
                Toast.makeText(
                    this@FloatingService,
                    "AI engine connection is not ready yet",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }

        box.addView(title)
        box.addView(start)
        panel = box

        val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        else
            WindowManager.LayoutParams.TYPE_PHONE

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.END
            x = 20
            y = 180
        }

        windowManager?.addView(box, params)
    }

    override fun onDestroy() {
        panel?.let { windowManager?.removeView(it) }
        panel = null
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
