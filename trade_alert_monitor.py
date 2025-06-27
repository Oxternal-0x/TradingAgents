#!/usr/bin/env python3
"""
Trade Entry Alert Monitor for TradingAgents
Monitors for BUY signals and sends alerts via multiple channels
"""

import os
import json
import time
import logging
import smtplib
import requests
from datetime import datetime, date, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from pathlib import Path
from typing import List, Dict, Optional, Union
import schedule
import argparse

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trade_alerts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradeAlertMonitor:
    """Monitor for trade entry signals and send alerts."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the monitor with configuration."""
        self.config = config or DEFAULT_CONFIG.copy()
        self.alert_history_file = "alert_history.json"
        self.alert_history = self._load_alert_history()
        
        # Alert configuration (set these via environment variables)
        self.email_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'sender_email': os.getenv('SENDER_EMAIL'),
            'sender_password': os.getenv('SENDER_PASSWORD'),
            'recipient_emails': os.getenv('RECIPIENT_EMAILS', '').split(',') if os.getenv('RECIPIENT_EMAILS') else []
        }
        
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        self.slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        
        # Initialize TradingAgents graph
        self.trading_graph = TradingAgentsGraph(debug=False, config=self.config)
        
        logger.info("Trade Alert Monitor initialized")
    
    def _load_alert_history(self) -> Dict:
        """Load alert history from file."""
        if os.path.exists(self.alert_history_file):
            try:
                with open(self.alert_history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading alert history: {e}")
                return {}
        return {}
    
    def _save_alert_history(self):
        """Save alert history to file."""
        try:
            with open(self.alert_history_file, 'w') as f:
                json.dump(self.alert_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving alert history: {e}")
    
    def check_for_trade_entries(self, tickers: List[str], trade_date: Optional[str] = None) -> List[Dict]:
        """Check for BUY signals across multiple tickers."""
        if trade_date is None:
            trade_date = datetime.now().strftime("%Y-%m-%d")
        
        trade_entries = []
        
        for ticker in tickers:
            try:
                logger.info(f"Analyzing {ticker} for {trade_date}")
                
                # Run the trading analysis
                final_state, decision = self.trading_graph.propagate(ticker, trade_date)
                
                # Check if it's a BUY signal
                if decision.upper().strip() == "BUY":
                    # Create unique key for this alert
                    alert_key = f"{ticker}_{trade_date}_{decision}"
                    
                    # Check if we've already alerted for this exact signal
                    if alert_key not in self.alert_history:
                        trade_entry = {
                            'ticker': ticker,
                            'date': trade_date,
                            'decision': decision,
                            'timestamp': datetime.now().isoformat(),
                            'analysis_summary': self._extract_analysis_summary(final_state),
                            'confidence_indicators': self._extract_confidence_indicators(final_state)
                        }
                        
                        trade_entries.append(trade_entry)
                        
                        # Mark as alerted
                        self.alert_history[alert_key] = {
                            'timestamp': datetime.now().isoformat(),
                            'alerted': True
                        }
                        
                        logger.info(f"🚨 TRADE ENTRY DETECTED: {ticker} - {decision}")
                    else:
                        logger.info(f"Already alerted for {ticker} {decision} on {trade_date}")
                else:
                    logger.info(f"{ticker}: {decision} (no entry signal)")
                    
            except Exception as e:
                logger.error(f"Error analyzing {ticker}: {e}")
                continue
        
        self._save_alert_history()
        return trade_entries
    
    def _extract_analysis_summary(self, final_state: Dict) -> str:
        """Extract key points from the analysis for the alert."""
        summary = []
        
        # Get the final decision reasoning
        if 'final_trade_decision' in final_state:
            # Extract first 200 characters of the decision reasoning
            decision_text = final_state['final_trade_decision'][:200] + "..."
            summary.append(f"Decision Reasoning: {decision_text}")
        
        # Get key analyst insights
        if 'market_report' in final_state and final_state['market_report']:
            summary.append("✅ Market Analysis: Completed")
        
        if 'sentiment_report' in final_state and final_state['sentiment_report']:
            summary.append("✅ Sentiment Analysis: Completed")
            
        if 'news_report' in final_state and final_state['news_report']:
            summary.append("✅ News Analysis: Completed")
            
        if 'fundamentals_report' in final_state and final_state['fundamentals_report']:
            summary.append("✅ Fundamentals Analysis: Completed")
        
        return "\n".join(summary)
    
    def _extract_confidence_indicators(self, final_state: Dict) -> Dict:
        """Extract confidence indicators from the analysis."""
        indicators = {
            'analyst_consensus': 'Unknown',
            'risk_assessment': 'Unknown',
            'debate_rounds': 0
        }
        
        # Check investment debate state
        if 'investment_debate_state' in final_state:
            debate_state = final_state['investment_debate_state']
            if 'count' in debate_state:
                indicators['debate_rounds'] = debate_state['count']
        
        # Check risk debate state
        if 'risk_debate_state' in final_state:
            risk_state = final_state['risk_debate_state']
            if 'judge_decision' in risk_state and risk_state['judge_decision']:
                # Simple sentiment analysis of the risk decision
                risk_text = risk_state['judge_decision'].lower()
                if 'high confidence' in risk_text or 'strong buy' in risk_text:
                    indicators['risk_assessment'] = 'High Confidence'
                elif 'moderate' in risk_text or 'cautious' in risk_text:
                    indicators['risk_assessment'] = 'Moderate'
                else:
                    indicators['risk_assessment'] = 'Standard'
        
        return indicators
    
    def send_email_alert(self, trade_entries: List[Dict]):
        """Send email alerts for trade entries."""
        if not self.email_config['sender_email'] or not self.email_config['recipient_emails'][0]:
            logger.warning("Email configuration missing, skipping email alerts")
            return
        
        try:
            # Create email content
            subject = f"🚨 TRADE ENTRY ALERT - {len(trade_entries)} BUY Signal{'s' if len(trade_entries) > 1 else ''}"
            
            body = self._create_email_body(trade_entries)
            
            # Create message
            msg = MimeMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(self.email_config['recipient_emails'])
            msg['Subject'] = subject
            
            msg.attach(MimeText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])
            
            for recipient in self.email_config['recipient_emails']:
                if recipient.strip():
                    server.send_message(msg, to_addrs=[recipient.strip()])
            
            server.quit()
            logger.info(f"Email alert sent for {len(trade_entries)} trade entries")
            
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")
    
    def _create_email_body(self, trade_entries: List[Dict]) -> str:
        """Create HTML email body for trade entries."""
        html = """
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2E7D32;">🚨 TradingAgents Trade Entry Alert</h2>
            <p>New BUY signals detected:</p>
        """
        
        for entry in trade_entries:
            html += f"""
            <div style="border: 1px solid #4CAF50; margin: 10px 0; padding: 15px; border-radius: 5px; background-color: #F1F8E9;">
                <h3 style="color: #2E7D32; margin-top: 0;">📈 {entry['ticker']} - {entry['decision']}</h3>
                <p><strong>Date:</strong> {entry['date']}</p>
                <p><strong>Timestamp:</strong> {entry['timestamp']}</p>
                <p><strong>Risk Assessment:</strong> {entry['confidence_indicators']['risk_assessment']}</p>
                <p><strong>Debate Rounds:</strong> {entry['confidence_indicators']['debate_rounds']}</p>
                
                <h4>Analysis Summary:</h4>
                <div style="background-color: #FFFFFF; padding: 10px; border-radius: 3px; font-size: 12px;">
                    <pre style="white-space: pre-wrap;">{entry['analysis_summary']}</pre>
                </div>
            </div>
            """
        
        html += """
            <br>
            <p style="font-size: 12px; color: #666;">
                This alert was generated by TradingAgents Trade Monitor.<br>
                <strong>Disclaimer:</strong> This is for informational purposes only and not financial advice.
            </p>
        </body>
        </html>
        """
        
        return html
    
    def send_discord_alert(self, trade_entries: List[Dict]):
        """Send Discord webhook alerts."""
        if not self.discord_webhook:
            logger.warning("Discord webhook URL not configured, skipping Discord alerts")
            return
        
        try:
            for entry in trade_entries:
                embed = {
                    "title": f"🚨 Trade Entry Alert: {entry['ticker']}",
                    "description": f"**{entry['decision']}** signal detected",
                    "color": 0x4CAF50,  # Green color
                    "fields": [
                        {"name": "Ticker", "value": entry['ticker'], "inline": True},
                        {"name": "Date", "value": entry['date'], "inline": True},
                        {"name": "Risk Assessment", "value": entry['confidence_indicators']['risk_assessment'], "inline": True},
                    ],
                    "footer": {"text": "TradingAgents Monitor"},
                    "timestamp": entry['timestamp']
                }
                
                payload = {"embeds": [embed]}
                
                response = requests.post(self.discord_webhook, json=payload)
                response.raise_for_status()
                
            logger.info(f"Discord alert sent for {len(trade_entries)} trade entries")
            
        except Exception as e:
            logger.error(f"Error sending Discord alert: {e}")
    
    def send_slack_alert(self, trade_entries: List[Dict]):
        """Send Slack webhook alerts."""
        if not self.slack_webhook:
            logger.warning("Slack webhook URL not configured, skipping Slack alerts")
            return
        
        try:
            for entry in trade_entries:
                blocks = [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 Trade Entry: {entry['ticker']} - {entry['decision']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Date:* {entry['date']}"},
                            {"type": "mrkdwn", "text": f"*Risk:* {entry['confidence_indicators']['risk_assessment']}"},
                        ]
                    },
                    {"type": "divider"}
                ]
                
                payload = {"blocks": blocks}
                
                response = requests.post(self.slack_webhook, json=payload)
                response.raise_for_status()
                
            logger.info(f"Slack alert sent for {len(trade_entries)} trade entries")
            
        except Exception as e:
            logger.error(f"Error sending Slack alert: {e}")
    
    def send_alerts(self, trade_entries: List[Dict]):
        """Send alerts via all configured channels."""
        if not trade_entries:
            logger.info("No trade entries to alert")
            return
        
        logger.info(f"Sending alerts for {len(trade_entries)} trade entries")
        
        # Send alerts via all configured channels
        self.send_email_alert(trade_entries)
        self.send_discord_alert(trade_entries)
        self.send_slack_alert(trade_entries)
    
    def monitor_tickers(self, tickers: List[str], trade_date: Optional[str] = None):
        """Monitor tickers and send alerts for trade entries."""
        logger.info(f"Starting monitoring for tickers: {', '.join(tickers)}")
        
        trade_entries = self.check_for_trade_entries(tickers, trade_date)
        
        if trade_entries:
            self.send_alerts(trade_entries)
            logger.info(f"✅ Monitoring complete - {len(trade_entries)} alerts sent")
        else:
            logger.info("✅ Monitoring complete - no trade entries detected")

