#!/usr/bin/env python3
"""
Test script for TradingAgents Alert Monitor
"""

import os
import sys
from datetime import datetime
from trade_alert_monitor import TradeAlertMonitor

def test_single_ticker():
    """Test monitoring a single ticker."""
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
    """Test alert configuration."""
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
