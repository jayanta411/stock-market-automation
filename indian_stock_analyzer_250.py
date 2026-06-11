import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path
import time
from fetch_top_stocks import NSEStockFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianStockAnalyzer250:
    def __init__(self):
        self.fetcher = NSEStockFetcher()
        self.results = []
        self.data_dir = Path('data/daily_analysis')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def load_top_stocks(self):
        top_stocks = self.fetcher.load_top_stocks()
        if top_stocks:
            return [s['ticker'] for s in top_stocks['stocks']]
        else:
            top_250_df = self.fetcher.get_top_250_stocks()
            self.fetcher.save_top_stocks(top_250_df)
            return top_250_df['ticker'].tolist()
    
    def fetch_data(self, ticker, days=365):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            return data if not data.empty else None
        except:
            return None
    
    def calculate_features(self, data):
        if data is None or data.empty or len(data) < 50:
            return None
        try:
            df = data.copy()
            df['SMA_20'] = df['Close'].rolling(20).mean()
            df['SMA_50'] = df['Close'].rolling(50).mean()
            df['SMA_200'] = df['Close'].rolling(200).mean()
            df['RSI'] = self._calculate_rsi(df['Close'])
            df['MACD'] = self._calculate_macd(df['Close'])
            df['Signal_Line'] = df['MACD'].ewm(span=9).mean()
            df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
            df['BB_Middle'] = df['Close'].rolling(20).mean()
            bb_std = df['Close'].rolling(20).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            df['ATR'] = self._calculate_atr(df)
            df['Volume_MA'] = df['Volume'].rolling(20).mean()
            df['Volume_Ratio'] = df['Volume'] / (df['Volume_MA'] + 1)
            df['Returns'] = df['Close'].pct_change() * 100
            df = df.dropna()
            return df if len(df) > 0 else None
        except:
            return None
    
    def _calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices, fast=12, slow=26):
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        return ema_fast - ema_slow
    
    def _calculate_atr(self, df, period=14):
        df_copy = df.copy()
        df_copy['TR'] = np.maximum(
            df_copy['High'] - df_copy['Low'],
            np.maximum(
                abs(df_copy['High'] - df_copy['Close'].shift(1)),
                abs(df_copy['Low'] - df_copy['Close'].shift(1))
            )
        )
        return df_copy['TR'].rolling(window=period).mean()
    
    def predict_next_day(self, ticker, data):
        df = self.calculate_features(data)
        if df is None or len(df) < 50:
            return {'ticker': ticker, 'error': 'Insufficient data'}
        try:
            features = ['SMA_20', 'SMA_50', 'SMA_200', 'RSI', 'MACD', 'MACD_Histogram', 'ATR', 'Volume_Ratio', 'Returns']
            X = df[features][:-1]
            y = (df['Close'].shift(-1) > df['Close']).astype(int)[:-1]
            if len(y) < 50:
                return {'ticker': ticker, 'error': 'Insufficient data'}
            model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X, y)
            prediction_score = model.predict(X.iloc[-1:].values)[0]
            confidence = abs(prediction_score - 0.5) * 2
            current_price = df['Close'].iloc[-1]
            rsi = df['RSI'].iloc[-1]
            macd_hist = df['MACD_Histogram'].iloc[-1]
            sma_20 = df['SMA_20'].iloc[-1]
            sma_50 = df['SMA_50'].iloc[-1]
            bb_upper = df['BB_Upper'].iloc[-1]
            bb_lower = df['BB_Lower'].iloc[-1]
            daily_volume = data['Volume'].iloc[-1]
            volume_ma = df['Volume_MA'].iloc[-1]
            daily_return = df['Returns'].iloc[-1]
            signal = self._generate_signal(prediction_score, rsi, macd_hist, current_price, sma_20, sma_50, bb_upper, bb_lower)
            return {
                'ticker': ticker,
                'symbol': ticker.replace('.NS', ''),
                'current_price': float(current_price),
                'predicted_direction': 'UP' if prediction_score > 0.5 else 'DOWN',
                'confidence': float(confidence),
                'signal': signal,
                'technical_metrics': {
                    'rsi': float(rsi),
                    'sma_20': float(sma_20),
                    'sma_50': float(sma_50),
                    'macd_histogram': float(macd_hist),
                    'volume': float(daily_volume),
                    'volume_ma': float(volume_ma),
                    'daily_return_pct': float(daily_return)
                },
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'ticker': ticker, 'error': str(e)[:50]}
    
    def _generate_signal(self, prediction, rsi, macd_hist, price, sma20, sma50, bb_upper, bb_lower):
        score = 0
        if prediction > 0.6:
            score += 2
        elif prediction > 0.5:
            score += 1
        if rsi < 30:
            score += 2
        elif rsi > 70:
            score -= 2
        elif rsi < 50:
            score += 1
        if macd_hist > 0:
            score += 1
        if price < bb_lower:
            score += 2
        elif price > bb_upper:
            score -= 2
        if sma20 > sma50:
            score += 1
        if score >= 5:
            return "STRONG BUY 🚀"
        elif score >= 2:
            return "BUY ✅"
        elif score <= -5:
            return "STRONG SELL ⛔"
        elif score <= -2:
            return "SELL ⚠️"
        else:
            return "HOLD 📌"
    
    def analyze_all_stocks(self):
        stocks = self.load_top_stocks()
        logger.info(f"Analyzing {len(stocks)} stocks...")
        print(f"\n{'='*100}")
        print(f"{'Symbol':<10} {'Signal':<15} {'Price':<12} {'RSI':<8} {'Confidence':<12} {'Volume':<15}")
        print(f"{'='*100}")
        
        for idx, ticker in enumerate(stocks, 1):
            try:
                data = self.fetch_data(ticker)
                if data is not None:
                    prediction = self.predict_next_day(ticker, data)
                    self.results.append(prediction)
                    if 'error' not in prediction:
                        symbol = prediction['symbol']
                        signal = prediction['signal']
                        price = prediction['current_price']
                        rsi = prediction['technical_metrics']['rsi']
                        conf = prediction['confidence']
                        volume = prediction['technical_metrics']['volume']
                        print(f"{symbol:<10} {signal:<15} ₹{price:<11.2f} {rsi:<7.1f} {conf:<11.1%} {volume:<15,.0f}")
                if idx % 20 == 0:
                    time.sleep(1)
            except:
                pass
        print(f"{'='*100}")
        return self.results
    
    def save_results(self, results):
        today = datetime.now().strftime('%Y-%m-%d')
        json_file = self.data_dir / f"analysis_{today}.json"
        with open(json_file, 'w') as f:
            json.dump({'generated_at': datetime.now().isoformat(), 'total_analyzed': len(results), 'results': results}, f, indent=2)
        
        valid_results = [r for r in results if 'error' not in r]
        if valid_results:
            df = pd.DataFrame([{'Symbol': r['symbol'], 'Price_INR': r['current_price'], 'Signal': r['signal'], 'Confidence': f"{r['confidence']:.1%}", 'RSI': f"{r['technical_metrics']['rsi']:.1f}", 'SMA_20': f"{r['technical_metrics']['sma_20']:.2f}", 'Volume': f"{r['technical_metrics']['volume']:,.0f}", 'Daily_Return_%': f"{r['technical_metrics']['daily_return_pct']:.2f}"} for r in valid_results])
            csv_file = self.data_dir / f"analysis_{today}.csv"
            df.to_csv(csv_file, index=False)
    
    def run(self):
        results = self.analyze_all_stocks()
        self.save_results(results)
        valid_results = [r for r in results if 'error' not in r]
        buy_signals = [r for r in valid_results if 'BUY' in r['signal']]
        print(f"\n{'='*50}")
        print(f"✓ Analysis Summary:")
        print(f"  Total Analyzed: {len(valid_results)}")
        print(f"  BUY Signals: {len(buy_signals)}")
        print(f"{'='*50}")

if __name__ == "__main__":
    analyzer = IndianStockAnalyzer250()
    analyzer.run()
