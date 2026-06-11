import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NSEStockFetcher:
    def __init__(self):
        self.cache_dir = Path('data/stock_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.top_stocks_file = 'data/top_250_stocks.json'
        self.volume_history_dir = Path('data/volume_history')
        self.volume_history_dir.mkdir(parents=True, exist_ok=True)
        
    def get_nse_stock_list(self):
        """Get comprehensive list of NSE stocks"""
        nse_stocks = {
            'HDFC.NS', 'ICICIBANK.NS', 'AXIS.NS', 'KOTAKBANK.NS', 'SBIN.NS',
            'INDUSIND.NS', 'AUBANK.NS', 'FEDERALBANK.NS', 'IDFCBANK.NS', 'IDBI.NS',
            'BANKBARODA.NS', 'PNB.NS', 'CANBANK.NS', 'UNIONBANK.NS', 'CENTRALBANK.NS',
            'HSBC.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'LT.NS',
            'HDFCLIFE.NS', 'ICICIPRULI.NS', 'SBILIFE.NS', 'MAXHEALTH.NS',
            'TCS.NS', 'INFY.NS', 'WIPRO.NS', 'HCLTECH.NS', 'TECHM.NS',
            'LTTS.NS', 'MINDTREE.NS', 'MPHASIS.NS', 'PERSISTENT.NS', 'COFORGE.NS',
            'RELIANCE.NS', 'BPCL.NS', 'HPCL.NS', 'GAIL.NS', 'IOC.NS',
            'ADANIGAS.NS', 'ADANIGREEN.NS', 'ADANIPOWER.NS', 'NTPC.NS', 'POWER.NS',
            'TATAPOWER.NS', 'TORNTPOWER.NS', 'THERMAX.NS',
            'MARUTI.NS', 'MAHINDRA.NS', 'TATAMOTORS.NS', 'BAJAJMOTO.NS', 'EICHERMOT.NS',
            'ASHOKLEY.NS', 'BOSCHLTD.NS', 'BHEL.NS', 'CUMMINSIND.NS',
            'SUNPHARMA.NS', 'CIPLA.NS', 'LUPIN.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
            'BAJAJPHARM.NS', 'GLENMARK.NS', 'ALKEM.NS', 'AUPHARMACY.NS', 'BIOCON.NS',
            'MANKIND.NS', 'NATCPHARMA.NS', 'STERLINBIO.NS', 'IPCALAB.NS', 'AUROPHARMA.NS',
            'ITC.NS', 'NESTLEIND.NS', 'BRITANNIA.NS', 'COLPAL.NS', 'HINDUNILVR.NS',
            'MARICO.NS', 'GODREJCP.NS', 'EMAMIPERF.NS', 'HAVELLS.NS', 'KAJARIA.NS',
            'BERGER.NS', 'CERA.NS',
            'ULTRACEMCO.NS', 'SHREECEM.NS', 'AMBUJACEMENT.NS', 'DALMIACEM.NS', 'RAMCOCEM.NS',
            'ACC.NS', 'JKCEMENT.NS', 'HEIDELBERG.NS',
            'LARSENTOUBRO.NS', 'BHARTIARTL.NS', 'JSWSTEEL.NS', 'SAILIND.NS',
            'OBEROIRLTY.NS', 'DLF.NS', 'ITES.NS', 'LODHA.NS', 'SUNTV.NS',
            'TATASTEEL.NS', 'HINDALCO.NS', 'NALCO.NS', 'VEDL.NS', 'JINDALSTEL.NS',
            'MOIL.NS', 'NMDC.NS', 'GPIL.NS',
            'DMART.NS', 'PAGEIND.NS', 'SHOPPER.NS',
            'ONGC.NS', 'BASF.NS', 'PIDILITIND.NS', 'BALRAMCHIN.NS', 'ASTERDM.NS',
            'APOLLOHOSP.NS', 'FORTIS.NS', 'HEALTHCARE.NS',
            'ICICIGI.NS', 'BAJAJINSV.NS', 'CHOLAHLDNG.NS',
            'INFIBEAM.NS', 'PGHH.NS', 'ESCORTS.NS', 'SIEMENS.NS', 'ABB.NS',
            'KALYANKJIL.NS', 'SOBHA.NS', 'MINDAIND.NS', 'BEL.NS', 'HAL.NS',
            'GRAPHITE.NS', 'GICRE.NS', 'EQUITAS.NS', 'ARVINDFARM.NS', 'MAGMA.NS',
            'IRFC.NS', 'COCHINSHIP.NS', 'MAPMYINDIA.NS', 'FSL.NS', 'LAXMIMACH.NS',
        }
        return list(nse_stocks)
    
    def get_top_250_stocks(self):
        """Fetch top 250 stocks by volume"""
        logger.info("Fetching top 250 stocks...")
        stock_list = self.get_nse_stock_list()
        volumes = []
        
        for idx, ticker in enumerate(stock_list, 1):
            try:
                data = yf.download(ticker, period='5d', progress=False)
                if not data.empty:
                    latest_volume = data['Volume'].iloc[-1]
                    latest_price = data['Close'].iloc[-1]
                    volumes.append({
                        'ticker': ticker,
                        'symbol': ticker.replace('.NS', ''),
                        'volume': float(latest_volume),
                        'price': float(latest_price),
                        'date': data.index[-1].strftime('%Y-%m-%d')
                    })
            except:
                pass
            if idx % 10 == 0:
                time.sleep(1)
        
        volumes_df = pd.DataFrame(volumes)
        top_250 = volumes_df.nlargest(250, 'volume')
        logger.info(f"Found {len(top_250)} stocks")
        return top_250
    
    def save_top_stocks(self, df):
        """Save top 250 stocks"""
        top_stocks_dict = {
            'generated_at': datetime.now().isoformat(),
            'total_stocks': len(df),
            'stocks': df.to_dict('records')
        }
        with open(self.top_stocks_file, 'w') as f:
            json.dump(top_stocks_dict, f, indent=2)
        df.to_csv('data/top_250_stocks.csv', index=False)
        logger.info("Saved top 250 stocks")
    
    def load_top_stocks(self):
        """Load existing top 250 stocks"""
        if Path(self.top_stocks_file).exists():
            with open(self.top_stocks_file) as f:
                return json.load(f)
        return None
