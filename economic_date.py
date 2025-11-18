import pandas as pd

def get_cpi_dates(year):
    """
    CPI release dates - usually 2nd week of each month.
    Source: https://www.bls.gov/schedule/news_release/cpi.htm
    """
    cpi_2023 = [
        '2023-01-12', '2023-02-14', '2023-03-14', '2023-04-12',
        '2023-05-10', '2023-06-13', '2023-07-12', '2023-08-10',
        '2023-09-13', '2023-10-12', '2023-11-14', '2023-12-12'
    ]
    
    cpi_2024 = [
        '2024-01-11', '2024-02-13', '2024-03-12', '2024-04-10',
        '2024-05-15', '2024-06-12', '2024-07-11', '2024-08-14',
        '2024-09-11', '2024-10-10', '2024-11-13', '2024-12-11'
    ]
    
    cpi_2025 = [
        '2025-01-15', '2025-02-12', '2025-03-12', '2025-04-10',
        '2025-05-13', '2025-06-11', '2025-07-11', '2025-08-13',
        '2025-09-10', '2025-10-15', '2025-11-12', '2025-12-10'
    ]
    
    if year == 2023:
        return cpi_2023
    elif year == 2024:
        return cpi_2024
    elif year == 2025:
        return cpi_2025
    else:
        return []


def get_nfp_dates(year):
    """
    Non-Farm Payrolls (NFP) - First Friday of every month.
    Source: https://www.bls.gov/schedule/news_release/empsit.htm
    """
    nfp_2023 = [
        '2023-01-06', '2023-02-03', '2023-03-10', '2023-04-07',
        '2023-05-05', '2023-06-02', '2023-07-07', '2023-08-04',
        '2023-09-01', '2023-10-06', '2023-11-03', '2023-12-08'
    ]
    
    nfp_2024 = [
        '2024-01-05', '2024-02-02', '2024-03-08', '2024-04-05',
        '2024-05-03', '2024-06-07', '2024-07-05', '2024-08-02',
        '2024-09-06', '2024-10-04', '2024-11-01', '2024-12-06'
    ]
    
    nfp_2025 = [
        '2025-01-10', '2025-02-07', '2025-03-07', '2025-04-04',
        '2025-05-02', '2025-06-06', '2025-07-03', '2025-08-01',
        '2025-09-05', '2025-10-03', '2025-11-07', '2025-12-05'
    ]
    
    if year == 2023:
        return nfp_2023
    elif year == 2024:
        return nfp_2024
    elif year == 2025:
        return nfp_2025
    else:
        return []


def get_all_cpi_dates():
    """Get all CPI dates across years."""
    return get_cpi_dates(2023) + get_cpi_dates(2024) + get_cpi_dates(2025)


def get_all_nfp_dates():
    """Get all NFP dates across years."""
    return get_nfp_dates(2023) + get_nfp_dates(2024) + get_nfp_dates(2025)


def check_economic_data_nearby(target_date, window_days=5):
    """
    Check if CPI or NFP release is within window of target date.
    Works for ANY date, not just Fed meetings.
    
    Args:
        target_date: Any date to check (string 'YYYY-MM-DD')
        window_days: Days before/after to check (default 5)
    
    Returns:
        Dict with 'cpi', 'nfp', and 'any' booleans
    """
    target_dt = pd.to_datetime(target_date)
    year = target_dt.year
    
    cpi_dates = get_cpi_dates(year)
    nfp_dates = get_nfp_dates(year)
    
    has_cpi = False
    has_nfp = False
    
    # Check CPI
    for cpi_date in cpi_dates:
        cpi_dt = pd.to_datetime(cpi_date)
        days_apart = abs((target_dt - cpi_dt).days)
        
        if days_apart <= window_days:
            print(f"  CPI on {cpi_date} ({days_apart} days away)")
            has_cpi = True
    
    # Check NFP
    for nfp_date in nfp_dates:
        nfp_dt = pd.to_datetime(nfp_date)
        days_apart = abs((target_dt - nfp_dt).days)
        
        if days_apart <= window_days:
            print(f"  NFP on {nfp_date} ({days_apart} days away)")
            has_nfp = True
    
    return {
        'cpi': has_cpi,
        'nfp': has_nfp,
        'any': has_cpi or has_nfp
    }


# Test it
if __name__ == "__main__":
    print("Testing Economic Data Detection:\n")
    
    # Test Fed meeting date
    print("July 31, 2024 (Fed meeting):")
    result = check_economic_data_nearby('2024-07-31')
    print(f"Result: {result}\n")
    
    # Test today's date (your VXX trade)
    print("Nov 17, 2025 (your entry today):")
    result = check_economic_data_nearby('2025-11-17')
    print(f"Result: {result}\n")
    
    # Test random date
    print("June 15, 2024 (random date):")
    result = check_economic_data_nearby('2024-06-15')
    print(f"Result: {result}")