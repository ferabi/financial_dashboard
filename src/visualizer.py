# src/visualizer.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
class FinancialVisualizer:
    @staticmethod
    def create_ratio_trend_chart(ratios_df, ratio_names):
        """Create multi-line chart for ratio trends"""
        fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Liquidity Ratios", "Profitability Ratios", 
        "Solvency Ratios", "Efficiency Ratios")
        )

        # Add traces for each ratio category
        colors = px.colors.qualitative.Set3

        for i, ratio in enumerate(ratio_names[:4]):
            fig.add_trace(
            go.Scatter(x=ratios_df.index, y=ratios_df[ratio],
            name=ratio, line=dict(color=colors[i])),
            row=1, col=1 if i < 2 else 2
            )

        fig.update_layout(height=600, title_text="Financial Ratio Trends")
        return fig

    @staticmethod
    def create_financial_statement_waterfall(df_income, year):
        """Create waterfall chart for income statement"""
        fig = go.Figure(go.Waterfall(
        name="Income Statement",
        orientation="v",
        measure=["relative"] * (len(df_income) - 1) + ["total"],
        x=df_income.index,
        y=df_income[year],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))

        fig.update_layout(title=f"Income Statement {year}")
        return fig