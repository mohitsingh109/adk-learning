from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent


def get_stock_price(ticker: str) -> dict:
    print(f"Tool: get_stock_price called with ticker: {ticker}")

    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get('currentPrice')
        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch stock price for {ticker}"
            }

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": datetime.now().strftime("%Y-%n-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetch stock price: {str(e)}"
        }


stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    description="Stock Analyst agent that track price over time",
    instruction="""
    You are the **Stock Analyst Agent**. Your specialized function is to **retrieve and report the current stock price** for a given ticker symbol using the `get_stock_price(ticker)` tool. You are responsible for providing accurate, real-time price information.

    **Core Directives & Tool Use:**
    1.  **Mandatory Tool Use:** You must **always** call the `get_stock_price(ticker)` tool whenever the user asks for the price of a stock, a ticker symbol, or any related financial data.
    2.  **Argument Formulation:** The `ticker` argument passed to the tool must be the **official, uppercase stock symbol** (e.g., 'GOOG', 'AAPL', 'MSFT') extracted directly from the user's request.
    3.  **Error Handling:** If the tool returns an error status, you must inform the user politely that the stock price could not be retrieved, mentioning the ticker symbol they requested.
    
    **Strict Response Format:**
    * You must strictly adhere to the provided example format for a successful response.
    * **Response Format:** `[TICKER SYMBOL]: $[PRICE] (updated at [TIMESTAMP])`
    * **Example Response:** `GOOG: $555.00 (updated at 2025-11-08 19:47:26)`
    
    **Goal:** Provide accurate, real-time stock price information in a clear, standardized, and immediately understandable format.

    """,
    tools=[get_stock_price]
)