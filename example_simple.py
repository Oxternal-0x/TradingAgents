"""
Simple TradingAgents Example
============================

This is a minimal example to test your TradingAgents setup.
Make sure you have your API keys set as environment variables:

export GOOGLE_API_KEY="your_google_api_key"
export FINNHUB_API_KEY="your_finnhub_api_key"

Or for OpenAI:
export OPENAI_API_KEY="your_openai_api_key"
export FINNHUB_API_KEY="your_finnhub_api_key"
"""

import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def main():
    print("🚀 Starting TradingAgents Simple Example")
    print("=" * 50)
    
    # Check if API keys are set
    google_key = os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    
    if not finnhub_key:
        print("❌ ERROR: FINNHUB_API_KEY not found!")
        print("Please set: export FINNHUB_API_KEY='your_key_here'")
        return
    
    if not google_key and not openai_key:
        print("❌ ERROR: No LLM API key found!")
        print("Please set either:")
        print("  export GOOGLE_API_KEY='your_key_here'")
        print("  OR")
        print("  export OPENAI_API_KEY='your_key_here'")
        return
    
    print("✅ API keys found!")
    
    # Create configuration - optimized for low cost testing
    config = DEFAULT_CONFIG.copy()
    
    if google_key:
        print("🤖 Using Google Gemini")
        config["llm_provider"] = "google"
        config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
        config["deep_think_llm"] = "gemini-2.0-flash"
        config["quick_think_llm"] = "gemini-2.0-flash"
    else:
        print("🤖 Using OpenAI")
        config["llm_provider"] = "openai"
        config["backend_url"] = "https://api.openai.com/v1"
        config["deep_think_llm"] = "gpt-4o-mini"  # Cheaper model
        config["quick_think_llm"] = "gpt-4o-mini"  # Cheaper model
    
    # Optimize for testing (reduce API calls and costs)
    config["max_debate_rounds"] = 1  # Reduce debates to save API calls
    config["max_risk_discuss_rounds"] = 1  # Reduce risk discussions
    config["online_tools"] = True  # Use real-time data (set False for cached data)
    
    print(f"⚙️  Configuration:")
    print(f"   Provider: {config['llm_provider']}")
    print(f"   Model: {config['deep_think_llm']}")
    print(f"   Debate rounds: {config['max_debate_rounds']}")
    print(f"   Online tools: {config['online_tools']}")
    print()
    
    # Initialize TradingAgents
    print("🔧 Initializing TradingAgents...")
    try:
        ta = TradingAgentsGraph(debug=True, config=config)
        print("✅ TradingAgents initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your API keys are correct")
        print("2. Make sure you have internet connection")
        print("3. Try running: source tradingagents-env/bin/activate")
        return
    
    # Run analysis
    ticker = "SPY"  # S&P 500 ETF - safe choice for testing
    date = "2024-12-01"  # Recent date
    
    print(f"📊 Running analysis for {ticker} on {date}")
    print("⏳ This may take 2-5 minutes depending on the model...")
    print("   You'll see debug output showing agent activity")
    print("-" * 50)
    
    try:
        # Run the analysis
        final_state, decision = ta.propagate(ticker, date)
        
        print("\n" + "=" * 50)
        print("📋 ANALYSIS COMPLETE!")
        print("=" * 50)
        print(f"📈 Trading Decision for {ticker}:")
        print(decision)
        print("\n🎉 Success! Your TradingAgents setup is working!")
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        print("\nPossible issues:")
        print("1. API rate limits - wait a few minutes and try again")
        print("2. Invalid ticker symbol - try 'AAPL' or 'MSFT'")
        print("3. Network issues - check your connection")
        print("4. API quota exceeded - check your API usage")

if __name__ == "__main__":
    main()