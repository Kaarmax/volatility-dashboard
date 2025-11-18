import yfinance as yf
import pandas as pd

vix = yf.download('^VIX', period='2y')

def is_vix_below_18(date, vix_data):
    date = pd.to_datetime(date)
    
    # Handle both single and multi-index columns
    if isinstance(vix_data.columns, pd.MultiIndex):
        close_prices = vix_data['Close']['^VIX']
    else:
        close_prices = vix_data['Close']
    
    close_price = close_prices.asof(date)
    
    return close_price < 18

# Test it
test_date = '2024-10-17'
result = is_vix_below_18(test_date, vix)
print(f"VIX below 18 on {test_date}? {result}")

# Also print the actual VIX value
if isinstance(vix.columns, pd.MultiIndex):
    vix_value = vix['Close']['^VIX'].asof(pd.to_datetime(test_date))
else:
    vix_value = vix['Close'].asof(pd.to_datetime(test_date))
    
print(f"Actual VIX value: {vix_value:.2f}")