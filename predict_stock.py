import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def predict_stock(ticker='AAPL', forecast_days=30):
data = yf.download(ticker, start='2015-01-01', end='2024-12-31')
data = data[['Close']].dropna()

kotlin
Copy
Edit
data['Prediction'] = data[['Close']].shift(-forecast_days)
X = np.array(data.drop(['Prediction'], axis=1))[:-forecast_days]
y = np.array(data['Prediction'])[:-forecast_days]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

X_future = data.drop(['Prediction'], axis=1)[-forecast_days:]
forecast = model.predict(X_future)

return data, forecast