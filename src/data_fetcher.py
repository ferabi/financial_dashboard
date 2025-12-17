# src/data_fetcher.py
import yfinance as yf
import pandas as pd
import json
import os
import pathlib
from datetime import datetime, timedelta

CACHE_DIR = pathlib.Path('data')
CACHE_TTL = timedelta(hours=24)

# Ensure the cache directory exists
CACHE_DIR.mkdir(exist_ok=True)

def _is_cache_valid(cache_path):
    """Check if a cache file is valid (exists and is not too old)."""
    if not cache_path.exists():
        return False
    
    file_mod_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
    return (datetime.now() - file_mod_time) < CACHE_TTL

def get_stock_info(ticker):
    """Fetch stock info from Yahoo Finance, with file-based caching."""
    cache_path = CACHE_DIR / f"{ticker}_info.json"

    if _is_cache_valid(cache_path):
        with open(cache_path, 'r') as f:
            return json.load(f)

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        with open(cache_path, 'w') as f:
            json.dump(info, f)
        return info
    except Exception:
        return None

def fetch_yahoo_data(ticker, period="5y"):
    """Fetch price data and financial statements from Yahoo Finance, with file-based caching."""
    data_dir = CACHE_DIR / f"{ticker}_{period}"
    data_dir.mkdir(exist_ok=True)
    
    prices_path = data_dir / "prices.parquet"
    income_stmt_path = data_dir / "income_stmt.parquet"
    balance_sheet_path = data_dir / "balance_sheet.parquet"
    cash_flow_path = data_dir / "cash_flow.parquet"

    # Check if all parts of the data are cached and valid
    all_cached = all(_is_cache_valid(p) for p in [prices_path, income_stmt_path, balance_sheet_path, cash_flow_path])

    if all_cached:
        return {
            'prices': pd.read_parquet(prices_path),
            'income_stmt': pd.read_parquet(income_stmt_path),
            'balance_sheet': pd.read_parquet(balance_sheet_path),
            'cash_flow': pd.read_parquet(cash_flow_path)
        }

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow

        # Save to cache
        hist.to_parquet(prices_path)
        income_stmt.to_parquet(income_stmt_path)
        balance_sheet.to_parquet(balance_sheet_path)
        cash_flow.to_parquet(cash_flow_path)

        return {
            'prices': hist,
            'income_stmt': income_stmt,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow
        }
    except Exception:
        return None