from below18 import is_vix_below_18, vix
from fed_meetings import get_all_fed_dates
from earnings import check_earnings_overlap
from economic_date import check_economic_data_nearby
import pandas as pd


def calculate_entry_score(target_date):
    """
    Calculate volatility catalyst score for any date.
    
    Scoring:
    - Fed meeting: +2 points (scheduled uncertainty)
    - VIX below 18: +2 points (complacency = bigger moves)
    - Big tech earnings overlap: +3 points (multiple catalysts)
    - Economic data nearby: +2 points (CPI/NFP uncertainty)
    
    Total possible: 9 points
    
    Conviction levels:
    - HIGH: 7-9 points
    - MEDIUM: 4-6 points
    - LOW: 0-3 points
    
    Returns:
        Dict with score and breakdown
    """
    score = 0
    breakdown = {}
    
    print(f"\n{'='*50}")
    print(f"Entry Score for {target_date}")
    print(f"{'='*50}")
    
    # Check 1: Is it a Fed meeting?
    fed_dates = get_all_fed_dates()
    is_fed_meeting = target_date in fed_dates
    if is_fed_meeting:
        score += 2
        print("✓ Fed meeting date: +2 points")
    else:
        print("✗ Not a Fed meeting: 0 points")
    breakdown['fed_meeting'] = is_fed_meeting
    
    # Check 2: VIX level
    vix_check = is_vix_below_18(target_date, vix)
    if vix_check:
        score += 2
        print("✓ VIX below 18: +2 points")
    else:
        print("✗ VIX NOT below 18: 0 points")
    breakdown['vix_low'] = vix_check
    
    # Check 3: Earnings overlap
    print("\nChecking earnings overlap:")
    earnings_check = check_earnings_overlap(target_date, window_days=5)
    if earnings_check:
        score += 3
        print("✓ Big tech earnings nearby: +3 points")
    else:
        print("✗ No earnings overlap: 0 points")
    breakdown['earnings'] = earnings_check
    
    # Check 4: Economic data
    print("\nChecking economic data:")
    econ_data = check_economic_data_nearby(target_date, window_days=5)
    if econ_data['any']:
        score += 2
        print("✓ Economic data nearby: +2 points")
    else:
        print("✗ No economic data: 0 points")
    breakdown['economic_data'] = econ_data['any']
    
    print(f"\n{'='*50}")
    print(f"TOTAL SCORE: {score}/9")
    print(f"{'='*50}\n")
    
    # Determine conviction level
    if score >= 7:
        conviction = "HIGH"
    elif score >= 4:
        conviction = "MEDIUM"
    else:
        conviction = "LOW"
    
    print(f"Conviction Level: {conviction}\n")
    
    return {
        'date': target_date,
        'score': score,
        'conviction': conviction,
        'breakdown': breakdown
    }


# Test it
if __name__ == "__main__":
    print("="*60)
    print("TESTING ENTRY SCORING SYSTEM")
    print("="*60)
    
    # Test 1: July 31, 2024 - your best backtest trade (+33.99%)
    print("\n\nTEST 1: July 31, 2024 (Best backtest trade)")
    result1 = calculate_entry_score('2024-07-31')
    
    # Test 2: Today's 50% winner
    print("\n\nTEST 2: Nov 17, 2025 (Today's 50% win)")
    result2 = calculate_entry_score('2025-11-17')
    
    # Test 3: Nov 7, 2024 - Fed meeting that lost (-17.81%)
    print("\n\nTEST 3: Nov 7, 2024 (Fed meeting - lost 17.81%)")
    result3 = calculate_entry_score('2024-11-07')
    
    # Summary
    print("\n\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"July 31, 2024: {result1['score']}/9 - {result1['conviction']}")
    print(f"Nov 17, 2025: {result2['score']}/9 - {result2['conviction']}")
    print(f"Nov 7, 2024: {result3['score']}/9 - {result3['conviction']}")