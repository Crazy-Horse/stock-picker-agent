import yfinance as yf
from crewai.tools import tool

@tool("get_fundamentals")
def get_fundamentals(ticker: str):
    """
    Fetch fundamental financial metrics for a given stock ticker.
    Returns growth rates, margins, FCF, and leverage ratios.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    
    metrics = {
        "revenue_growth": info.get("revenueGrowth"),
        "ebitda_margins": info.get("ebitdaMargins"),
        "free_cash_flow": info.get("freeCashflow"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_equity": info.get("returnOnEquity"),
        "trailing_pe": info.get("trailingPE")
    }
    return metrics