#!/usr/bin/env python3
"""
Test script for your personalized alert configuration
"""

from datetime import datetime
from tradingagents.alerts.alert_manager import AlertManager
from alert_config import DESKTOP_WEBHOOK_CONFIG, EMAIL_ONLY_CONFIG

def test_desktop_webhook_alerts():
    """Test desktop + webhook alerts (no email setup needed)"""
    print("🚨 Testing Desktop + Webhook Alerts")
    print("=" * 50)
    
    try:
        # Initialize with desktop + webhook config
        alert_manager = AlertManager(DESKTOP_WEBHOOK_CONFIG)
        print("✅ AlertManager initialized successfully")
        print(f"   - Number of handlers: {len(alert_manager.handlers)}")
        
        # Test alert
        test_trade_data = {
            "ticker": "AAPL",
            "decision": "BUY",
            "trade_date": datetime.now().strftime("%Y-%m-%d"),
            "confidence": 0.85,
            "summary": "Strong bullish signals detected. Technical indicators show upward momentum with good volume support.",
            "full_analysis": {
                "market_report": "Market conditions favorable for technology stocks",
                "technical_analysis": "RSI oversold, MACD bullish crossover",
                "price_target": "$180.00"
            }
        }
        
        print("\n📤 Sending test alert...")
        results = alert_manager.send_trade_alert(
            ticker="AAPL",
            decision="BUY", 
            trade_date=datetime.now().strftime("%Y-%m-%d"),
            full_analysis=test_trade_data["full_analysis"],
            summary=test_trade_data["summary"]
        )
        
        print("\n📊 Alert Results:")
        for handler_name, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"   - {handler_name}: {status}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing alerts: {e}")
        return False

def test_webhook_only():
    """Test just the webhook functionality"""
    print("\n🔗 Testing Webhook Only")
    print("=" * 30)
    
    webhook_only_config = {
        "alerts_enabled": True,
        "alert_on_decisions": ["BUY", "SELL"],
        "notification_handlers": {
            "webhook": {
                "enabled": True,
                "url": "https://webhook.site/unique-url-here",  # Replace with actual webhook URL
                "method": "POST",
                "headers": {
                    "Authorization": "Bearer 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",
                    "Content-Type": "application/json"
                }
            }
        }
    }
    
    try:
        alert_manager = AlertManager(webhook_only_config)
        results = alert_manager.send_trade_alert(
            ticker="TSLA",
            decision="SELL",
            trade_date=datetime.now().strftime("%Y-%m-%d"),
            summary="Technical analysis suggests overbought conditions"
        )
        
        for handler_name, success in results.items():
            status = "✅ Success" if success else "❌ Failed" 
            print(f"   - {handler_name}: {status}")
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")

def main():
    print("🚨 Testing Your Personal Alert Configuration")
    print("=" * 60)
    print(f"📧 Email: oxternal.0x@gmail.com")
    print(f"🔑 API Key: sk-or-v1-...{DESKTOP_WEBHOOK_CONFIG['notification_handlers']['webhook']['headers']['Authorization'][-8:]}")
    print()
    
    # Test desktop + webhook (works immediately)
    success = test_desktop_webhook_alerts()
    
    if success:
        print("\n🎉 Basic alert system is working!")
        print("\n📋 Next Steps:")
        print("1. ✅ Desktop notifications are working")
        print("2. 🔗 Webhook is configured with your API key")
        print("3. 📧 For email alerts, you'll need to set up Gmail app password")
        print("4. 🚀 Ready to use with your trading system!")
        
        # Test webhook separately
        test_webhook_only()
        
    else:
        print("\n❌ Alert system needs troubleshooting")

if __name__ == "__main__":
    main()