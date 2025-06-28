#!/usr/bin/env python3
"""
Personalized Alert Configuration
"""

from tradingagents.alerts.config_template import create_email_config, create_multi_channel_config

# Your personalized alert configuration
PERSONAL_ALERT_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],  # Get alerts for actionable signals
    
    "notification_handlers": {
        # Desktop notifications (immediate local alerts)
        "desktop": {
            "enabled": True,
        },
        
        # Email notifications to your Gmail
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": "your-app-password-here",  # You'll need to set this
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        },
        
        # Webhook for custom integrations (using your API key)
        "webhook": {
            "enabled": True,
            "url": "https://api.openrouter.ai/api/v1/webhooks/trading-alerts",  # Example URL
            "method": "POST",
            "headers": {
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            }
        }
    }
}

# Email-only configuration (simpler setup)
EMAIL_ONLY_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": "your-app-password-here",  # Set your Gmail app password
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        }
    }
}

# Desktop + Webhook configuration (no email setup needed)
DESKTOP_WEBHOOK_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "desktop": {
            "enabled": True,
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

# Multi-channel configuration (Email + Telegram + Webhook)
FULL_ALERT_SYSTEM = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "email": {
            "enabled": False,  # Set to True and add your Gmail app password
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": "your-app-password-here",
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        },
        "telegram": {
            "enabled": False,  # Set to True and add your bot credentials
            "bot_token": "your-bot-token-here",
            "chat_id": "your-chat-id-here",
            "parse_mode": "Markdown",
            "disable_notification": False,
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