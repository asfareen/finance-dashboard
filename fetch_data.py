import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

def fetch_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data.append({
            'Ticker': ticker,
            'Name': info.get('shortName', ''),
            'Sector': info.get('sector', 'Unknown'),
            'Industry': info.get('industry', 'Unknown'),
            'Market Cap': info.get('marketCap', 0),
            'P/E Ratio': info.get('trailingPE', 0),
            'Dividend Yield': info.get('dividendYield', 0)
        })
    return pd.DataFrame(data)

df = fetch_data(tickers)

engine = create_engine('sqlite:///stocks.db')
df.to_sql('stock_data', con=engine, if_exists='replace', index=False)
