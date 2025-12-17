# src/visualizer.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
class FinancialVisualizer:
    def create_ratio_trend_chart(self, ratios_df, ratio_names):
        """Create multi-line chart for ratio trends"""
        if ratios_df.empty:
            return go.Figure()
        rows = (len(ratio_names) + 1) // 2
        fig = make_subplots(
            rows=rows,
            cols=2,
            subplot_titles=ratio_names
        )

        for i, ratio in enumerate(ratio_names):
            row = (i // 2) + 1
            col = (i % 2) + 1
            fig.add_trace(
                go.Scatter(x=ratios_df.index, y=ratios_df[ratio], name=ratio),
                row=row, col=col
            )

        fig.update_layout(height=300 * rows, title_text="Financial Ratio Trends")
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