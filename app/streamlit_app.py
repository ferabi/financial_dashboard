# app/streamlit_app.py
import streamlit as st
import pandas as pd
from src.data_fetcher import fetch_yahoo_data, get_stock_info
from src.ratio_calculator import FinancialRatioCalculator
from src.visualizer import FinancialVisualizer


def display_ratio_dataframes(title, df):
    st.subheader(title)
    if not df.empty:
        st.dataframe(df.T.style.background_gradient(cmap='RdYlGn'))
    else:
        st.write("No data to display")

def display_ratio_trend_chart(title, df):
    st.write(f"### {title}")
    if not df.empty:
        fig = visualizer.create_ratio_trend_chart(df, df.columns.tolist())
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data to display")

# Page config
st.set_page_config(page_title="Financial Dashboard", layout="wide")
# Sidebar
st.sidebar.title("Financial Dashboard")
ticker = st.sidebar.text_input("Enter Ticker Symbol", "AAPL")
years = st.sidebar.slider("Analysis Period (Years)", 1, 10, 5)
# Initialize
calculator = FinancialRatioCalculator()
visualizer = FinancialVisualizer()
# Main content
st.title(f"Financial Analysis: {ticker}")

# Fetch data
with st.spinner(f"Fetching data for {ticker}..."):
    data = fetch_yahoo_data(ticker, f"{years}y")
    info = get_stock_info(ticker)

if not data or not info:
    st.error(f"Could not fetch data for {ticker}. Please try another ticker.")
    st.stop()

# Calculate ratios
liquidity = calculator.calculate_liquidity_ratios(
    data['balance_sheet'], data['income_stmt'])
profitability = calculator.calculate_profitability_ratios(
    data['income_stmt'], data['balance_sheet'])
solvency = calculator.calculate_solvency_ratios(
    data['balance_sheet'], data['income_stmt'])

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview", "Ratio Analysis", "Financial Statements", "Trend Analysis"
])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        price = info.get('currentPrice', 'N/A')
        price_change = info.get('regularMarketChange', 0)
        st.metric("Current Price", f"${price}", f"{price_change:.2f}")
    with col2:
        market_cap = info.get('marketCap', 'N/A')
        st.metric("Market Cap", f"${market_cap:,}", "")
    with col3:
        pe_ratio = info.get('trailingPE', 'N/A')
        st.metric("P/E Ratio", pe_ratio, "")

    # Price chart
    st.subheader("Price History")
    st.line_chart(data['prices']['Close'])

with tab2:
    if liquidity.empty and profitability.empty and solvency.empty:
        st.write("No data to display")
    else:
        # Display in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            display_ratio_dataframes("Liquidity Ratios", liquidity)
        with col2:
            display_ratio_dataframes("Profitability Ratios", profitability)
        with col3:
            display_ratio_dataframes("Solvency Ratios", solvency)

with tab3:
    st.subheader("Financial Statements")

    with st.expander("Income Statement"):
        st.dataframe(data['income_stmt'])
    with st.expander("Balance Sheet"):
        st.dataframe(data['balance_sheet'])
    with st.expander("Cash Flow"):
        st.dataframe(data['cash_flow'])

    st.subheader("Income Statement Waterfall")
    latest_year = data['income_stmt'].columns[0]
    fig = visualizer.create_financial_statement_waterfall(data['income_stmt'], latest_year)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Ratio Trends")
    display_ratio_trend_chart("Liquidity Ratio Trends", liquidity)
    display_ratio_trend_chart("Profitability Ratio Trends", profitability)
    display_ratio_trend_chart("Solvency Ratio Trends", solvency)