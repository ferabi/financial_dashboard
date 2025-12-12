# src/data_fetcher.py
import yfinance as yf
import pandas as pd
from sec_api import QueryApi
import requests
class FinancialDataFetcher:
    def __init__(self):
        self.api_keys = {'sec-api.io':"Add your OWN"} # Store API keys securely

    def fetch_yahoo_data(self, ticker, period="5y"):
        """Fetch price data and basic info from Yahoo Finance"""
        stock = yf.Ticker(ticker)
        # Get historical prices
        hist = stock.history(period=period)
        # Get financial statements
        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow
        return {
        'prices': hist,
        'income_stmt': income_stmt,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow
        }
    
    def fetch_sec_data(self, ticker):
        """Fetch official SEC filings for accurate data"""
        # Using SEC API (requires key)
        queryApi = QueryApi(api_key=self.api_keys['sec-api.io'])
        query = {
        "query": {
        "query_string": {
        "query": f"ticker:{ticker} AND formType:\"10-K\""
        }
        },
        "from": "0",
        "size": "5",
        "sort": [{"filedAt": {"order": "desc"}}]
        }
        return queryApi.get_filings(query)