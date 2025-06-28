#!/usr/bin/env python3
"""
Telegram Alert Setup Guide for Trading Agents

This script helps you set up Telegram alerts step by step.
"""

import requests
import json
from datetime import datetime
from tradingagents.alerts.telegram_handler import TelegramNotificationHandler


def show_telegram_setup_instructions():
    """Show detailed Telegram setup instructions"""
    print("📱 Telegram Alert Setup for Trading Agents")
    print("=" * 50)
    print()
    
    print("📋 Complete Setup Steps:")
    print("=" * 30)
    
    print("\n🤖 Step 1: Create a Telegram Bot")
    print("   1. Open Telegram and search for '@BotFather'")
    print("   2. Start a chat with BotFather")
    print("   3. Send: /newbot")
    print("   4. Follow prompts to name your bot (e.g., 'MyTradingBot')")
    print("   5. Choose a username ending in 'bot' (e.g., 'mytradingalerts_bot')")
    print("   6. 🔑 SAVE the bot token (looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)")
    
    print("\n💬 Step 2: Get Your Chat ID")
    print("   1. Start a chat with your new bot")
    print("   2. Send any message to your bot (e.g., 'Hello')")
    print("   3. Use the tool below to find your chat ID")
    
    print("\n🧪 Step 3: Test Your Setup")
    print("   After getting bot token and chat ID, test with:")
    print("   python3 test_telegram_alerts.py")


def get_chat_id_helper(bot_token: str):
    """Helper to get chat ID from bot token"""
    if not bot_token:
        print("❌ Please provide a bot token")
        return None
    
    try:
        print(f"🔍 Looking for chat ID for bot token: {bot_token[:20]}...")
        
        # Get updates from Telegram API
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok") and data.get("result"):
                updates = data["result"]
                if updates:
                    print(f"✅ Found {len(updates)} messages")
                    
                    # Show available chat IDs
                    chat_ids = set()
                    for update in updates:
                        if "message" in update:
                            chat_id = update["message"]["chat"]["id"]
                            chat_type = update["message"]["chat"]["type"]
                            first_name = update["message"]["chat"].get("first_name", "Unknown")
                            chat_ids.add((chat_id, chat_type, first_name))
                    
                    if chat_ids:
                        print("\n📞 Available Chat IDs:")
                        for chat_id, chat_type, name in chat_ids:
                            print(f"   • Chat ID: {chat_id} (Type: {chat_type}, Name: {name})")
                        
                        # Return the most recent personal chat
                        personal_chats = [(cid, ctype, name) for cid, ctype, name in chat_ids if ctype == "private"]
                        if personal_chats:
                            return str(personal_chats[0][0])
                    else:
                        print("❌ No chat IDs found")
                        return None
                else:
                    print("❌ No messages found. Please send a message to your bot first.")
                    return None
            else:
                print(f"❌ Telegram API error: {data}")
                return None
        else:
            print(f"❌ HTTP error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting chat ID: {e}")
        return None


def test_telegram_bot(bot_token: str, chat_id: str):
    """Test Telegram bot with given credentials"""
    print(f"\n🧪 Testing Telegram Bot")
    print("=" * 30)
    
    config = {
        "bot_token": bot_token,
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "disable_notification": False
    }
    
    try:
        handler = TelegramNotificationHandler(config)
        
        # Test connection
        print("🔐 Testing bot connection...")
        if handler.test_connection():
            print("✅ Bot connection successful!")
            
            # Send test message
            print("📤 Sending test trading alert...")
            if handler.send_test_message():
                print("✅ Test message sent successfully!")
                print("📱 Check your Telegram for the test alert")
                return True
            else:
                print("❌ Failed to send test message")
                return False
        else:
            print("❌ Bot connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing bot: {e}")
        return False


