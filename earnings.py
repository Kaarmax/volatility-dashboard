import yfinance as yf
import pandas as pd

def get_earnings_dates(ticker, start_date='2023-01-01', end_date='2025-12-31'):
    """
    Get earnings dates for a ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        # Get earnings calendar
        earnings_dates = stock.earnings_dates
        
        if earnings_dates is not None and not earnings_dates.empty:
            # Filter by date range and extract dates
            earnings_dates = earnings_dates.index.tolist()
            earnings_dates = [d.strftime('%Y-%m-%d') for d in earnings_dates 
                            if start_date <= d.strftime('%Y-%m-%d') <= end_date]
            return earnings_dates
        return []
    except:
        return []


def check_earnings_overlap(fed_date, tickers=['AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'NVDA'], window_days=5):
    """
    Auto-check earnings overlap by pulling live data from yfinance.
    """
    fed_dt = pd.to_datetime(fed_date)
    L = []
    for ticker in tickers:
        earnings_dates = get_earnings_dates(ticker)
        
        for earnings_date in earnings_dates:
            earnings_dt = pd.to_datetime(earnings_date)
            days_apart = abs((fed_dt - earnings_dt).days)
            
            if days_apart <= window_days:
                print(f"  Found: {ticker} earnings on {earnings_date} ({days_apart} days from Fed)")
                L += [ticker]
    if len(L) > 0:
        print(*L)
        return True
    else:
        return False


# Test it
if __name__ == "__main__":
    print("Testing Auto Earnings Detection:\n")
    
    print("Oct 29, 2025 Fed meeting:")
    result = check_earnings_overlap('2025-10-29')
    print(f"Overlap? {result}\n")