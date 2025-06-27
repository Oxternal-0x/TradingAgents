#!/usr/bin/env python3
"""
Example script showing how to use the Trading Agents Alert System

This script demonstrates:
1. How to configure alerts
2. How to test the alert system
3. How to run analysis with alerts enabled
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path to import tradingagents
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.alerts.config_template import (
    DESKTOP_ONLY_CONFIG,
    create_email_config,
    create_slack_config,
    create_multi_channel_config
)


def example_desktop_alerts():
    """Example using only desktop notifications."""
    print("🖥️ Setting up desktop-only alerts...")
    
    # Create config with desktop alerts
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["alert_config"] = DESKTOP_ONLY_CONFIG
    
    # Initialize trading system with alerts
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Test alerts
    print("\n🧪 Testing desktop alerts...")
    ta.test_alerts()
    
    # Run analysis (this will trigger an alert if BUY/SELL decision is made)
    print("\n📊 Running analysis for NVDA...")
    final_state, decision = ta.propagate("NVDA", "2024-05-10")
    print(f"Decision: {decision}")
    
    return ta


def example_email_alerts():
    """Example using email notifications."""
    print("📧 Setting up email alerts...")
    
    # Create email configuration
    # NOTE: You need to replace these with your actual email credentials
    email_config = create_email_config(
        sender_email="your-email@gmail.com",
        sender_password="your-app-password",  # Use Gmail app password
        recipient_emails=["your-email@gmail.com"]
    )
    
    # Create config with email alerts
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["alert_config"] = email_config
    
    # Initialize trading system with alerts
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Test alerts
    print("\n🧪 Testing email alerts...")
    ta.test_alerts()
    
    return ta


def example_slack_alerts():
    """Example using Slack notifications."""
    print("💬 Setting up Slack alerts...")
    
    # Create Slack configuration
    # NOTE: You need to replace this with your actual Slack webhook URL
    slack_config = create_slack_config(
        webhook_url="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
        channel="#trading-alerts"
    )
    
    # Create config with Slack alerts
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["alert_config"] = slack_config
    
    # Initialize trading system with alerts
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Test alerts
    print("\n🧪 Testing Slack alerts...")
    ta.test_alerts()
    
    return ta


def example_multi_channel_alerts():
    """Example using multiple notification channels."""
    print("🔔 Setting up multi-channel alerts...")
    
    # Configure multiple channels
    email_config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "recipient_emails": ["your-email@gmail.com"]
    }
    
    slack_config = {
        "slack_webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
        "slack_channel": "#trading-alerts",
        "slack_username": "Trading Bot"
    }
    
    # Create multi-channel configuration
    multi_config = create_multi_channel_config(
        email_config=email_config,
        slack_config=slack_config
    )
    
    # Create config with multi-channel alerts
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["alert_config"] = multi_config
    
    # Initialize trading system with alerts
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Test alerts
    print("\n🧪 Testing multi-channel alerts...")
    ta.test_alerts()
    
    return ta


def check_alert_status(ta):
    """Check the status of the alert system."""
    print("\n📋 Alert System Status:")
    status = ta.get_alert_status()
    
    if not status["available"]:
        print(f"❌ Alert system not available: {status['reason']}")
        return
    
    print(f"✅ Alert system available and {'enabled' if status['enabled'] else 'disabled'}")
    
    if "handlers" in status:
        print("\n📱 Configured handlers:")
        for handler_name, handler_info in status["handlers"].items():
            configured = "✅" if handler_info["configured"] else "❌"
            print(f"  {configured} {handler_name}")


def main():
    """Main function demonstrating different alert configurations."""
    print("🚨 Trading Agents Alert System Examples")
    print("=" * 50)
    
    # Example 1: Desktop alerts (works on most systems)
    print("\n1️⃣ Example 1: Desktop Notifications")
    print("-" * 30)
    try:
        ta = example_desktop_alerts()
        check_alert_status(ta)
    except Exception as e:
        print(f"❌ Error with desktop alerts: {e}")
    
    print("\n" + "=" * 50)
    
    # Example 2: Email alerts (requires email configuration)
    print("\n2️⃣ Example 2: Email Notifications")
    print("-" * 30)
    print("⚠️  Note: This example requires you to configure your email credentials")
    print("    Edit the email_config in example_email_alerts() function")
    # Uncomment the next lines to test email alerts:
    # try:
    #     ta = example_email_alerts()
    #     check_alert_status(ta)
    # except Exception as e:
    #     print(f"❌ Error with email alerts: {e}")
    
    print("\n" + "=" * 50)
    
    # Example 3: Slack alerts (requires Slack webhook)
    print("\n3️⃣ Example 3: Slack Notifications")
    print("-" * 30)
    print("⚠️  Note: This example requires you to configure your Slack webhook URL")
    print("    Edit the slack_config in example_slack_alerts() function")
    # Uncomment the next lines to test Slack alerts:
    # try:
    #     ta = example_slack_alerts()
    #     check_alert_status(ta)
    # except Exception as e:
    #     print(f"❌ Error with Slack alerts: {e}")
    
    print("\n" + "=" * 50)
    print("\n🎉 Alert system examples completed!")
    print("\nTo enable alerts in your trading system:")
    print("1. Choose your preferred notification method(s)")
    print("2. Configure the credentials in the config")
    print("3. Add 'alert_config' to your TradingAgentsGraph config")
    print("4. Run your trading analysis - alerts will be sent automatically!")


if __name__ == "__main__":
    main()