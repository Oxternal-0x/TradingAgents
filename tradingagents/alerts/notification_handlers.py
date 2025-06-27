import smtplib
import requests
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from abc import ABC, abstractmethod

try:
    import plyer
    DESKTOP_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    DESKTOP_NOTIFICATIONS_AVAILABLE = False

try:
    from twilio.rest import Client as TwilioClient
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False


class NotificationHandler(ABC):
    """Abstract base class for notification handlers."""
    
    @abstractmethod
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send a notification with trade data."""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the handler is properly configured."""
        pass


class EmailNotificationHandler(NotificationHandler):
    """Handles email notifications for trade alerts."""
    
    def __init__(self, config: Dict[str, Any]):
        self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = config.get("smtp_port", 587)
        self.sender_email = config.get("sender_email")
        self.sender_password = config.get("sender_password")
        self.recipient_emails = config.get("recipient_emails", [])
        
        if isinstance(self.recipient_emails, str):
            self.recipient_emails = [self.recipient_emails]
    
    def is_configured(self) -> bool:
        return bool(
            self.sender_email 
            and self.sender_password 
            and self.recipient_emails
        )
    
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send email notification for trade alert."""
        if not self.is_configured():
            logging.warning("Email handler not properly configured")
            return False
        
        try:
            # Create message
            msg = MimeMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)
            msg['Subject'] = f"🚨 Trade Alert: {trade_data['decision']} {trade_data['ticker']}"
            
            # Create email body
            body = self._create_email_body(trade_data)
            msg.attach(MimeText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Email alert sent for {trade_data['ticker']} {trade_data['decision']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")
            return False
    
    def _create_email_body(self, trade_data: Dict[str, Any]) -> str:
        """Create HTML email body."""
        decision_color = {
            'BUY': '#28a745',
            'SELL': '#dc3545', 
            'HOLD': '#ffc107'
        }.get(trade_data['decision'], '#6c757d')
        
        return f"""
        <html>
        <body>
            <h2 style="color: {decision_color};">Trade Alert: {trade_data['decision']} {trade_data['ticker']}</h2>
            <p><strong>Date:</strong> {trade_data['date']}</p>
            <p><strong>Time:</strong> {trade_data['timestamp']}</p>
            <p><strong>Decision:</strong> <span style="color: {decision_color}; font-weight: bold;">{trade_data['decision']}</span></p>
            
            <h3>Analysis Summary:</h3>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                <p>{trade_data.get('summary', 'Full analysis available in system logs.')}</p>
            </div>
            
            <h3>Key Metrics:</h3>
            <ul>
                <li><strong>Market Report:</strong> Available</li>
                <li><strong>Sentiment Analysis:</strong> Available</li>
                <li><strong>News Analysis:</strong> Available</li>
                <li><strong>Fundamentals:</strong> Available</li>
            </ul>
            
            <p><em>This is an automated alert from your Trading Agents system.</em></p>
        </body>
        </html>
        """


class SMSNotificationHandler(NotificationHandler):
    """Handles SMS notifications using Twilio."""
    
    def __init__(self, config: Dict[str, Any]):
        self.account_sid = config.get("twilio_account_sid")
        self.auth_token = config.get("twilio_auth_token")
        self.from_number = config.get("twilio_from_number")
        self.to_numbers = config.get("recipient_numbers", [])
        
        if isinstance(self.to_numbers, str):
            self.to_numbers = [self.to_numbers]
    
    def is_configured(self) -> bool:
        return bool(
            TWILIO_AVAILABLE
            and self.account_sid 
            and self.auth_token 
            and self.from_number
            and self.to_numbers
        )
    
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send SMS notification for trade alert."""
        if not self.is_configured():
            logging.warning("SMS handler not properly configured or Twilio not available")
            return False
        
        try:
            client = TwilioClient(self.account_sid, self.auth_token)
            
            message_body = f"🚨 TRADE ALERT 🚨\n{trade_data['decision']} {trade_data['ticker']}\n{trade_data['date']} {trade_data['timestamp']}\n\nCheck your trading system for full analysis."
            
            for phone_number in self.to_numbers:
                message = client.messages.create(
                    body=message_body,
                    from_=self.from_number,
                    to=phone_number
                )
                logging.info(f"SMS alert sent to {phone_number}: {message.sid}")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to send SMS alert: {e}")
            return False


