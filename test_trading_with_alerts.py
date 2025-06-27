#!/usr/bin/env python3
"""
Complete test of trading system with personalized alerts
"""

import os
from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from alert_config import DESKTOP_WEBHOOK_CONFIG

def setup_environment():
    """Set up environment variables for API access"""
    # Set up Google API key for LLM (you may need to set this)
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ GOOGLE_API_KEY not set. You may need to configure this for LLM access.")
    
    return True

def test_trading_with_alerts():
    """Test the complete trading system with alerts"""
    print("🚨 Testing Trading System with Personal Alerts")
    print("=" * 60)
    print(f"📧 Alert Email: oxternal.0x@gmail.com")
    print(f"🔑 API Key: sk-or-v1-...{DESKTOP_WEBHOOK_CONFIG['notification_handlers']['webhook']['headers']['Authorization'][-8:]}")
    print()
    
    # Create working configuration for alerts (webhook disabled due to missing URL)
    working_alert_config = {
        "alerts_enabled": True,
        "alert_on_decisions": ["BUY", "SELL"],
        "notification_handlers": {
            # Use a simple console notification for testing
            "console": {
                "enabled": True,
            }
        }
    }
    
    # Set up trading configuration
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["alert_config"] = working_alert_config
    
    print("📊 Initializing trading system with alerts...")
    
    try:
        # Initialize trading system
        trading_graph = TradingAgentsGraph(config)
        print("✅ Trading system initialized successfully!")
        
        # Test with a sample stock analysis
        print("\n📈 Running sample analysis for AAPL...")
        
        # Simulate a trade analysis (without requiring real LLM calls)
        sample_trade_data = {
            "ticker": "AAPL",
            "decision": "BUY",
            "trade_date": datetime.now().strftime("%Y-%m-%d"),
            "confidence": 0.85,
            "summary": "Strong technical indicators show bullish momentum for AAPL",
            "full_analysis": {
                "market_report": "Technology sector showing strength",
                "technical_analysis": "RSI indicates oversold conditions, MACD bullish crossover",
                "fundamental_analysis": "Strong quarterly earnings, positive guidance",
                "price_target": "$185.00",
                "stop_loss": "$165.00"
            }
        }
        
        # Test the alert system directly
        if trading_graph.alert_manager:
            print("📤 Testing alert system...")
            results = trading_graph.alert_manager.send_trade_alert(
                ticker=sample_trade_data["ticker"],
                decision=sample_trade_data["decision"],
                trade_date=sample_trade_data["trade_date"],
                full_analysis=sample_trade_data["full_analysis"],
                summary=sample_trade_data["summary"]
            )
            
            print("\n📊 Alert Results:")
            for handler_name, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"   - {handler_name}: {status}")
        else:
            print("⚠️ Alert manager not initialized")
        
        print("\n🎉 Trading system with alerts is ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing trading system: {e}")
        print(f"   This may be due to missing API keys or dependencies")
        return False

def show_usage_instructions():
    """Show how to use the system with real trading"""
    print("\n📋 How to Use Your Alert System:")
    print("=" * 40)
    print("1. 🔑 Set up your Google API key:")
    print("   export GOOGLE_API_KEY='your-google-api-key'")
    print()
    print("2. 📧 For email alerts, set up Gmail app password:")
    print("   - Go to Google Account settings")
    print("   - Enable 2-factor authentication") 
    print("   - Generate app password for 'Mail'")
    print("   - Update alert_config.py with the app password")
    print()
    print("3. 🔗 For webhook alerts, set up your webhook URL:")
    print("   - Visit https://webhook.site to get a test URL")
    print("   - Update the webhook URL in alert_config.py")
    print()
    print("4. 🚀 Run real trading analysis:")
    print("   python3 main.py --ticker AAPL --alert-config alert_config.py")
    print()
    print("5. 📊 Monitor continuous alerts:")
    print("   python3 examples/continuous_monitoring.py")

def main():
    # Set up environment
    setup_environment()
    
    # Test the system
    success = test_trading_with_alerts()
    
    if success:
        show_usage_instructions()
    else:
        print("\n🔧 Troubleshooting:")
        print("- Ensure all dependencies are installed")
        print("- Set up API keys for LLM access")
        print("- Check alert configuration")

if __name__ == "__main__":
    main()