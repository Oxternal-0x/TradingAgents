#!/usr/bin/env python3
"""
Setup script for TradingAgents Trade Alert Monitor
Helps configure and test the alerting system
"""

import os
import sys
import json
from pathlib import Path

def create_env_file():
    """Create environment configuration file."""
    config_content = """# TradingAgents Alert Monitor Configuration
# Copy this file to .env and customize with your values

# Required API Keys
export FINNHUB_API_KEY="your_finnhub_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"

# Email Configuration (Gmail example)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-gmail-app-password"  # Use app password for Gmail
export RECIPIENT_EMAILS="alert1@email.com,alert2@email.com"

# Discord Webhook (optional)
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# Slack Webhook (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WEBHOOK_URL"

# Trading Configuration
export MONITOR_TICKERS="SPY,QQQ,AAPL,MSFT,GOOGL"
export ALERT_SCHEDULE="daily"  # daily, hourly, manual
"""
    
    with open("alert_config.env", "w") as f:
        f.write(config_content)
    
    print("✅ Configuration file created: alert_config.env")
    print("📝 Please edit this file with your actual API keys and preferences")
    print()

def test_configuration():
    """Test if all required environment variables are set."""
    print("🔍 Testing configuration...")
    print()
    
    required_vars = [
        "FINNHUB_API_KEY",
        "OPENAI_API_KEY"
    ]
    
    optional_vars = [
        "SENDER_EMAIL",
        "RECIPIENT_EMAILS",
        "DISCORD_WEBHOOK_URL",
        "SLACK_WEBHOOK_URL"
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
        else:
            print(f"✅ {var}: Configured")
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
        else:
            print(f"✅ {var}: Configured")
    
    if missing_required:
        print(f"\n❌ Missing required environment variables:")
        for var in missing_required:
            print(f"   - {var}")
        print("\n🔧 Please set these before running the alert monitor.")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional environment variables (alerts won't be sent):")
        for var in missing_optional:
            print(f"   - {var}")
    
    print("\n✅ Configuration test completed!")
    return True

def create_systemd_service():
    """Create a systemd service file for running alerts as a service."""
    current_dir = Path.cwd()
    python_path = sys.executable
    
    service_content = f"""[Unit]
Description=TradingAgents Trade Alert Monitor
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={current_dir}
Environment=PATH={os.environ.get('PATH')}
EnvironmentFile={current_dir}/alert_config.env
ExecStart={python_path} {current_dir}/trade_alert_monitor.py --schedule daily --tickers SPY QQQ AAPL
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "tradingagents-alerts.service"
    with open(service_file, "w") as f:
        f.write(service_content)
    
    print(f"✅ Systemd service file created: {service_file}")
    print("🔧 To install as a system service:")
    print(f"   sudo cp {service_file} /etc/systemd/system/")
    print("   sudo systemctl daemon-reload")
    print("   sudo systemctl enable tradingagents-alerts.service")
    print("   sudo systemctl start tradingagents-alerts.service")
    print()

def create_test_script():
    """Create a test script to verify the system works."""
    test_content = """#!/usr/bin/env python3
\"\"\"
Test script for TradingAgents Alert Monitor
\"\"\"

import os
import sys
from datetime import datetime
from trade_alert_monitor import TradeAlertMonitor

def test_single_ticker():
    \"\"\"Test monitoring a single ticker.\"\"\"
    print("🧪 Testing single ticker analysis...")
    
    # Test with a safe ticker and recent date
    monitor = TradeAlertMonitor()
    
    # Use a recent trading day
    test_date = "2024-12-06"  # Friday
    test_ticker = "SPY"
    
    try:
        print(f"Analyzing {test_ticker} for {test_date}...")
        trade_entries = monitor.check_for_trade_entries([test_ticker], test_date)
        
        if trade_entries:
            print(f"✅ Found {len(trade_entries)} trade entries:")
            for entry in trade_entries:
                print(f"   📈 {entry['ticker']}: {entry['decision']}")
                print(f"      Risk: {entry['confidence_indicators']['risk_assessment']}")
        else:
            print("ℹ️  No BUY signals detected (this is normal)")
        
        print("✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_alert_config():
    \"\"\"Test alert configuration.\"\"\"
    print("🧪 Testing alert configuration...")
    
    monitor = TradeAlertMonitor()
    
    # Test email config
    if monitor.email_config['sender_email']:
        print("✅ Email configuration found")
    else:
        print("⚠️  Email configuration missing")
    
    # Test webhook configs
    if monitor.discord_webhook:
        print("✅ Discord webhook configured")
    else:
        print("ℹ️  Discord webhook not configured")
    
    if monitor.slack_webhook:
        print("✅ Slack webhook configured")
    else:
        print("ℹ️  Slack webhook not configured")
    
    return True

if __name__ == "__main__":
    print("🚀 TradingAgents Alert Monitor Test")
    print("=" * 40)
    
    # Test configuration
    if not test_alert_config():
        sys.exit(1)
    
    print()
    
    # Test analysis
    if not test_single_ticker():
        sys.exit(1)
    
    print()
    print("🎉 All tests passed! The alert monitor is ready to use.")
"""
    
    with open("test_alerts.py", "w") as f:
        f.write(test_content)
    
    os.chmod("test_alerts.py", 0o755)
    print("✅ Test script created: test_alerts.py")
    print("🧪 Run it with: python test_alerts.py")
    print()

def main():
    print("🚀 TradingAgents Alert Monitor Setup")
    print("=" * 40)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("tradingagents"):
        print("❌ Please run this script from the TradingAgents root directory")
        sys.exit(1)
    
    print("1. Creating configuration file...")
    create_env_file()
    
    print("2. Creating test script...")
    create_test_script()
    
    print("3. Creating systemd service file...")
    create_systemd_service()
    
    print("🎯 Next Steps:")
    print("   1. Edit alert_config.env with your API keys and alert preferences")
    print("   2. Source the config: source alert_config.env")
    print("   3. Test the system: python test_alerts.py")
    print("   4. Run manual check: python trade_alert_monitor.py --tickers SPY AAPL")
    print("   5. For automated alerts: python trade_alert_monitor.py --schedule daily")
    print()
    print("📖 For help: python trade_alert_monitor.py --help")

if __name__ == "__main__":
    main()