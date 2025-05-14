import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from sqlalchemy import create_engine
from io import BytesIO
from auth import login  # Ensure this is correct
from predict_utils import predict_stock

st.set_page_config(
    page_title="📊 StockX Dashboard",
    page_icon="📈",
    layout="wide",  # Makes it full-width for dashboard
)

if not login():
    st.stop()

# Load the data from the database
engine = create_engine('sqlite:///stocks.db')
df = pd.read_sql('stock_data', engine)

# Make sure df is loaded properly before accessing it
if df.empty:
    st.error("Stock data is not available. Please check the database.")
    st.stop()

# UI components
st.title("📈 Enhanced Stock Dashboard")

# Add Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Forecast", "📥 Downloads"])

with tab1:
    st.subheader("P/E Ratio Comparison")
    st.plotly_chart(px.bar(df, x='Ticker', y='P/E Ratio', color='Sector'), use_container_width=True)

    st.subheader("Dividend Yield Comparison")
    st.plotly_chart(px.bar(df, x='Ticker', y='Dividend Yield', color='Sector'), use_container_width=True)

    st.subheader("📉 Historical Price Chart")
    selected_stock = st.selectbox("Choose stock", df['Ticker'].unique())
    hist = yf.Ticker(selected_stock).history(period="6mo")
    fig = go.Figure(data=[go.Candlestick(
        x=hist.index,
        open=hist['Open'], high=hist['High'],
        low=hist['Low'], close=hist['Close']
    )])
    fig.update_layout(title=f"{selected_stock} - Last 6 Months", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🔮 Stock Price Forecast")

    selected = st.selectbox("Select a stock for forecast", df['Ticker'].unique())
    forecast_days = st.slider("Days to forecast", 7, 60, 30)

    with st.spinner("Predicting future stock prices..."):
        forecast_df = predict_stock(selected, forecast_days)

    if forecast_df.empty:
        st.error("Prediction failed. Please try another stock.")
    else:
        st.line_chart(forecast_df.set_index("Date"))
        st.dataframe(forecast_df)

with tab3:
    csv = df.to_csv(index=False).encode('utf-8')
    excel_io = BytesIO()
    df.to_excel(excel_io, index=False, engine='openpyxl')

    st.download_button("📥 Download CSV", csv, "stocks.csv", "text/csv")
    st.download_button("📥 Download Excel", excel_io.getvalue(), "stocks.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

