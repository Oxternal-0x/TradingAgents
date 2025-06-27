# 🚨 TradingAgents Trade Entry Alert Monitor

A comprehensive alerting system for the TradingAgents framework that monitors for BUY signals (trade entries) and sends real-time alerts via multiple channels.

## 🌟 Features

- **Multi-Ticker Monitoring**: Monitor multiple stocks simultaneously
- **Smart Alert Deduplication**: Prevents duplicate alerts for the same signals
- **Multiple Alert Channels**: 
  - 📧 Email alerts with detailed analysis
  - 💬 Discord webhook notifications
  - 📱 Slack webhook notifications
- **Flexible Scheduling**: Manual, hourly, or daily monitoring
- **Rich Analysis Context**: Includes confidence indicators and analysis summaries
- **Persistent Alert History**: Tracks what's already been alerted
- **Systemd Service Support**: Run as a background service

## 🚀 Quick Start

### 1. Installation

First, ensure you have the TradingAgents framework installed, then add the alert monitor dependencies:

```bash
# Install additional dependencies
pip install schedule

# Or install from requirements.txt (schedule is already added)
pip install -r requirements.txt
```

### 2. Setup

Run the setup script to create configuration files:

```bash
python alert_setup.py
```

This creates:
- `alert_config.env` - Configuration template
- `test_alerts.py` - Test script
- `tradingagents-alerts.service` - Systemd service file

### 3. Configuration

Edit `alert_config.env` with your API keys and alert preferences:

```bash
# Required API Keys
export FINNHUB_API_KEY="your_finnhub_api_key"
export OPENAI_API_KEY="your_openai_api_key"

# Email Configuration (optional)
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAILS="alert1@email.com,alert2@email.com"

# Discord Webhook (optional)
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK"

# Slack Webhook (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WEBHOOK"
```

Load the configuration:

```bash
source alert_config.env
```

### 4. Test the System

```bash
python test_alerts.py
```

## 📊 Usage Examples

### Manual Single Check

Check specific tickers once:

```bash
python trade_alert_monitor.py --tickers SPY AAPL MSFT
```

### Manual Check with Date

Check for a specific date:

```bash
python trade_alert_monitor.py --tickers SPY AAPL --date 2024-12-06
```

### Automated Daily Monitoring

Run daily at market open (9:30 AM):

```bash
python trade_alert_monitor.py --schedule daily --tickers SPY QQQ AAPL MSFT GOOGL
```

### Automated Hourly Monitoring

Run every hour during market hours:

```bash
python trade_alert_monitor.py --schedule hourly --tickers SPY QQQ
```

## 🛠️ Configuration Options

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FINNHUB_API_KEY` | ✅ | FinnHub API key for market data |
| `OPENAI_API_KEY` | ✅ | OpenAI API key for LLM analysis |
| `SENDER_EMAIL` | ⚠️ | Email address for sending alerts |
| `SENDER_PASSWORD` | ⚠️ | Email password/app password |
| `RECIPIENT_EMAILS` | ⚠️ | Comma-separated list of recipient emails |
| `DISCORD_WEBHOOK_URL` | ⚠️ | Discord webhook URL |
| `SLACK_WEBHOOK_URL` | ⚠️ | Slack webhook URL |

⚠️ = Optional but required for that alert channel

### Command Line Arguments

```bash
python trade_alert_monitor.py --help
```

- `--tickers`: List of tickers to monitor (default: SPY QQQ AAPL)
- `--date`: Specific date to analyze (YYYY-MM-DD, default: today)
- `--schedule`: Schedule type (manual/daily/hourly, default: manual)
- `--create-config`: Create sample configuration file

## 📧 Alert Examples

### Email Alert
Rich HTML email with:
- Trade entry details (ticker, date, decision)
- Risk assessment level
- Analysis summary from all agents
- Confidence indicators

### Discord Alert
Embedded message with:
- Trade entry notification
- Key metrics (ticker, date, risk level)
- Timestamp and branding

### Slack Alert
Block-formatted message with:
- Header with trade entry info
- Key fields organized in blocks
- Professional formatting

## 🔧 Advanced Usage

### Running as a System Service

1. Install the service:
```bash
sudo cp tradingagents-alerts.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tradingagents-alerts.service
```

2. Start the service:
```bash
sudo systemctl start tradingagents-alerts.service
```

3. Check status:
```bash
sudo systemctl status tradingagents-alerts.service
```

4. View logs:
```bash
sudo journalctl -u tradingagents-alerts.service -f
```

### Custom Configuration

You can customize the TradingAgents configuration by modifying the monitor initialization:

```python
from trade_alert_monitor import TradeAlertMonitor
from tradingagents.default_config import DEFAULT_CONFIG

# Custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o"
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 2

monitor = TradeAlertMonitor(config)
```

## 📁 File Structure

```
TradingAgents/
├── trade_alert_monitor.py      # Main alert monitor script
├── alert_setup.py              # Setup and configuration script
├── test_alerts.py              # Test script (created by setup)
├── alert_config.env            # Configuration file (created by setup)
├── alert_history.json          # Alert history (created automatically)
├── trade_alerts.log            # Log file (created automatically)
└── tradingagents-alerts.service # Systemd service file (created by setup)
```

## 🔍 How It Works

1. **Analysis**: Runs the full TradingAgents pipeline for each ticker
2. **Signal Processing**: Extracts clean BUY/SELL/HOLD decisions
3. **Entry Detection**: Identifies BUY signals as trade entries
4. **Deduplication**: Checks against alert history to prevent spam
5. **Context Extraction**: Gathers analysis summaries and confidence indicators
6. **Multi-Channel Alerts**: Sends formatted alerts via configured channels
7. **History Tracking**: Records sent alerts for future deduplication

## 🧪 Testing

### Test Configuration
```bash
python test_alerts.py
```

### Test Specific Functionality
```python
from trade_alert_monitor import TradeAlertMonitor

monitor = TradeAlertMonitor()

# Test single ticker
entries = monitor.check_for_trade_entries(['SPY'], '2024-12-06')
print(f"Found {len(entries)} trade entries")

# Test alerts (without sending)
if entries:
    print("Would send alerts for:")
    for entry in entries:
        print(f"  {entry['ticker']}: {entry['decision']}")
```

## 📈 Monitoring Best Practices

1. **Start Small**: Begin with 2-3 liquid tickers (SPY, QQQ, AAPL)
2. **Regular Testing**: Test the system weekly with known dates
3. **API Limits**: Monitor your API usage to avoid rate limits
4. **Log Monitoring**: Check `trade_alerts.log` regularly for issues
5. **Alert Fatigue**: Don't monitor too many tickers initially
6. **Market Hours**: Consider market hours for your alert schedule
7. **Backup Alerts**: Configure multiple alert channels for redundancy

## 🚨 Important Disclaimers

- **Not Financial Advice**: This system is for informational purposes only
- **No Guarantee**: Past performance doesn't guarantee future results
- **Risk Management**: Always implement proper risk management
- **Testing Required**: Test thoroughly before relying on alerts
- **Market Hours**: Consider market schedules for timing
- **API Costs**: Monitor your API usage and costs

## 🐛 Troubleshooting

### Common Issues

**"API Key not found"**
- Check that environment variables are set: `echo $OPENAI_API_KEY`
- Source your config file: `source alert_config.env`

**"No trade entries detected"**
- Normal behavior - BUY signals are relatively rare
- Test with different dates or tickers
- Check logs for analysis details

**"Email not sending"**
- Verify SMTP settings and credentials
- For Gmail, use app passwords, not account password
- Check firewall/network restrictions

**"Module not found"**
- Install missing dependencies: `pip install -r requirements.txt`
- Ensure you're in the correct virtual environment

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues related to:
- **TradingAgents Framework**: Check the main repository
- **Alert Monitor**: Review logs in `trade_alerts.log`
- **API Issues**: Verify your API keys and quotas

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional alert channels (Telegram, SMS, etc.)
- Better confidence scoring algorithms
- Advanced scheduling options
- Performance optimizations
- More sophisticated deduplication logic

---

## 📄 License

This alert monitor follows the same license as the TradingAgents framework.

**Remember**: This is a research tool. Always implement proper risk management and never risk more than you can afford to lose.