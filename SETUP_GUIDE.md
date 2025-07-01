# TradingAgents Setup Guide

## Quick Start Guide

This guide will help you set up and run the TradingAgents framework on your system.

## Prerequisites

- Python 3.10+ (you have 3.13.3 ✅)
- Virtual environment (already created ✅)
- Dependencies installed (already done ✅)

## Required API Keys

To run TradingAgents, you need two main API keys:

### 1. FINNHUB API Key (Required)
- **Purpose**: Financial market data
- **Cost**: Free tier available
- **How to get**:
  1. Go to [finnhub.io](https://finnhub.io)
  2. Sign up for a free account
  3. Get your API key from the dashboard

### 2. LLM Provider API Key (Required)

Choose one of these options:

#### Option A: Google Gemini (Recommended - Currently configured)
- **Purpose**: AI model for analysis
- **Cost**: Free tier available with generous limits
- **How to get**:
  1. Go to [ai.google.dev](https://ai.google.dev)
  2. Click "Get API key"
  3. Create a new project or use existing
  4. Generate API key

#### Option B: OpenAI (Alternative)
- **Purpose**: AI model for analysis  
- **Cost**: Pay-per-use (can be expensive with many agents)
- **How to get**:
  1. Go to [platform.openai.com](https://platform.openai.com)
  2. Create account and add payment method
  3. Go to API keys section
  4. Create new API key

## Setup Instructions

### Step 1: Set Environment Variables

**For Google Gemini (current configuration):**
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
export FINNHUB_API_KEY="your_finnhub_api_key_here"
```

**For OpenAI (if you prefer):**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export FINNHUB_API_KEY="your_finnhub_api_key_here"
```

### Step 2: Choose Your Configuration

#### Option 1: Use Google Gemini (main.py default)
```bash
source tradingagents-env/bin/activate
python main.py
```

#### Option 2: Use OpenAI (modify config)
Edit `main.py` and change:
```python
config["llm_provider"] = "openai"
config["backend_url"] = "https://api.openai.com/v1"
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"
```

#### Option 3: Use the Interactive CLI
```bash
source tradingagents-env/bin/activate
python -m cli.main
```

## Running Your First Analysis

1. **Start with a simple example** (SPY ETF on recent date):
   ```python
   ta = TradingAgentsGraph(debug=True, config=config)
   _, decision = ta.propagate("SPY", "2024-12-01")
   print(decision)
   ```

2. **Key parameters to adjust for testing**:
   - `max_debate_rounds = 1` (reduce to save API calls)
   - `online_tools = False` (use cached data for testing)

## Cost Optimization Tips

1. **Start with smaller models**: Use `gpt-4o-mini` or `gemini-flash` instead of premium models
2. **Reduce debate rounds**: Set `max_debate_rounds = 1` for initial testing
3. **Use cached data**: Set `online_tools = False` to avoid repeated API calls
4. **Test with one agent**: Start by testing individual agents before full workflow

## Troubleshooting

### Error: "DefaultCredentialsError"
- You need to set the `GOOGLE_API_KEY` environment variable
- Run: `export GOOGLE_API_KEY="your_key_here"`

### Error: "Invalid API key"
- Double-check your API key is correct
- Make sure it's properly set in environment variables

### Error: "Rate limit exceeded"
- You're hitting API limits - wait a few minutes
- Consider upgrading your API plan
- Reduce `max_debate_rounds` to make fewer calls

### High API costs
- Switch to smaller models (gpt-4o-mini, gemini-flash)
- Set `online_tools = False` for testing
- Reduce `max_debate_rounds` and `max_risk_discuss_rounds`

## Next Steps

Once you have it running:

1. **Experiment with different stocks**: Try "AAPL", "TSLA", "NVDA"
2. **Adjust the analysis date**: Use different market conditions
3. **Modify the configuration**: Try different LLM models
4. **Explore the CLI**: Use `python -m cli.main` for interactive mode
5. **Read the code**: Explore the `tradingagents/` directory to understand how it works

## Contributing Ideas

Since you forked this project, here are ways you could contribute:

1. **Documentation improvements**: Add more examples, better error handling
2. **Cost optimization**: Add features to reduce API usage
3. **New LLM providers**: Add support for other models (Anthropic, etc.)
4. **Better visualization**: Improve the CLI interface
5. **Backtesting tools**: Add historical performance analysis
6. **Risk management**: Improve the risk assessment algorithms

Good luck with your trading agents! 🚀📈