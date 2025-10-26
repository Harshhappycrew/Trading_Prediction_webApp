"""
Stock Data Collection Module
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
import ta

class DataCollector:
    """Collect and process stock market data"""
    
    def __init__(self, symbols: list = None):
        # Default Indian stocks from NSE
        self.symbols = symbols or [
            # Nifty 50 Top Stocks
            "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
            "BHARTIARTL", "SBIN", "HINDUNILVR", "ITC", "LT",
            "BAJFINANCE", "KOTAKBANK", "HCLTECH", "AXISBANK",
            "MARUTI", "SUNPHARMA", "TITAN", "ULTRACEMCO",
            "ASIANPAINT", "WIPRO"
        ]
    
    def fetch_historical_data(self, symbol: str, period: str = "2y"):
        """Fetch historical data from yfinance for NSE stocks"""
        try:
            logger.info(f"Fetching data for {symbol} from NSE...")
            
            # Add .NS suffix for NSE (National Stock Exchange)
            nse_symbol = f"{symbol}.NS"
            ticker = yf.Ticker(nse_symbol)
            df = ticker.history(period=period)
            
            if df.empty:
                logger.warning(f"No data retrieved for {symbol}")
                return None
            
            # yfinance returns NSE prices in INR by default
            # Add technical indicators
            df = self.add_technical_indicators(df)
            
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def add_technical_indicators(self, df: pd.DataFrame):
        """Add technical indicators to dataframe"""
        try:
            # RSI
            df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
            
            # MACD
            macd = ta.trend.MACD(df['Close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['Close'])
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_middle'] = bb.bollinger_mavg()
            df['bb_lower'] = bb.bollinger_lband()
            
            # Moving Averages
            df['sma_20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
            df['sma_50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
            
            # Fill NaN values
            df = df.fillna(method='bfill').fillna(method='ffill')
            
            return df
        
        except Exception as e:
            logger.error(f"Error adding technical indicators: {e}")
            return df
    
    def fetch_all_symbols(self):
        """Fetch data for all configured symbols"""
        data = {}
        for symbol in self.symbols:
            df = self.fetch_historical_data(symbol)
            if df is not None:
                data[symbol] = df
        return data
    
    def save_to_csv(self, df: pd.DataFrame, symbol: str, path: str = "data/raw"):
        """Save dataframe to CSV"""
        try:
            import os
            os.makedirs(path, exist_ok=True)
            
            filename = f"{path}/{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename)
            logger.info(f"Data saved to {filename}")
        
        except Exception as e:
            logger.error(f"Error saving data: {e}")
