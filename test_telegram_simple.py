#!/usr/bin/env python3
"""
Simple Telegram Alert Test - Shows setup instructions
"""

def show_telegram_setup():
    print("📱 Telegram Alert Setup for Trading Agents")
    print("=" * 50)
    print()
    
    print("🤖 Quick Setup Steps:")
    print("1. Open Telegram app")
    print("2. Search for '@BotFather'")
    print("3. Send: /newbot")
    print("4. Name your bot (e.g., 'MyTradingBot')")
    print("5. Choose username ending in 'bot' (e.g., 'mytradingalerts_bot')")
    print("6. Save the bot token")
    print("7. Send a message to your bot")
    print("8. Run the full setup: python3 telegram_setup_guide.py")
    
    print("\n📱 What You'll Get:")
    print("✅ Instant mobile notifications")
    print("✅ Rich formatted messages with emojis")
    print("✅ BUY/SELL signals with analysis")
    print("✅ Price targets and stop losses")
    print("✅ Confidence levels and timestamps")
    
    print("\n📋 Sample Telegram Alert:")
    print("=" * 30)
    print("🟢📈 *BUY Signal*")
    print("")
    print("📊 *Ticker:* `AAPL`")
    print("📅 *Date:* 2025-06-27")
    print("💭 *Summary:* Strong bullish signals detected")
    print("")
    print("📈 *Analysis Details:*")
    print("🎯 Target: `$185.00`")
    print("🛑 Stop Loss: `$165.00`")
    print("📊 Confidence: `85%`")
    print("🔧 Technical: RSI oversold, MACD bullish crossover")
    print("")
    print("⏰ *Alert Time:* 14:30:22 UTC")
    print("🤖 *Trading Agents Alert System*")
    print("=" * 30)
    
    print("\n🔗 Next Steps:")
    print("• Run: python3 telegram_setup_guide.py")
    print("• Follow the interactive setup")
    print("• Test your bot with sample alerts")
    print("• Integrate with your trading system")

def test_telegram_format():
    """Test the message formatting without sending"""
    print("\n🧪 Testing Message Format:")
    
    # Simulate the telegram message creation
    trade_data = {
        "ticker": "AAPL",
        "decision": "BUY",
        "trade_date": "2025-06-27",
        "confidence": 0.85,
        "summary": "Strong bullish signals detected. RSI oversold with MACD bullish crossover.",
        "full_analysis": {
            "price_target": "$185.00",
            "stop_loss": "$165.00",
            "technical_analysis": "RSI: 28 (oversold), MACD: bullish crossover, Volume: above average"
        }
    }
    
    # Create message (same logic as TelegramNotificationHandler)
    ticker = trade_data["ticker"]
    decision = trade_data["decision"]
    
    if decision == "BUY":
        emoji = "🟢📈"
        action = "BUY Signal"
    elif decision == "SELL":
        emoji = "🔴📉"
        action = "SELL Signal"
    else:
        emoji = "⚪"
        action = f"{decision} Signal"
    
    message = f"{emoji} *{action}*\n\n"
    message += f"📊 *Ticker:* `{ticker}`\n"
    message += f"📅 *Date:* {trade_data['trade_date']}\n"
    message += f"💭 *Summary:* {trade_data['summary']}\n"
    
    full_analysis = trade_data["full_analysis"]
    message += "\n📈 *Analysis Details:*\n"
    message += f"🎯 Target: `{full_analysis['price_target']}`\n"
    message += f"🛑 Stop Loss: `{full_analysis['stop_loss']}`\n"
    
    confidence = trade_data["confidence"]
    confidence_pct = int(confidence * 100)
    message += f"📊 Confidence: `{confidence_pct}%`\n"
    message += f"🔧 Technical: {full_analysis['technical_analysis'][:60]}...\n"
    
    message += f"\n⏰ *Alert Time:* 14:30:22 UTC"
    message += f"\n🤖 *Trading Agents Alert System*"
    
    print("\n📱 Generated Telegram Message:")
    print("-" * 40)
    print(message)
    print("-" * 40)

def main():
    show_telegram_setup()
    test_telegram_format()
    
    print("\n🚀 Ready to set up Telegram alerts?")
    print("Run: python3 telegram_setup_guide.py")

if __name__ == "__main__":
    main()