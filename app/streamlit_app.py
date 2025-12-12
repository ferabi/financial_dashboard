# app/streamlit_app.py
import streamlit as st
import pandas as pd
from src.data_fetcher import FinancialDataFetcher
from src.ratio_calculator import FinancialRatioCalculator
from src.visualizer import FinancialVisualizer
# Page config
st.set_page_config(page_title="Financial Dashboard", layout="wide")
# Sidebar
st.sidebar.title("Financial Dashboard")
ticker = st.sidebar.text_input("Enter Ticker Symbol", "AAPL")
years = st.sidebar.slider("Analysis Period (Years)", 1, 10, 5)
# Initialize
fetcher = FinancialDataFetcher()
calculator = FinancialRatioCalculator()
visualizer = FinancialVisualizer()
# Main content
st.title(f"Financial Analysis: {ticker}")
# Fetch data
with st.spinner(f"Fetching data for {ticker}..."):
    data = fetcher.fetch_yahoo_data(ticker, f"{years}y")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
"Overview", "Ratio Analysis", "Financial Statements", "Trend Analysis"
])
with tab1:
    col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Price", "$150.25", "$1.50")
with col2:
    st.metric("Market Cap", "$2.4T", "2.3%")
with col3:
    st.metric("P/E Ratio", "28.5", "-0.5")

# Price chart
st.subheader("Price History")
st.line_chart(data['prices']['Close'])
with tab2:
# Calculate ratios
    liquidity = calculator.calculate_liquidity_ratios(
        data['balance_sheet'], data['income_stmt'])

# Display in columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Liquidity Ratios")
    st.dataframe(liquidity.T.style.background_gradient(cmap='RdYlGn'))

with col2:
    st.subheader("Ratio Trends")
    fig = visualizer.create_ratio_trend_chart(liquidity, liquidity.columns)
    st.plotly_chart(fig, use_container_width=True)
# Run with: streamlit run app/streamlit_app.py