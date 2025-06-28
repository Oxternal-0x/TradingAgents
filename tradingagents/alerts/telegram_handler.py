import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from .notification_handlers import NotificationHandler


class TelegramNotificationHandler(NotificationHandler):
    """Handles Telegram notifications for trading alerts."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Telegram handler with bot token and chat ID."""
        self.bot_token = config.get("bot_token", "")
        self.chat_id = config.get("chat_id", "")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.parse_mode = config.get("parse_mode", "Markdown")
        self.disable_notification = config.get("disable_notification", False)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def is_configured(self) -> bool:
        """Check if Telegram is properly configured."""
        return bool(self.bot_token and self.chat_id)
    
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send Telegram notification for trade alert."""
        if not self.is_configured():
            self.logger.error("Telegram not configured - missing bot token or chat ID")
            return False
        
        try:
            # Create message
            message = self._create_telegram_message(trade_data)
            
            # Send message
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": self.parse_mode,
                "disable_notification": self.disable_notification
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.logger.info(f"Telegram alert sent successfully for {trade_data['ticker']}")
                return True
            else:
                self.logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send Telegram alert: {e}")
            return False
    
    def _create_telegram_message(self, trade_data: Dict[str, Any]) -> str:
        """Create formatted Telegram message."""
        ticker = trade_data.get("ticker", "Unknown")
        decision = trade_data.get("decision", "UNKNOWN")
        trade_date = trade_data.get("trade_date", datetime.now().strftime("%Y-%m-%d"))
        summary = trade_data.get("summary", "Trading signal generated")
        
        # Determine emoji based on decision
        if decision == "BUY":
            emoji = "🟢📈"
            action = "BUY Signal"
        elif decision == "SELL":
            emoji = "🔴📉"
            action = "SELL Signal"
        else:
            emoji = "⚪"
            action = f"{decision} Signal"
        
        # Create main message
        message = f"{emoji} *{action}*\n\n"
        message += f"📊 *Ticker:* `{ticker}`\n"
        message += f"📅 *Date:* {trade_date}\n"
        message += f"💭 *Summary:* {summary}\n"
        
        # Add analysis details if available
        full_analysis = trade_data.get("full_analysis", {})
        if full_analysis:
            message += "\n📈 *Analysis Details:*\n"
            
            # Price targets
            if "price_target" in full_analysis:
                message += f"🎯 Target: `{full_analysis['price_target']}`\n"
            
            if "stop_loss" in full_analysis:
                message += f"🛑 Stop Loss: `{full_analysis['stop_loss']}`\n"
            
            # Confidence level
            confidence = trade_data.get("confidence")
            if confidence:
                confidence_pct = int(confidence * 100) if confidence <= 1 else int(confidence)
                message += f"📊 Confidence: `{confidence_pct}%`\n"
            
            # Technical analysis
            if "technical_analysis" in full_analysis:
                tech_analysis = full_analysis["technical_analysis"]
                if len(tech_analysis) > 100:
                    tech_analysis = tech_analysis[:100] + "..."
                message += f"🔧 Technical: {tech_analysis}\n"
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S UTC")
        message += f"\n⏰ *Alert Time:* {timestamp}"
        message += f"\n🤖 *Trading Agents Alert System*"
        
        return message
    
    def test_connection(self) -> bool:
        """Test Telegram bot connection."""
        if not self.is_configured():
            return False
        
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get("ok"):
                    self.logger.info(f"Telegram bot connection successful: {bot_info['result']['username']}")
                    return True
            
            self.logger.error(f"Telegram bot test failed: {response.text}")
            return False
            
        except Exception as e:
            self.logger.error(f"Telegram connection test error: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test trading alert message."""
        test_trade_data = {
            "ticker": "AAPL",
            "decision": "BUY",
            "trade_date": datetime.now().strftime("%Y-%m-%d"),
            "confidence": 0.85,
            "summary": "🧪 This is a test alert from your Trading Agents system!",
            "full_analysis": {
                "price_target": "$185.00",
                "stop_loss": "$165.00",
                "technical_analysis": "RSI oversold, MACD bullish crossover, strong volume"
            }
        }
        
        return self.send_notification(test_trade_data)
    
    def get_chat_id(self) -> Optional[str]:
        """Get chat ID for the bot (useful for setup)."""
        if not self.bot_token:
            return None
        
        try:
            url = f"{self.api_url}/getUpdates"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok") and data.get("result"):
                    # Get the most recent message's chat ID
                    updates = data["result"]
                    if updates:
                        latest_update = updates[-1]
                        if "message" in latest_update:
                            chat_id = latest_update["message"]["chat"]["id"]
                            return str(chat_id)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting chat ID: {e}")
            return None