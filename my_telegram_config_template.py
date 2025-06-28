#!/usr/bin/env python3
"""
My Telegram Alert Configuration Template

INSTRUCTIONS:
1. Replace BOT_TOKEN with your actual bot token from BotFather
2. Replace CHAT_ID with your actual chat ID
3. Save this file as 'my_telegram_config.py'
4. Test with: python3 test_my_telegram.py
"""

# Replace these with your actual credentials
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your bot token from BotFather
CHAT_ID = "123456789"  # Your chat ID (find with getUpdates)

# Telegram alert configuration
TELEGRAM_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "telegram": {
            "enabled": True,
            "bot_token": BOT_TOKEN,
            "chat_id": CHAT_ID,
            "parse_mode": "Markdown",
            "disable_notification": False,
        }
    }
}

# Multi-channel configuration (Telegram + Email + Webhook)
FULL_TELEGRAM_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "telegram": {
            "enabled": True,
            "bot_token": BOT_TOKEN,
            "chat_id": CHAT_ID,
            "parse_mode": "Markdown",
            "disable_notification": False,
        },
        "email": {
            "enabled": False,  # Set to True and configure
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": "your-gmail-app-password-here",
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        },
        "webhook": {
            "enabled": True,
            "url": "https://webhook.site/your-unique-url",
            "method": "POST",
            "headers": {
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            }
        }
    }
}

# Usage instructions:
"""
To use this configuration in your trading system:

1. Save as 'my_telegram_config.py' with your actual credentials
2. Import in your trading script:
   from my_telegram_config import TELEGRAM_CONFIG
   
3. Use in your trading graph:
   config['alert_config'] = TELEGRAM_CONFIG
"""