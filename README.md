# Financial Dashboard

A web-based financial dashboard that provides a comprehensive overview of a company's financial health. Users can enter a stock ticker to view key financial metrics, analyze trends in financial ratios, and inspect financial statements. The application is built with Python and Streamlit, and it fetches data from the Yahoo Finance API.

## Features

*   **Company Overview:** Displays key information about the company, including current stock price, market capitalization, and P/E ratio.
*   **Price History:** An interactive chart showing the historical stock price.
*   **Ratio Analysis:** Calculates and displays key financial ratios, categorized into:
    *   **Liquidity Ratios:** Current Ratio, Quick Ratio, Cash Ratio.
    *   **Profitability Ratios:** Return on Equity (ROE), Return on Assets (ROA), Gross Margin, Net Margin, Asset Turnover, Financial Leverage.
    *   **Solvency Ratios:** Debt-to-Equity, Interest Coverage.
*   **Financial Statements:** Displays the company's Income Statement, Balance Sheet, and Cash Flow statement.
*   **Trend Analysis:** Visualizes the trends of financial ratios over time.
*   **File-Based Caching:** Implements a file-based caching mechanism to improve performance and allow for offline use of cached data.

## Project Structure

```
.
├── app/
│   └── streamlit_app.py    # Main Streamlit application
├── data/                   # Directory for cached data
├── src/
│   ├── data_fetcher.py     # Fetches data from Yahoo Finance
│   ├── ratio_calculator.py # Calculates financial ratios
│   └── visualizer.py       # Creates visualizations
├── requirements.txt        # Project dependencies
└── README.md
```

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd financial_dashboard
    ```
3.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

```bash
streamlit run app/streamlit_app.py
```

## Caching

This application uses a file-based caching system to store data fetched from the Yahoo Finance API. The cached data is stored in the `data/` directory. This has the following benefits:

*   **Improved Performance:** Reduces the number of API calls, making the application faster on subsequent loads for the same ticker.
*   **Offline Access:** Allows the application to be used without an internet connection if the data has been previously cached.

The cache is invalidated every 24 hours.

## Dependencies

*   `streamlit`
*   `yfinance`
*   `pandas`
*   `plotly`
*   `fastparquet`
