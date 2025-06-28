#!/usr/bin/env python3
"""
Working Gmail Alert Configuration Template
Update the app_password with your actual Gmail app password
"""

# Replace 'your-app-password-here' with your 16-character Gmail app password
GMAIL_APP_PASSWORD = "your-app-password-here"

# Your working Gmail alert configuration
GMAIL_ALERT_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": GMAIL_APP_PASSWORD,
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        }
    }
}

# Multi-channel config (email + webhook)
FULL_ALERT_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": GMAIL_APP_PASSWORD,
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        },
        "webhook": {
            "enabled": True,
            "url": "https://webhook.site/your-unique-url",  # Replace with your webhook URL
            "method": "POST",
            "headers": {
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            }
        }
    }
}
