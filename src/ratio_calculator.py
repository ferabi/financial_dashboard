# src/ratio_calculator.py
import pandas as pd
import numpy as np
class FinancialRatioCalculator:
    @staticmethod
    def calculate_liquidity_ratios(df_balance, df_income):
        """Calculate current ratio, quick ratio, cash ratio"""
        ratios = {}

        # Current Ratio = Current Assets / Current Liabilities
        current_assets = df_balance.loc['Current Assets'] if 'Current Assets' in df_balance.index else df_balance.loc['Total Current Assets']
        current_liabilities = df_balance.loc['Current Liabilities'] if 'Current Liabilities' in df_balance.index else df_balance.loc['Total Current Liabilities']
        ratios['current_ratio'] = current_assets / current_liabilities

        # Quick Ratio = (Current Assets - Inventory) / Current Liabilities
        inventory = df_balance.loc['Inventory'] if 'Inventory' in df_balance.index else 0
        ratios['quick_ratio'] = (current_assets - inventory) / current_liabilities

        return pd.DataFrame(ratios)
    @staticmethod
    def calculate_profitability_ratios(df_income, df_balance):
        """Calculate ROE, ROA, Gross Margin, Net Margin"""
        ratios = {}

        # ROE = Net Income / Shareholders' Equity
        net_income = df_income.loc['Net Income']
        shareholders_equity = df_balance.loc['Total Stockholders Equity']
        ratios['roe'] = net_income / shareholders_equity

        # ROA = Net Income / Total Assets
        total_assets = df_balance.loc['Total Assets']
        ratios['roa'] = net_income / total_assets

        # Margins
        revenue = df_income.loc['Total Revenue']
        gross_profit = df_income.loc['Gross Profit']
        ratios['gross_margin'] = gross_profit / revenue
        ratios['net_margin'] = net_income / revenue

        # DuPont Analysis
        ratios['asset_turnover'] = revenue / total_assets
        ratios['financial_leverage'] = total_assets / shareholders_equity

        return pd.DataFrame(ratios)
    @staticmethod
    def calculate_solvency_ratios(df_balance, df_income):
        """Calculate Debt-to-Equity, Interest Coverage"""
        ratios = {}

        # Debt to Equity = Total Debt / Total Equity
        total_debt = df_balance.loc['Total Debt'] if 'Total Debt' in df_balance.index else 0
        total_equity = df_balance.loc['Total Stockholders Equity']
        ratios['debt_to_equity'] = total_debt / total_equity

        # Interest Coverage = EBIT / Interest Expense
        ebit = df_income.loc['EBIT'] if 'EBIT' in df_income.index else df_income.loc['Operating Income']
        interest_expense = df_income.loc['Interest Expense']
        ratios['interest_coverage'] = ebit / interest_expense

        return pd.DataFrame(ratios)
    