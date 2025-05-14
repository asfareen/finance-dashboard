import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from sqlalchemy import create_engine
from io import BytesIO
from auth import login

st.set_page_config(layout='wide')
login()
st.title("📈 Enhanced Stock Dashboard")

# Load data
engine = create_engine('sqlite:///stocks.db')
df = pd.read_sql('stock_data', engine)

# Search
search_term = st.text_input("🔍 Search by Name or Ticker")
if search_term:
    df = df[df['Name'].str.contains(search_term, case=False, na=False) | 
            df['Ticker'].str.contains(search_term.upper(), na=False)]

# P/E filter
pe_filter = st.slider("📊 Max P/E Ratio", 0, 100, 100)
df = df[df['P/E Ratio'] <= pe_filter]

# Sector filter
sector_filter = st.multiselect("📂 Filter by Sector", df['Sector'].unique(), default=df['Sector'].unique())
df = df[df['Sector'].isin(sector_filter)]

# Pagination
page_size = 5
page_num = st.number_input("📄 Page number", 1, (len(df) // page_size + 1))
start = (page_num - 1) * page_size
end = start + page_size
df_paginated = df.iloc[start:end]

st.dataframe(df_paginated)

# Download
csv = df.to_csv(index=False).encode('utf-8')
excel_io = BytesIO()
df.to_excel(excel_io, index=False, engine='openpyxl')

st.download_button("📥 Download CSV", csv, "stocks.csv", "text/csv")
st.download_button("📥 Download Excel", excel_io.getvalue(), "stocks.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Bar Charts
st.subheader("P/E Ratio Comparison")
st.plotly_chart(px.bar(df, x='Ticker', y='P/E Ratio', color='Sector'), use_container_width=True)

st.subheader("Dividend Yield Comparison")
st.plotly_chart(px.bar(df, x='Ticker', y='Dividend Yield', color='Sector'), use_container_width=True)

# Historical Chart
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
