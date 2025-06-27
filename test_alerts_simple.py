#!/usr/bin/env python3
"""
Simple test script for the Trading Agents Alert System

This script tests the alert system components without requiring LLM credentials.
"""

from datetime import datetime
from tradingagents.alerts.alert_manager import AlertManager
from tradingagents.alerts.config_template import DESKTOP_ONLY_CONFIG

def test_alert_system():
    print("🚨 Testing Alert System Components")
    print("=" * 50)
    
    # Test alert manager initialization
    print("📊 Initializing AlertManager...")
    try:
        alert_manager = AlertManager(DESKTOP_ONLY_CONFIG)
        print("✅ AlertManager initialized successfully")
        print(f"   - Number of handlers: {len(alert_manager.handlers)}")
        print(f"   - Enabled handlers: {[h.__class__.__name__ for h in alert_manager.handlers if h.is_configured()]}")
    except Exception as e:
        print(f"❌ Error initializing AlertManager: {e}")
        return
    
    # Test creating a sample trade alert
    print("\n📈 Testing trade alert...")
    sample_trade_data = {
        "ticker": "AAPL",
        "decision": "BUY",
        "date": "2024-01-15",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "summary": "Strong technical indicators and positive sentiment analysis suggest a BUY signal.",
        "full_analysis": {
            "market_report": "Market showing bullish trend",
            "news_analysis": "Positive earnings report",
            "sentiment": "Bullish"
        }
    }
    
    # Test sending alert
    try:
        results = alert_manager.send_trade_alert(
            ticker=sample_trade_data["ticker"],
            decision=sample_trade_data["decision"],
            trade_date=sample_trade_data["date"],
            full_analysis=sample_trade_data["full_analysis"],
            summary=sample_trade_data["summary"]
        )
        
        print("✅ Trade alert sent successfully!")
        print(f"   - Alert results: {results}")
        
        if any(results.values()):
            print("🎉 At least one notification method worked!")
        else:
            print("⚠️  No notification methods were able to send alerts")
            print("   This is normal if you haven't configured email/SMS/Slack")
            
    except Exception as e:
        print(f"❌ Error sending trade alert: {e}")
    
    # Test handler configuration status
    print("\n🔧 Handler Configuration Status:")
    for handler in alert_manager.handlers:
        handler_name = handler.__class__.__name__
        configured = handler.is_configured()
        status = "✅ Configured" if configured else "❌ Not configured"
        print(f"   - {handler_name}: {status}")
    
    print("\n✨ Alert system test completed!")
    print("\nNext steps:")
    print("1. Configure email/SMS/Slack handlers in your config")
    print("2. Set up LLM API keys for full trading system")
    print("3. Run the full trading analysis with alerts enabled")

if __name__ == "__main__":
    test_alert_system()