def create_telegram_config_file(bot_token: str, chat_id: str):
    """Create a Telegram configuration file"""
    config_content = f'''#!/usr/bin/env python3
"""
Working Telegram Alert Configuration
Generated by Telegram setup script
"""

# Your Telegram bot credentials
TELEGRAM_BOT_TOKEN = "{bot_token}"
TELEGRAM_CHAT_ID = "{chat_id}"

# Telegram-only alert configuration
TELEGRAM_ALERT_CONFIG = {{
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {{
        "telegram": {{
            "enabled": True,
            "bot_token": TELEGRAM_BOT_TOKEN,
            "chat_id": TELEGRAM_CHAT_ID,
            "parse_mode": "Markdown",
            "disable_notification": False,
        }}
    }}
}}

# Multi-channel config (Telegram + Email + Webhook)
MULTI_CHANNEL_WITH_TELEGRAM = {{
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {{
        "telegram": {{
            "enabled": True,
            "bot_token": TELEGRAM_BOT_TOKEN,
            "chat_id": TELEGRAM_CHAT_ID,
            "parse_mode": "Markdown",
            "disable_notification": False,
        }},
        "email": {{
            "enabled": False,  # Set to True and configure
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": "your-app-password-here",
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        }},
        "webhook": {{
            "enabled": False,  # Set to True and configure
            "url": "https://webhook.site/your-unique-url",
            "method": "POST",
            "headers": {{
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            }}
        }}
    }}
}}
'''
    
    try:
        with open('telegram_config.py', 'w') as f:
            f.write(config_content)
        print("✅ Created telegram_config.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False


def create_telegram_test_script(bot_token: str, chat_id: str):
    """Create a test script for Telegram alerts"""
    test_script_content = f'''#!/usr/bin/env python3
"""
Test Telegram Trading Alerts
"""

from datetime import datetime
from tradingagents.alerts.telegram_handler import TelegramNotificationHandler

def test_telegram_alerts():
    print("📱 Testing Telegram Trading Alerts")
    print("=" * 40)
    
    # Your bot configuration
    config = {{
        "bot_token": "{bot_token}",
        "chat_id": "{chat_id}",
        "parse_mode": "Markdown",
        "disable_notification": False
    }}
    
    try:
        handler = TelegramNotificationHandler(config)
        
        # Test different types of alerts
        test_alerts = [
            {{
                "ticker": "AAPL",
                "decision": "BUY",
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "confidence": 0.85,
                "summary": "Strong bullish signals detected. RSI oversold with MACD bullish crossover.",
                "full_analysis": {{
                    "price_target": "$185.00",
                    "stop_loss": "$165.00",
                    "technical_analysis": "RSI: 28 (oversold), MACD: bullish crossover, Volume: above average"
                }}
            }},
            {{
                "ticker": "TSLA",
                "decision": "SELL", 
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "confidence": 0.72,
                "summary": "Overbought conditions detected. Taking profits at resistance level.",
                "full_analysis": {{
                    "price_target": "$220.00",
                    "stop_loss": "$260.00",
                    "technical_analysis": "RSI: 78 (overbought), Resistance at $250, Declining volume"
                }}
            }}
        ]
        
        for i, alert in enumerate(test_alerts, 1):
            print(f"\\n📤 Sending test alert {{i}}/{{len(test_alerts)}}...")
            success = handler.send_notification(alert)
            if success:
                print(f"✅ Alert {{i}} sent successfully!")
            else:
                print(f"❌ Alert {{i}} failed")
            
            # Small delay between messages
            import time
            time.sleep(1)
        
        print("\\n🎉 Telegram alert testing complete!")
        print("📱 Check your Telegram for the test messages")
        
    except Exception as e:
        print(f"❌ Error testing Telegram alerts: {{e}}")

if __name__ == "__main__":
    test_telegram_alerts()
'''
    
    try:
        with open('test_telegram_alerts.py', 'w') as f:
            f.write(test_script_content)
        print("✅ Created test_telegram_alerts.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create test script: {e}")
        return False


def main():
    show_telegram_setup_instructions()
    
    print("\n🛠️ Interactive Setup:")
    print("=" * 25)
    
    # Get bot token
    bot_token = input("\nEnter your bot token (from BotFather): ").strip()
    
    if not bot_token:
        print("❌ Bot token is required")
        return
    
    if len(bot_token) < 40:
        print("⚠️ Bot token seems too short. Make sure you copied the full token.")
    
    # Try to get chat ID automatically
    print("\n🔍 Attempting to find your chat ID...")
    chat_id = get_chat_id_helper(bot_token)
    
    if not chat_id:
        print("\n💡 Manual chat ID input:")
        print("   If you can't find your chat ID automatically:")
        print("   1. Send a message to your bot")
        print("   2. Visit: https://api.telegram.org/bot{}/getUpdates".format(bot_token[:20] + "..."))
        print("   3. Look for 'chat':{'id': YOUR_CHAT_ID}")
        chat_id = input("\nEnter your chat ID manually (or press Enter to skip): ").strip()
    
    if not chat_id:
        print("❌ Chat ID is required for testing")
        return
    
    print(f"\n📋 Configuration Summary:")
    print(f"   🤖 Bot Token: {bot_token[:20]}...")
    print(f"   💬 Chat ID: {chat_id}")
    
    # Test the configuration
    if test_telegram_bot(bot_token, chat_id):
        print("\n📁 Creating configuration files...")
        create_telegram_config_file(bot_token, chat_id)
        create_telegram_test_script(bot_token, chat_id)
        
        print("\n🎉 Telegram setup complete!")
        print("\n📋 Next steps:")
        print("1. ✅ Check your Telegram for the test message")
        print("2. ✅ Use telegram_config.py in your trading system")
        print("3. ✅ Run: python3 test_telegram_alerts.py")
        print("4. 🚀 Start receiving live trading alerts!")
    else:
        print("\n❌ Setup failed. Please check your credentials and try again.")


if __name__ == "__main__":
    main()