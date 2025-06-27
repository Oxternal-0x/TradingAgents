import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from .notification_handlers import (
    NotificationHandler,
    EmailNotificationHandler,
    SMSNotificationHandler,
    SlackNotificationHandler,
    DesktopNotificationHandler,
    WebhookNotificationHandler,
)


class AlertManager:
    """Manages and coordinates trade alert notifications."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the alert manager with configuration."""
        self.config = config
        self.handlers: List[NotificationHandler] = []
        self.enabled = config.get("alerts_enabled", True)
        self.alert_on_decisions = config.get("alert_on_decisions", ["BUY", "SELL"])
        
        # Initialize handlers based on configuration
        self._initialize_handlers()
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_handlers(self):
        """Initialize notification handlers based on configuration."""
        handler_configs = self.config.get("notification_handlers", {})
        
        # Email handler
        if "email" in handler_configs and handler_configs["email"].get("enabled", False):
            email_handler = EmailNotificationHandler(handler_configs["email"])
            if email_handler.is_configured():
                self.handlers.append(email_handler)
                self.logger.info("Email notification handler initialized")
            else:
                self.logger.warning("Email handler configured but missing required settings")
        
        # SMS handler
        if "sms" in handler_configs and handler_configs["sms"].get("enabled", False):
            sms_handler = SMSNotificationHandler(handler_configs["sms"])
            if sms_handler.is_configured():
                self.handlers.append(sms_handler)
                self.logger.info("SMS notification handler initialized")
            else:
                self.logger.warning("SMS handler configured but missing required settings or Twilio not available")
        
        # Slack handler
        if "slack" in handler_configs and handler_configs["slack"].get("enabled", False):
            slack_handler = SlackNotificationHandler(handler_configs["slack"])
            if slack_handler.is_configured():
                self.handlers.append(slack_handler)
                self.logger.info("Slack notification handler initialized")
            else:
                self.logger.warning("Slack handler configured but missing webhook URL")
        
        # Desktop handler
        if "desktop" in handler_configs and handler_configs["desktop"].get("enabled", True):
            desktop_handler = DesktopNotificationHandler(handler_configs["desktop"])
            if desktop_handler.is_configured():
                self.handlers.append(desktop_handler)
                self.logger.info("Desktop notification handler initialized")
            else:
                self.logger.warning("Desktop notifications not available")
        
        # Webhook handler
        if "webhook" in handler_configs and handler_configs["webhook"].get("enabled", False):
            webhook_handler = WebhookNotificationHandler(handler_configs["webhook"])
            if webhook_handler.is_configured():
                self.handlers.append(webhook_handler)
                self.logger.info("Webhook notification handler initialized")
            else:
                self.logger.warning("Webhook handler configured but missing URL")
        
        if not self.handlers:
            self.logger.warning("No notification handlers configured or available")
    
    def send_trade_alert(
        self, 
        ticker: str, 
        decision: str, 
        trade_date: str,
        full_analysis: Optional[Dict[str, Any]] = None,
        summary: Optional[str] = None
    ) -> Dict[str, bool]:
        """Send trade alert through all configured handlers."""
        if not self.enabled:
            self.logger.info("Alerts are disabled")
            return {}
        
        # Check if we should alert on this decision
        if decision not in self.alert_on_decisions:
            self.logger.info(f"Not alerting on {decision} decision (only alerting on {self.alert_on_decisions})")
            return {}
        
        # Prepare trade data
        now = datetime.now()
        trade_data = {
            "ticker": ticker,
            "decision": decision,
            "date": trade_date,
            "timestamp": now.strftime("%H:%M:%S"),
            "full_timestamp": now.isoformat(),
            "summary": summary or f"Trading decision generated for {ticker}",
            "full_analysis": full_analysis or {}
        }
        
        self.logger.info(f"Sending trade alert: {decision} {ticker} on {trade_date}")
        
        # Send notifications through all handlers
        results = {}
        for handler in self.handlers:
            handler_name = handler.__class__.__name__
            try:
                success = handler.send_notification(trade_data)
                results[handler_name] = success
                if success:
                    self.logger.info(f"Alert sent successfully via {handler_name}")
                else:
                    self.logger.warning(f"Failed to send alert via {handler_name}")
            except Exception as e:
                self.logger.error(f"Error sending alert via {handler_name}: {e}")
                results[handler_name] = False
        
        return results
    
    def test_alerts(self) -> Dict[str, bool]:
        """Test all configured alert handlers."""
        self.logger.info("Testing all alert handlers...")
        
        test_data = {
            "ticker": "TEST",
            "decision": "BUY",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "full_timestamp": datetime.now().isoformat(),
            "summary": "This is a test alert from your Trading Agents system.",
            "full_analysis": {"test": True}
        }
        
        results = {}
        for handler in self.handlers:
            handler_name = handler.__class__.__name__
            try:
                success = handler.send_notification(test_data)
                results[handler_name] = success
                if success:
                    self.logger.info(f"Test alert sent successfully via {handler_name}")
                else:
                    self.logger.warning(f"Test alert failed via {handler_name}")
            except Exception as e:
                self.logger.error(f"Error testing {handler_name}: {e}")
                results[handler_name] = False
        
        return results
    
    def get_handler_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all handlers."""
        status = {}
        for handler in self.handlers:
            handler_name = handler.__class__.__name__
            status[handler_name] = {
                "configured": handler.is_configured(),
                "class": handler.__class__.__name__
            }
        return status
    
    def is_enabled(self) -> bool:
        """Check if alerts are enabled."""
        return self.enabled
    
    def enable_alerts(self):
        """Enable alerts."""
        self.enabled = True
        self.logger.info("Alerts enabled")
    
    def disable_alerts(self):
        """Disable alerts."""
        self.enabled = False
        self.logger.info("Alerts disabled")