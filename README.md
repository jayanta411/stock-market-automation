# 🇮🇳 NSE 250 Stocks - Automated Daily Analysis & Predictions

A complete automation system to analyze India's top 250 NSE stocks by trading volume, generate daily predictions, and provide actionable trading insights.

## 📊 Features

✅ **250 Highest-Volume NSE Stocks** - Automatically tracks and updates top liquid stocks  
✅ **Daily EOD Analysis** - Runs automatically after market close (4:15 PM IST)  
✅ **ML-Based Predictions** - Random Forest model for buy/sell/hold signals  
✅ **Technical Indicators** - RSI, MACD, Bollinger Bands, ATR, Moving Averages  
✅ **One-Pager Dashboard** - Beautiful HTML dashboard with search and filters  
✅ **Historical Tracking** - Complete history of all analyses and volume data  
✅ **Zero Cost** - GitHub Actions + yfinance (all free)  
✅ **Manual & Automated** - Can be triggered manually or scheduled automatically  

## 🚀 Quick Start

### Option 1: Manual Data Fetch (Instant Update)

```bash
# Install dependencies
pip install yfinance scikit-learn pandas numpy

# Fetch and analyze top 250 stocks
python refresh_data.py

# Or update top 250 stocks list + analyze
python refresh_data.py --update-stocks
```

### Option 2: Automatic Daily Runs (GitHub Actions)

No setup needed! The workflow runs automatically at **4:15 PM IST** every trading day.

### Option 3: View Dashboard

Simply open `dashboard.html` in your browser - it will automatically:
- Fetch available analysis dates from GitHub
- Display latest data with live filters
- Allow date selection to view historical results

## 📁 Directory Structure

```
stock-market-automation/
├── dashboard.html                      # 🎨 One-pager interactive dashboard
├── refresh_data.py                     # 🔄 Manual data refresh script
├── fetch_top_stocks.py                 # 📊 Get top 250 stocks by volume
├── indian_stock_analyzer_250.py        # 🔍 Main analysis engine
├── .github/
│   └── workflows/
│       └── daily-250-analysis.yml      # ⚙️ GitHub Actions workflow
└── data/
    ├── top_250_stocks.json             # Latest top 250 stocks
    ├── top_250_stocks.csv              # CSV format
    ├── volume_history/                 # Daily volume snapshots
    ├── volume_history_all.csv          # Complete history
    └── daily_analysis/                 # Daily predictions
        ├── analysis_2024-01-01.json
        ├── analysis_2024-01-01.csv
        ├── buy_signals_2024-01-01.csv
        └── ...
```

## 🎯 How to Use

### 1. **View Dashboard**
- Open `dashboard.html` in any browser
- Select date from dropdown
- Filter by signal (Buy/Sell/Hold) or search stock symbol
- Export results as CSV

### 2. **Fetch Latest Data Today**
```bash
python refresh_data.py
```
This will:
- Analyze all 250 stocks
- Save today's results to `data/daily_analysis/`
- Commit and push to GitHub
- Update the dashboard automatically

### 3. **Schedule Automatic Analysis**
GitHub Actions already configured to run at 4:15 PM IST every trading day (Mon-Fri)

### 4. **Get Only Buy Signals**
Filter by "🚀 Strong Buy" or "✅ Buy" in the dashboard

### 5. **Export Analysis**
Click "Export CSV" button in dashboard to download filtered results

## 📊 Dashboard Features

- **Date Selection** - View any past analysis
- **Signal Filters** - Strong Buy, Buy, Hold, Sell, Strong Sell
- **Search** - Find stocks by symbol
- **Statistics** - See total, buy, sell, hold counts
- **Technical Metrics** - RSI, SMA, Volume, Daily Returns
- **One-Click Export** - Download results as CSV

## 🔔 Signal Explanations

### 🚀 Strong Buy (Score ≥ 5)
- Prediction strongly bullish + Oversold RSI + Positive MACD
- **Action**: Good entry point for swing trading

### ✅ Buy (Score ≥ 2)
- Prediction bullish or RSI < 50 + Positive technical indicators
- **Action**: Consider buying on dips

### 📌 Hold (Score -2 to 2)
- Mixed signals or neutral indicators
- **Action**: Wait for clearer direction

### ⚠️ Sell (Score ≤ -2)
- Prediction bearish or RSI > 70 + Negative technical indicators
- **Action**: Consider taking profits

