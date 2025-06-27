#!/usr/bin/env python3
"""
Simple test script for the Trading Agents Alert System

This script demonstrates basic alert functionality with desktop notifications.
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.alerts.config_template import DESKTOP_ONLY_CONFIG


def main():
    print("🚨 Testing Trading Agents Alert System")
    print("=" * 50)

    # Create config with desktop alerts
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["alert_config"] = DESKTOP_ONLY_CONFIG

    print("📊 Initializing trading system with alerts...")
    
    try:
        # Initialize trading system with alerts
        ta = TradingAgentsGraph(debug=True, config=config)
        
        # Check alert status
        print("\n📋 Checking alert system status...")
        status = ta.get_alert_status()
        print(f"Alert system available: {status.get('available', False)}")
        if status.get('available'):
            print(f"Alert system enabled: {status.get('enabled', False)}")
            if 'handlers' in status:
                for handler, info in status['handlers'].items():
                    print(f"  {handler}: {'✅' if info['configured'] else '❌'}")

        # Test alerts
        print("\n🧪 Testing alert system...")
        test_result = ta.test_alerts()
        
        if test_result:
            print("✅ Alert test completed successfully!")
        else:
            print("❌ Alert test failed or no handlers configured")

        # Run actual analysis (this will trigger alerts on BUY/SELL)
        print("\n📊 Running trading analysis for NVDA...")
        print("This will generate alerts if a BUY or SELL decision is made...")
        
        final_state, decision = ta.propagate("NVDA", "2024-05-10")
        
        print(f"\n🎯 Analysis completed!")
        print(f"Decision: {decision}")
        
        if decision in ["BUY", "SELL"]:
            print("🚨 This should have triggered an alert!")
        else:
            print("ℹ️  No alert sent (only BUY/SELL decisions trigger alerts)")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nThis might be due to:")
        print("- Missing LLM API keys")
        print("- Missing dependencies (try: pip install plyer)")
        print("- Configuration issues")


if __name__ == "__main__":
    main()