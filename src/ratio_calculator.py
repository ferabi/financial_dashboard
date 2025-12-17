# src/ratio_calculator.py
import pandas as pd
import numpy as np
class FinancialRatioCalculator:
    def _get_financial_value(self, df, keys):
        for key in keys:
            if key in df.index:
                return df.loc[key]
        return np.nan

    def _calculate_ratio(self, numerator, denominator):
        """Safely calculate the ratio of two numbers or two pandas Series."""
        if isinstance(denominator, pd.Series):
            # Replace 0 with NaN to avoid division by zero issues
            denominator = denominator.replace(0, np.nan)
        elif denominator == 0:
            return np.nan

        return numerator / denominator

    def calculate_liquidity_ratios(self, df_balance, df_income):
        """Calculate current ratio, quick ratio, cash ratio"""
        ratios = {}

        # Current Ratio
        current_assets = self._get_financial_value(df_balance, ['Current Assets', 'Total Current Assets'])
        current_liabilities = self._get_financial_value(df_balance, ['Current Liabilities', 'Total Current Liabilities'])
        ratios['current_ratio'] = self._calculate_ratio(current_assets, current_liabilities)

        # Quick Ratio
        inventory = self._get_financial_value(df_balance, ['Inventory'])
        if isinstance(inventory, pd.Series):
            inventory = inventory.fillna(0)
        elif pd.isna(inventory):
            inventory = 0
        ratios['quick_ratio'] = self._calculate_ratio(current_assets - inventory, current_liabilities)

        # Cash Ratio
        cash = self._get_financial_value(df_balance, ['Cash', 'Cash And Cash Equivalents'])
        ratios['cash_ratio'] = self._calculate_ratio(cash, current_liabilities)

        return pd.DataFrame(ratios)

    def calculate_profitability_ratios(self, df_income, df_balance):
        """Calculate ROE, ROA, Gross Margin, Net Margin"""
        ratios = {}

        net_income = self._get_financial_value(df_income, ['Net Income'])
        shareholders_equity = self._get_financial_value(df_balance, ['Total Stockholders Equity'])
        total_assets = self._get_financial_value(df_balance, ['Total Assets'])
        revenue = self._get_financial_value(df_income, ['Total Revenue'])
        gross_profit = self._get_financial_value(df_income, ['Gross Profit'])

        ratios['roe'] = self._calculate_ratio(net_income, shareholders_equity)
        ratios['roa'] = self._calculate_ratio(net_income, total_assets)
        ratios['gross_margin'] = self._calculate_ratio(gross_profit, revenue)
        ratios['net_margin'] = self._calculate_ratio(net_income, revenue)
        ratios['asset_turnover'] = self._calculate_ratio(revenue, total_assets)
        ratios['financial_leverage'] = self._calculate_ratio(total_assets, shareholders_equity)

        return pd.DataFrame(ratios)

    def calculate_solvency_ratios(self, df_balance, df_income):
        """Calculate Debt-to-Equity, Interest Coverage"""
        ratios = {}

        total_debt = self._get_financial_value(df_balance, ['Total Debt'])
        if isinstance(total_debt, pd.Series):
            total_debt = total_debt.fillna(0)
        elif pd.isna(total_debt):
            total_debt = 0
        total_equity = self._get_financial_value(df_balance, ['Total Stockholders Equity'])
        ebit = self._get_financial_value(df_income, ['EBIT', 'Operating Income'])
        interest_expense = self._get_financial_value(df_income, ['Interest Expense'])

        ratios['debt_to_equity'] = self._calculate_ratio(total_debt, total_equity)
        ratios['interest_coverage'] = self._calculate_ratio(ebit, interest_expense)

        return pd.DataFrame(ratios)