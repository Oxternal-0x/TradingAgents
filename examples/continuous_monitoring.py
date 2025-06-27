#!/usr/bin/env python3
"""
Continuous Trading Monitoring with Alerts

This script continuously monitors specified stocks and sends alerts when
BUY or SELL signals are generated.

Features:
- Monitor multiple stocks
- Configurable monitoring intervals
- Automatic retry on failures
- Logging of all activities
- Alert rate limiting to prevent spam
"""

import sys
import os
import time
import logging
import schedule
from datetime import datetime, timedelta, date
from typing import List, Dict, Any

# Add the parent directory to the path to import tradingagents
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.alerts.config_template import DESKTOP_ONLY_CONFIG


class TradingMonitor:
    """Continuous trading monitor with alerting."""
    
    def __init__(self, config: Dict[str, Any], tickers: List[str], 
                 alert_config: Dict[str, Any] = None):
        """
        Initialize the trading monitor.
        
        Args:
            config: Trading system configuration
            tickers: List of stock tickers to monitor
            alert_config: Alert system configuration
        """
        self.tickers = tickers
        self.config = config.copy()
        
        # Add alert config if provided
        if alert_config:
            self.config["alert_config"] = alert_config
        
        # Initialize trading system
        self.trading_system = TradingAgentsGraph(debug=False, config=self.config)
        
        # Set up logging
        self._setup_logging()
        
        # Track last alerts to prevent spam
        self.last_alerts = {}  # ticker -> (decision, timestamp)
        self.alert_cooldown = timedelta(hours=1)  # Don't repeat same alert within 1 hour
        
        # Statistics
        self.stats = {
            "analyses_run": 0,
            "alerts_sent": 0,
            "errors": 0,
            "start_time": datetime.now()
        }
        
        self.logger.info(f"Trading monitor initialized for tickers: {', '.join(tickers)}")
    
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('TradingMonitor')
    
    def should_send_alert(self, ticker: str, decision: str) -> bool:
        """Check if we should send an alert based on cooldown."""
        if ticker not in self.last_alerts:
            return True
        
        last_decision, last_time = self.last_alerts[ticker]
        
        # Don't send if same decision within cooldown period
        if (last_decision == decision and 
            datetime.now() - last_time < self.alert_cooldown):
            return False
        
        return True
    
    def analyze_ticker(self, ticker: str, trade_date: str = None) -> Dict[str, Any]:
        """
        Analyze a single ticker and send alerts if needed.
        
        Args:
            ticker: Stock ticker to analyze
            trade_date: Date for analysis (defaults to today)
        
        Returns:
            Analysis results
        """
        if trade_date is None:
            trade_date = date.today().strftime("%Y-%m-%d")
        
        try:
            self.logger.info(f"Analyzing {ticker} for {trade_date}")
            
            # Run analysis
            final_state, decision = self.trading_system.propagate(ticker, trade_date)
            self.stats["analyses_run"] += 1
            
            # Check if we should send alert
            if decision in ["BUY", "SELL"] and self.should_send_alert(ticker, decision):
                self.logger.info(f"Alert-worthy decision for {ticker}: {decision}")
                self.last_alerts[ticker] = (decision, datetime.now())
                self.stats["alerts_sent"] += 1
            else:
                self.logger.info(f"No alert needed for {ticker}: {decision}")
            
            return {
                "ticker": ticker,
                "decision": decision,
                "trade_date": trade_date,
                "success": True,
                "final_state": final_state
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing {ticker}: {e}")
            self.stats["errors"] += 1
            return {
                "ticker": ticker,
                "decision": "ERROR",
                "trade_date": trade_date,
                "success": False,
                "error": str(e)
            }
    
    def run_analysis_cycle(self, trade_date: str = None):
        """Run analysis for all configured tickers."""
        self.logger.info(f"Starting analysis cycle for {len(self.tickers)} tickers")
        
        results = []
        for ticker in self.tickers:
            result = self.analyze_ticker(ticker, trade_date)
            results.append(result)
            
            # Small delay between tickers to avoid rate limiting
            time.sleep(1)
        
        # Log cycle summary
        successful = sum(1 for r in results if r["success"])
        alerts_sent = sum(1 for r in results if r.get("decision") in ["BUY", "SELL"])
        
        self.logger.info(
            f"Analysis cycle complete: {successful}/{len(results)} successful, "
            f"{alerts_sent} potential alerts"
        )
        
        return results
    
    def print_stats(self):
        """Print monitoring statistics."""
        runtime = datetime.now() - self.stats["start_time"]
        
        print("\n📊 Trading Monitor Statistics")
        print("=" * 40)
        print(f"Runtime: {runtime}")
        print(f"Analyses run: {self.stats['analyses_run']}")
        print(f"Alerts sent: {self.stats['alerts_sent']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Monitored tickers: {', '.join(self.tickers)}")
        
        # Show last alert for each ticker
        if self.last_alerts:
            print(f"\n📱 Recent Alerts:")
            for ticker, (decision, timestamp) in self.last_alerts.items():
                print(f"  {ticker}: {decision} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def test_system(self):
        """Test the monitoring system."""
        print("🧪 Testing trading monitor system...")
        
        # Test alert system
        if self.trading_system.alert_manager:
            print("Testing alert system...")
            alert_results = self.trading_system.test_alerts()
            if any(alert_results.values()) if alert_results else False:
                print("✅ Alert system working")
            else:
                print("❌ Alert system not working properly")
        else:
            print("⚠️  No alert system configured")
        
        # Test analysis on first ticker
        if self.tickers:
            print(f"Testing analysis on {self.tickers[0]}...")
            result = self.analyze_ticker(self.tickers[0])
            if result["success"]:
                print(f"✅ Analysis working - Decision: {result['decision']}")
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        
        return True


def create_monitor_config():
    """Create a default monitoring configuration."""
    config = DEFAULT_CONFIG.copy()
    
    # Use Google's models (adjust as needed)
    config["llm_provider"] = "google"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["max_debate_rounds"] = 1  # Faster analysis
    config["online_tools"] = True
    
    return config


def main():
    """Main function for continuous monitoring."""
    # Configuration
    TICKERS_TO_MONITOR = ["NVDA", "AAPL", "TSLA", "MSFT", "GOOGL"]  # Customize this list
    MONITORING_INTERVAL_HOURS = 4  # How often to check (in hours)
    
    print("🚨 Trading Agents Continuous Monitor")
    print("=" * 50)
    print(f"Monitoring: {', '.join(TICKERS_TO_MONITOR)}")
    print(f"Check interval: Every {MONITORING_INTERVAL_HOURS} hours")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create configuration
    config = create_monitor_config()
    alert_config = DESKTOP_ONLY_CONFIG  # Use desktop alerts by default
    
    # Initialize monitor
    monitor = TradingMonitor(
        config=config,
        tickers=TICKERS_TO_MONITOR,
        alert_config=alert_config
    )
    
    # Test the system first
    print("\n🧪 Testing system before starting monitoring...")
    monitor.test_system()
    
    # Set up scheduled monitoring
    schedule.every(MONITORING_INTERVAL_HOURS).hours.do(monitor.run_analysis_cycle)
    
    # Also run immediately
    print(f"\n🚀 Starting monitoring loop...")
    monitor.run_analysis_cycle()
    
    # Main monitoring loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled jobs
            
            # Print stats every hour
            if datetime.now().minute == 0:
                monitor.print_stats()
                
    except KeyboardInterrupt:
        print(f"\n🛑 Monitoring stopped by user")
        monitor.print_stats()
        
    except Exception as e:
        print(f"\n❌ Monitoring stopped due to error: {e}")
        monitor.logger.error(f"Monitoring stopped: {e}")


if __name__ == "__main__":
    main()