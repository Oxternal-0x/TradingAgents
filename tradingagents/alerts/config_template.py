"""
Alert Configuration Template

Copy this template to create your alert configuration.
Update the settings with your actual credentials and preferences.
"""

ALERT_CONFIG_TEMPLATE = {
    # Global alert settings
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],  # Don't alert on HOLD by default
    
    # Notification handlers configuration
    "notification_handlers": {
        
        # Desktop notifications (works on most systems)
        "desktop": {
            "enabled": True,
        },
        
        # Email notifications via SMTP
        "email": {
            "enabled": False,  # Set to True to enable
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your-email@gmail.com",
            "sender_password": "your-app-password",  # Use app password for Gmail
            "recipient_emails": [
                "your-email@gmail.com",
                # "trader@yourcompany.com"
            ]
        },
        
        # SMS notifications via Twilio
        "sms": {
            "enabled": False,  # Set to True to enable
            "twilio_account_sid": "your-twilio-account-sid",
            "twilio_auth_token": "your-twilio-auth-token", 
            "twilio_from_number": "+1234567890",
            "recipient_numbers": [
                "+1234567890",
                # "+0987654321"
            ]
        },
        
        # Slack notifications via webhook
        "slack": {
            "enabled": False,  # Set to True to enable
            "slack_webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
            "slack_channel": "#trading-alerts",
            "slack_username": "Trading Bot"
        },
        
        # Custom webhook notifications
        "webhook": {
            "enabled": False,  # Set to True to enable
            "webhook_url": "https://your-webhook-endpoint.com/alerts",
            "webhook_headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer your-token"
            },
            "webhook_timeout": 10
        }
    }
}

# Quick setup configurations for common scenarios

# Configuration for desktop-only alerts (default)
DESKTOP_ONLY_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    "notification_handlers": {
        "desktop": {"enabled": True}
    }
}

# Configuration for email alerts
def create_email_config(sender_email: str, sender_password: str, recipient_emails: list):
    """Create email-only alert configuration."""
    return {
        "alerts_enabled": True,
        "alert_on_decisions": ["BUY", "SELL"], 
        "notification_handlers": {
            "email": {
                "enabled": True,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": sender_email,
                "sender_password": sender_password,
                "recipient_emails": recipient_emails
            }
        }
    }

# Configuration for Slack alerts
def create_slack_config(webhook_url: str, channel: str = "#trading-alerts"):
    """Create Slack-only alert configuration."""
    return {
        "alerts_enabled": True,
        "alert_on_decisions": ["BUY", "SELL"],
        "notification_handlers": {
            "slack": {
                "enabled": True,
                "slack_webhook_url": webhook_url,
                "slack_channel": channel,
                "slack_username": "Trading Bot"
            }
        }
    }

# Multi-channel configuration
def create_multi_channel_config(email_config: dict = None, slack_config: dict = None, sms_config: dict = None):
    """Create multi-channel alert configuration."""
    config = {
        "alerts_enabled": True,
        "alert_on_decisions": ["BUY", "SELL"],
        "notification_handlers": {
            "desktop": {"enabled": True}
        }
    }
    
    if email_config is not None:
        config["notification_handlers"]["email"] = {
            "enabled": True,
            **email_config
        }
    
    if slack_config is not None:
        config["notification_handlers"]["slack"] = {
            "enabled": True,
            **slack_config
        }
    
    if sms_config is not None:
        config["notification_handlers"]["sms"] = {
            "enabled": True,
            **sms_config
        }
    
    return config