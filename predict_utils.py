# predict_utils.py
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def predict_stock(ticker='AAPL', forecast_days=30):
    # Download historical data
    data = yf.download(ticker, start='2015-01-01', end='2024-12-31')
    if data.empty or 'Close' not in data.columns:
        return pd.DataFrame()  # Return empty df if failed

    # Prepare dataset
    data = data[['Close']].dropna()
    data['Prediction'] = data['Close'].shift(-forecast_days)

    # Features and labels
    X = np.array(data.drop(['Prediction'], axis=1))[:-forecast_days]
    y = np.array(data['Prediction'])[:-forecast_days]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Forecast
    X_future = np.array(data.drop(['Prediction'], axis=1)[-forecast_days:])
    forecast = model.predict(X_future)

    # Create future date index
    last_date = data.index[-1]
    forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq='B')

    # Return forecast dataframe
    forecast_df = pd.DataFrame({'Date': forecast_index, 'Forecast': forecast})
    return forecast_df