class SlackNotificationHandler(NotificationHandler):
    """Handles Slack notifications via webhook."""
    
    def __init__(self, config: Dict[str, Any]):
        self.webhook_url = config.get("slack_webhook_url")
        self.channel = config.get("slack_channel", "#trading-alerts")
        self.username = config.get("slack_username", "Trading Bot")
    
    def is_configured(self) -> bool:
        return bool(self.webhook_url)
    
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send Slack notification for trade alert."""
        if not self.is_configured():
            logging.warning("Slack handler not properly configured")
            return False
        
        try:
            # Choose emoji and color based on decision
            emoji_map = {'BUY': '📈', 'SELL': '📉', 'HOLD': '📊'}
            color_map = {'BUY': 'good', 'SELL': 'danger', 'HOLD': 'warning'}
            
            emoji = emoji_map.get(trade_data['decision'], '🔔')
            color = color_map.get(trade_data['decision'], '#36a64f')
            
            payload = {
                "channel": self.channel,
                "username": self.username,
                "icon_emoji": ":chart_with_upwards_trend:",
                "attachments": [
                    {
                        "color": color,
                        "title": f"{emoji} Trade Alert: {trade_data['decision']} {trade_data['ticker']}",
                        "fields": [
                            {
                                "title": "Decision",
                                "value": trade_data['decision'],
                                "short": True
                            },
                            {
                                "title": "Ticker",
                                "value": trade_data['ticker'],
                                "short": True
                            },
                            {
                                "title": "Date",
                                "value": trade_data['date'],
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": trade_data['timestamp'],
                                "short": True
                            }
                        ],
                        "footer": "Trading Agents System",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logging.info(f"Slack alert sent for {trade_data['ticker']} {trade_data['decision']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")
            return False


class DesktopNotificationHandler(NotificationHandler):
    """Handles desktop notifications."""
    
    def __init__(self, config: Dict[str, Any]):
        self.enabled = config.get("desktop_notifications", True)
    
    def is_configured(self) -> bool:
        return DESKTOP_NOTIFICATIONS_AVAILABLE and self.enabled
    
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send desktop notification for trade alert."""
        if not self.is_configured():
            logging.warning("Desktop notifications not available or disabled")
            return False
        
        try:
            title = f"Trade Alert: {trade_data['decision']} {trade_data['ticker']}"
            message = f"Decision: {trade_data['decision']}\nDate: {trade_data['date']}\nTime: {trade_data['timestamp']}"
            
            plyer.notification.notify(
                title=title,
                message=message,
                app_name="Trading Agents",
                timeout=10
            )
            
            logging.info(f"Desktop alert sent for {trade_data['ticker']} {trade_data['decision']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send desktop alert: {e}")
            return False


class WebhookNotificationHandler(NotificationHandler):
    """Handles custom webhook notifications."""
    
    def __init__(self, config: Dict[str, Any]):
        self.webhook_url = config.get("webhook_url")
        self.headers = config.get("webhook_headers", {"Content-Type": "application/json"})
        self.timeout = config.get("webhook_timeout", 10)
    
    def is_configured(self) -> bool:
        return bool(self.webhook_url)
    
    def send_notification(self, trade_data: Dict[str, Any]) -> bool:
        """Send webhook notification for trade alert."""
        if not self.is_configured():
            logging.warning("Webhook handler not properly configured")
            return False
        
        try:
            payload = {
                "alert_type": "trade_signal",
                "ticker": trade_data['ticker'],
                "decision": trade_data['decision'],
                "date": trade_data['date'],
                "timestamp": trade_data['timestamp'],
                "summary": trade_data.get('summary', ''),
                "full_analysis": trade_data.get('full_analysis', {})
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            logging.info(f"Webhook alert sent for {trade_data['ticker']} {trade_data['decision']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send webhook alert: {e}")
            return False