### ⛔ Strong Sell (Score ≤ -5)
- Prediction strongly bearish + Overbought RSI + Negative MACD
- **Action**: Exit or avoid entry

## 🎯 Included Stocks (Top 250 by Volume)

**Banking & Finance (40+)**
- HDFC, ICICIBANK, AXIS, KOTAKBANK, SBIN, INDUSIND, AUBANK, etc.

**IT & Software (15+)**
- TCS, INFY, WIPRO, HCLTECH, TECHM, LTTS, MINDTREE, etc.

**Energy & Oil (10+)**
- RELIANCE, BPCL, HPCL, GAIL, IOC, ADANIGAS, NTPC, etc.

**Pharma (15+)**
- SUNPHARMA, CIPLA, LUPIN, DIVISLAB, DRREDDY, BIOCON, etc.

**FMCG (15+)**
- ITC, NESTLEIND, BRITANNIA, COLPAL, HINDUNILVR, MARICO, etc.

**Automobiles (10+)**
- MARUTI, MAHINDRA, TATAMOTORS, BAJAJMOTO, EICHERMOT, etc.

**Infrastructure & Metals (20+)**
- LT, JSWSTEEL, SAIL, TATASTEEL, HINDALCO, etc.

**And 110+ more high-volume liquid stocks**

*Note: Excludes all ETFs, BEEs, and illiquid instruments*

## 🔧 Technical Stack

- **Data Source**: yfinance (NSE stocks with `.NS` suffix)
- **Analysis**: scikit-learn (Random Forest)
- **Scheduling**: GitHub Actions
- **Storage**: GitHub repo (free)
- **Dashboard**: Vanilla HTML/JavaScript (no dependencies)
- **Automation**: Python scripts

## 📊 Data Timing

- **Data Delay**: ~15-30 minutes (after market close at 3:30 PM IST)
- **Analysis Runs**: 4:15 PM IST (ensures complete daily data)
- **Dashboard Updates**: Within 5 minutes of analysis completion
- **Best for**: EOD swing trading & next-day decisions

## 💡 Usage Tips

1. **Use BUY signals** - Filter and sort by confidence level
2. **Check RSI** - Overbought (>70) may indicate pullback opportunity
3. **Monitor Volume** - High volume increases signal reliability
4. **Review History** - Check past predictions to validate model accuracy
5. **Combine Signals** - Wait for confirmation from multiple indicators

## ⚠️ Disclaimer

- This is for **educational purposes** only
- **Not financial advice** - Do your own research before trading
- Past performance ≠ Future results
- Use these signals as supplementary analysis, not sole decision maker
- Risk management is crucial - Always use stop losses

## 🛠️ Customization

### Add/Remove Stocks

Edit `fetch_top_stocks.py` - `nse_stocks` set:
```python
nse_stocks = {
    'RELIANCE.NS',
    'INFY.NS',
    # Add or remove as needed
}
```

### Change Analysis Time

Edit `.github/workflows/daily-250-analysis.yml`:
```yaml
# Change cron to your preferred time
- cron: '45 10 * * 1-5'  # IST 4:15 PM = UTC 10:45 AM
```

### Modify Signals

Edit `indian_stock_analyzer_250.py` - `_generate_signal()` method

## 📞 Troubleshooting

**"No data available"**
- Check if analysis has run today
- Verify dates in dropdown are populated
- GitHub Actions may not have executed yet

**"Failed to load data"**
- Ensure `data/daily_analysis/` folder exists
- Check browser console for CORS issues
- Try refreshing or using a different browser

**"Dashboard shows old data"**
- Click "🔄 Refresh" button
- Or manually run `python refresh_data.py`

**"Not getting email notifications"**
- Verify GitHub Secrets are set correctly
- Check spam folder
- Gmail requires app password (not regular password)

## 📈 Performance Notes

- First run: ~30-45 minutes (downloading 250 stocks)
- Subsequent runs: ~20-30 minutes (incremental)
- GitHub Actions provides 2,000 minutes/month free
- All data stored in GitHub repo (free storage)

## 🤝 Contributing

Feel free to:
- Add more stocks to the watchlist
- Improve signal generation logic
- Add more technical indicators
- Create visualizations

## 📄 License

MIT License - Free to use and modify

---

**Made with ❤️ for Indian stock market traders**

Questions? Check GitHub Issues or create a discussion!
