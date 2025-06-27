# Trading Agents Alert System

The Trading Agents Alert System provides real-time notifications when your trading system generates BUY or SELL signals. Get alerted via multiple channels including email, SMS, Slack, desktop notifications, and custom webhooks.

## 🚨 Features

- **Multiple Notification Channels**: Email, SMS, Slack, Desktop, Webhooks
- **Smart Filtering**: Only alert on BUY/SELL decisions (configurable)  
- **Rich Alerts**: Include analysis summary and key metrics
- **Easy Configuration**: Template-based setup
- **Reliable Delivery**: Multiple fallback options
- **Rate Limiting**: Prevent alert spam

## 📦 Installation

### Required Dependencies
```bash
pip install requests
```

### Optional Dependencies
For specific notification types:

```bash
# For desktop notifications
pip install plyer

# For SMS notifications via Twilio
pip install twilio

# Email notifications use built-in Python libraries (no extra dependencies)
```

## 🚀 Quick Start

### 1. Desktop Notifications (Easiest)
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.alerts.config_template import DESKTOP_ONLY_CONFIG

# Create config with desktop alerts
config = DEFAULT_CONFIG.copy()
config["alert_config"] = DESKTOP_ONLY_CONFIG

# Initialize trading system with alerts
ta = TradingAgentsGraph(debug=True, config=config)

# Test alerts
ta.test_alerts()

# Run analysis - alerts will be sent automatically on BUY/SELL
final_state, decision = ta.propagate("NVDA", "2024-05-10")
```

### 2. Email Notifications
```python
from tradingagents.alerts.config_template import create_email_config

# Configure email alerts
email_config = create_email_config(
    sender_email="your-email@gmail.com",
    sender_password="your-app-password",  # Gmail app password
    recipient_emails=["trader1@example.com", "trader2@example.com"]
)

config = DEFAULT_CONFIG.copy()
config["alert_config"] = email_config

ta = TradingAgentsGraph(config=config)
```

### 3. Slack Notifications
```python
from tradingagents.alerts.config_template import create_slack_config

# Configure Slack alerts
slack_config = create_slack_config(
    webhook_url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    channel="#trading-alerts"
)

config = DEFAULT_CONFIG.copy()
config["alert_config"] = slack_config

ta = TradingAgentsGraph(config=config)
```

## ⚙️ Configuration

### Complete Configuration Template
```python
ALERT_CONFIG = {
    # Global settings
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],  # Don't alert on HOLD
    
    "notification_handlers": {
        # Desktop notifications
        "desktop": {
            "enabled": True
        },
        
        # Email notifications
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your-email@gmail.com",
            "sender_password": "your-app-password",
            "recipient_emails": ["alerts@yourcompany.com"]
        },
        
        # SMS via Twilio
        "sms": {
            "enabled": True,
            "twilio_account_sid": "your-account-sid",
            "twilio_auth_token": "your-auth-token",
            "twilio_from_number": "+1234567890",
            "recipient_numbers": ["+1987654321"]
        },
        
        # Slack notifications
        "slack": {
            "enabled": True,
            "slack_webhook_url": "https://hooks.slack.com/services/...",
            "slack_channel": "#trading-alerts",
            "slack_username": "Trading Bot"
        },
        
        # Custom webhook
        "webhook": {
            "enabled": True,
            "webhook_url": "https://your-webhook.com/alerts",
            "webhook_headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer your-token"
            }
        }
    }
}
```

## 📧 Setting Up Email Alerts

### Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the app password in your configuration

### Other Email Providers
- **Outlook**: Use `smtp.office365.com:587`
- **Yahoo**: Use `smtp.mail.yahoo.com:587` 
- **Custom SMTP**: Configure your server details

## 📱 Setting Up SMS Alerts

1. Create a [Twilio](https://www.twilio.com/) account
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase a Twilio phone number
4. Configure in your alert config:

```python
"sms": {
    "enabled": True,
    "twilio_account_sid": "AC1234567890abcdef...",
    "twilio_auth_token": "your-auth-token",
    "twilio_from_number": "+1234567890",
    "recipient_numbers": ["+1987654321", "+1555666777"]
}
```

## 💬 Setting Up Slack Alerts

1. Create a Slack App:
   - Go to [Slack API](https://api.slack.com/apps)
   - Create New App → From scratch
   - Choose your workspace

2. Enable Incoming Webhooks:
   - Go to "Incoming Webhooks" in your app settings
   - Turn on "Activate Incoming Webhooks"
   - Click "Add New Webhook to Workspace"
   - Choose the channel and authorize

3. Copy the webhook URL to your config

## 🔄 Continuous Monitoring

Use the continuous monitoring script for ongoing alerts:

```bash
python examples/continuous_monitoring.py
```

This script:
- Monitors multiple stocks continuously
- Runs analysis at configurable intervals  
- Sends alerts automatically on signals
- Includes rate limiting to prevent spam
- Logs all activities

## 🧪 Testing Alerts

Test your alert configuration:

```python
# Test all configured alert handlers
ta.test_alerts()

# Check alert system status
status = ta.get_alert_status()
print(status)
```

## 📊 Alert Content

Alerts include:
- **Ticker Symbol** and **Decision** (BUY/SELL)
- **Date and Time** of analysis
- **Analysis Summary** with key insights
- **Full Analysis Data** (for webhooks)

### Email Alert Example
```
🚨 Trade Alert: BUY NVDA

Date: 2024-05-10
Time: 14:30:15
Decision: BUY

Analysis Summary:
Market analysis indicates strong bullish momentum with RSI at 65...

Key Metrics:
✓ Market Analysis: Available
✓ Sentiment Analysis: Available  
✓ News Analysis: Available
✓ Fundamentals: Available
```

## 🛠️ Advanced Usage

### Custom Alert Logic
```python
# Only alert on specific decisions
config["alert_config"]["alert_on_decisions"] = ["BUY"]  # Only BUY alerts

# Disable alerts temporarily
ta.alert_manager.disable_alerts()

# Re-enable alerts
ta.alert_manager.enable_alerts()
```

### Webhook Payload Format
```json
{
    "alert_type": "trade_signal",
    "ticker": "NVDA",
    "decision": "BUY", 
    "date": "2024-05-10",
    "timestamp": "14:30:15",
    "summary": "Trading decision summary...",
    "full_analysis": {
        "market_report": "...",
        "sentiment_report": "...",
        "news_report": "...",
        "fundamentals_report": "..."
    }
}
```

## 🔧 Troubleshooting

### Common Issues

**Desktop notifications not working:**
```bash
pip install plyer
```

**Email authentication failed:**
- Use app password, not regular password
- Check SMTP settings for your provider
- Verify 2FA is enabled

**SMS not sending:**
- Verify Twilio credentials
- Check phone number format (+1234567890)
- Ensure Twilio account has sufficient credits

**Slack webhook failing:**
- Check webhook URL is correct
- Verify app has permission to post to channel
- Test webhook URL with curl

### Logs and Debugging

Check logs for detailed error information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Examples

See the `examples/` directory for:
- `alerts_example.py` - Basic alert setup examples
- `continuous_monitoring.py` - Continuous monitoring with alerts

## 🔒 Security Notes

- Store credentials securely (environment variables recommended)
- Use app passwords for email, not main passwords
- Regularly rotate API keys and tokens
- Consider webhook authentication for production use

## 🤝 Contributing

To add new notification handlers:

1. Inherit from `NotificationHandler`
2. Implement `send_notification()` and `is_configured()` methods
3. Add to `AlertManager._initialize_handlers()`
4. Update configuration templates

## 📄 License

Part of the Trading Agents project. See main project license.