def create_sample_config():
    """Create a sample configuration file."""
    config_content = """# TradingAgents Alert Monitor Configuration

# Email Configuration (Gmail example)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"  # Use app password for Gmail
export RECIPIENT_EMAILS="alert1@email.com,alert2@email.com"

# Discord Configuration
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

# Slack Configuration
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WEBHOOK_URL"

# API Keys for TradingAgents
export FINNHUB_API_KEY="your_finnhub_api_key"
export OPENAI_API_KEY="your_openai_api_key"
"""
    
    with open("alert_config.env", "w") as f:
        f.write(config_content)
    
    print("Sample configuration file created: alert_config.env")
    print("Please edit this file with your actual configuration values.")

def main():
    parser = argparse.ArgumentParser(description="TradingAgents Trade Entry Alert Monitor")
    parser.add_argument("--tickers", nargs="+", default=["SPY", "QQQ", "AAPL"], 
                       help="Tickers to monitor (default: SPY QQQ AAPL)")
    parser.add_argument("--date", type=str, help="Trade date (YYYY-MM-DD, default: today)")
    parser.add_argument("--schedule", type=str, choices=["hourly", "daily", "manual"], 
                       default="manual", help="Schedule type (default: manual)")
    parser.add_argument("--create-config", action="store_true", 
                       help="Create sample configuration file")
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    # Initialize monitor
    monitor = TradeAlertMonitor()
    
    if args.schedule == "manual":
        # Run once
        monitor.monitor_tickers(args.tickers, args.date)
    elif args.schedule == "hourly":
        # Schedule to run every hour during market hours
        schedule.every().hour.at(":00").do(monitor.monitor_tickers, args.tickers)
        logger.info("Scheduled hourly monitoring - press Ctrl+C to stop")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    elif args.schedule == "daily":
        # Schedule to run daily at market open (9:30 AM ET)
        schedule.every().day.at("09:30").do(monitor.monitor_tickers, args.tickers)
        logger.info("Scheduled daily monitoring at 9:30 AM - press Ctrl+C to stop")
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    main()