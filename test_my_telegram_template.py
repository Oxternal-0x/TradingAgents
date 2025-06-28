#!/usr/bin/env python3
"""
Test Telegram Bot Script Template

INSTRUCTIONS:
1. Replace bot_token with your actual bot token from BotFather
2. Replace chat_id with your actual chat ID
3. Save this file as 'test_my_telegram.py'
4. Run: python3 test_my_telegram.py
"""

import requests
from datetime import datetime

# Your credentials (replace with actual values)
bot_token = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Replace with your bot token
chat_id = "123456789"  # Replace with your chat ID

def test_telegram():
    print("🧪 Testing Telegram Bot...")
    print(f"🔑 Bot Token: {bot_token[:20]}...")
    print(f"💬 Chat ID: {chat_id}")
    print()
    
    # Test message
    message = """🚨 *Test Alert*

📊 Your trading bot is working!
⏰ Time: """ + datetime.now().strftime("%H:%M:%S") + """
🤖 *Trading Agents Alert System*"""
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        print("📤 Sending test message...")
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Test message sent successfully!")
            print("📱 Check your Telegram for the test alert")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        return False

def test_trading_alert():
    """Send a sample trading alert"""
    print("\n🚀 Testing Trading Alert Format...")
    
    # Sample trading alert
    alert_message = """🟢📈 *BUY Signal*

📊 *Ticker:* `AAPL`
📅 *Date:* """ + datetime.now().strftime("%Y-%m-%d") + """
💭 *Summary:* Strong bullish signals detected

📈 *Analysis Details:*
🎯 Target: `$185.00`
🛑 Stop Loss: `$165.00`
📊 Confidence: `85%`
🔧 Technical: RSI oversold, MACD bullish crossover

⏰ *Alert Time:* """ + datetime.now().strftime("%H:%M:%S UTC") + """
🤖 *Trading Agents Alert System*"""
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": alert_message,
        "parse_mode": "Markdown"
    }
    
    try:
        print("📤 Sending sample trading alert...")
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Sample trading alert sent!")
            print("📱 Check your Telegram for the formatted alert")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to send trading alert: {e}")
        return False

def main():
    print("📱 Telegram Bot Testing")
    print("=" * 30)
    
    # Check credentials
    if bot_token == "123456789:ABCdefGHIjklMNOpqrsTUVwxyz":
        print("❌ Please update bot_token with your actual bot token")
        print("   Get it from @BotFather on Telegram")
        return
    
    if chat_id == "123456789":
        print("❌ Please update chat_id with your actual chat ID")
        print("   Visit: https://api.telegram.org/bot{}/getUpdates".format(bot_token))
        return
    
    # Run tests
    if test_telegram():
        print("\n" + "="*50)
        test_trading_alert()
        
        print("\n🎉 Testing Complete!")
        print("If you received both messages, your Telegram bot is ready!")
        print("You can now use it with your trading system.")
    else:
        print("\n❌ Basic test failed. Please check your credentials.")
        print("\n🔧 Troubleshooting:")
        print("1. Verify bot token is correct")
        print("2. Make sure you sent a message to your bot first")
        print("3. Check that chat_id is correct")

if __name__ == "__main__":
    main()