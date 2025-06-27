# 🚨 Trading Agents Alert System

**Get instant notifications when your trading system generates BUY or SELL signals!**

The Trading Agents Alert System seamlessly integrates with your existing trading analysis to provide real-time notifications through multiple channels including email, SMS, Slack, desktop notifications, and custom webhooks.

## ✨ Key Features

- 📱 **Multi-Channel Alerts**: Email, SMS, Slack, Desktop, Webhooks
- 🎯 **Smart Filtering**: Only alert on actionable signals (BUY/SELL)
- 📊 **Rich Content**: Include analysis summaries and key insights
- 🛡️ **Rate Limiting**: Prevent alert spam with intelligent cooldowns
- 🔧 **Easy Setup**: Template-based configuration
- 🧪 **Testing Built-in**: Test your alerts before going live

## 🚀 Quick Start (2 minutes)

### Step 1: Install Optional Dependencies
```bash
pip install plyer  # For desktop notifications
```

### Step 2: Add Alerts to Your Trading System
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.alerts.config_template import DESKTOP_ONLY_CONFIG

# Add alert config to your existing setup
config = DEFAULT_CONFIG.copy()
config["alert_config"] = DESKTOP_ONLY_CONFIG  # Enable desktop alerts

# Initialize with alerts
ta = TradingAgentsGraph(config=config)

# Test alerts (optional)
ta.test_alerts()

# Run your analysis as usual - alerts sent automatically!
final_state, decision = ta.propagate("NVDA", "2024-05-10")
```

### Step 3: Run the Test
```bash
python test_alerts.py
```

That's it! You'll now get desktop notifications whenever your system generates BUY or SELL signals.

## 📧 More Alert Types

### Email Alerts
```python
from tradingagents.alerts.config_template import create_email_config

email_config = create_email_config(
    sender_email="your-email@gmail.com",
    sender_password="your-app-password",  # Gmail app password
    recipient_emails=["alerts@yourcompany.com"]
)

config["alert_config"] = email_config
```

### Slack Alerts
```python
from tradingagents.alerts.config_template import create_slack_config

slack_config = create_slack_config(
    webhook_url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    channel="#trading-alerts"
)

config["alert_config"] = slack_config
```

### SMS Alerts (via Twilio)
```python
# First: pip install twilio
sms_config = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    "notification_handlers": {
        "sms": {
            "enabled": True,
            "twilio_account_sid": "your-twilio-sid",
            "twilio_auth_token": "your-twilio-token",
            "twilio_from_number": "+1234567890",
            "recipient_numbers": ["+1987654321"]
        }
    }
}

config["alert_config"] = sms_config
```

## 🔄 Continuous Monitoring

For 24/7 monitoring with automatic alerts:

```bash
python examples/continuous_monitoring.py
```

This script:
- Monitors multiple stocks continuously
- Runs analysis at configurable intervals (default: every 4 hours)
- Sends alerts automatically on BUY/SELL signals
- Includes intelligent rate limiting
- Logs all activities

## 📱 What Alerts Look Like

### Desktop Notification
```
🚨 Trade Alert: BUY NVDA
Decision: BUY
Date: 2024-05-10
Time: 14:30:15
```

### Email Alert
Rich HTML email with:
- Color-coded decision (green for BUY, red for SELL)
- Analysis date and time
- Summary of key insights
- Links to full analysis data

### Slack Alert
Formatted message with:
- Emoji indicators (📈 for BUY, 📉 for SELL)
- Structured fields for easy reading
- Timestamp and ticker information

## 🛠️ Configuration Options

### Global Settings
```python
{
    "alerts_enabled": True,              # Enable/disable all alerts
    "alert_on_decisions": ["BUY", "SELL"], # Which decisions trigger alerts
}
```

### Supported Notification Handlers
- **Desktop**: Works on Windows, macOS, Linux
- **Email**: SMTP-based (Gmail, Outlook, Yahoo, custom)
- **SMS**: Via Twilio API
- **Slack**: Via webhook integration
- **Webhook**: Custom HTTP endpoints

## 🧪 Testing Your Setup

```python
# Test all configured alert handlers
ta.test_alerts()

# Check alert system status
status = ta.get_alert_status()
print(status)

# Temporarily disable alerts
ta.alert_manager.disable_alerts()

# Re-enable alerts
ta.alert_manager.enable_alerts()
```

## 📁 File Structure

```
tradingagents/alerts/
├── __init__.py              # Package initialization
├── alert_manager.py         # Main alert coordination
├── notification_handlers.py # All notification implementations
├── config_template.py       # Configuration templates
└── README.md               # Detailed documentation

examples/
├── alerts_example.py        # Basic setup examples
└── continuous_monitoring.py # 24/7 monitoring script

test_alerts.py              # Quick test script
README_ALERTS.md           # This file
requirements-alerts.txt    # Optional dependencies
```

## 🔒 Security Best Practices

- Store credentials in environment variables
- Use app passwords for email (not main passwords)
- Regularly rotate API keys and tokens
- Consider webhook authentication for production
- Test with small amounts before going live

## 🆘 Troubleshooting

### Desktop notifications not working?
```bash
pip install plyer
```

### Email authentication failed?
- Use Gmail app password, not your regular password
- Enable 2-factor authentication first
- Check SMTP server settings

### SMS not sending?
- Verify Twilio credentials
- Check phone number format (+1234567890)
- Ensure Twilio account has credits

### Slack webhook failing?
- Verify webhook URL is correct
- Check app permissions for the channel
- Test webhook with curl

## 🎯 Advanced Use Cases

### Trading Team Coordination
Set up different alert channels for different team members:
- Traders get SMS for immediate action
- Analysts get email for detailed reports
- Team Slack gets all signals for coordination

### Risk Management
Configure alerts for specific scenarios:
- Only BUY alerts during bull markets
- All signals during high volatility periods
- Custom webhook to trading platform API

### Portfolio Management
- Monitor multiple portfolios with different alert configs
- Rate-limited alerts to prevent decision fatigue
- Integration with position sizing systems

## 🤝 Contributing

Want to add a new notification type?

1. Inherit from `NotificationHandler` in `notification_handlers.py`
2. Implement `send_notification()` and `is_configured()` methods
3. Add initialization logic to `AlertManager`
4. Update configuration templates
5. Add tests and documentation

## 📞 Support

If you encounter issues:
1. Run `python test_alerts.py` for basic diagnostics
2. Check logs for detailed error messages
3. Review the troubleshooting section above
4. File an issue with your configuration (sanitized)

---

**Ready to get alerted on your next winning trade? Start with the 2-minute setup above! 🚀**