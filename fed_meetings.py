# Fed meetings that were "pivots" - major shifts in policy direction
# fed_calendar.py

def get_fed_meeting_dates(year):
    """
    Fed meeting dates from federalreserve.gov/monetarypolicy/fomccalendars.htm
    Update once per year when Fed publishes next year's calendar.
    """
    fed_dates_2023 = [
        '2023-02-01', '2023-03-22', '2023-05-03', '2023-06-14',
        '2023-07-26', '2023-09-20', '2023-11-01', '2023-12-13'
    ]
    
    fed_dates_2024 = [
        '2024-01-31', '2024-03-20', '2024-05-01', '2024-06-12',
        '2024-07-31', '2024-09-18', '2024-11-07', '2024-12-18'
    ]
    
    fed_dates_2025 = [
        '2025-01-29', '2025-03-19', '2025-05-07', '2025-06-18',
        '2025-07-30', '2025-09-17', '2025-10-29', '2025-12-10'
    ]
    
    if year == 2023:
        return fed_dates_2023
    elif year == 2024:
        return fed_dates_2024
    elif year == 2025:
        return fed_dates_2025
    else:
        raise ValueError(f"No Fed dates available for {year}")


def get_all_fed_dates():
    """Get all Fed dates across years for backtesting."""
    return (get_fed_meeting_dates(2023) + 
            get_fed_meeting_dates(2024) + 
            get_fed_meeting_dates(2025))



def is_fed_meeting(input, fed_dates = get_all_fed_dates()):
    """
    Check if a Fed meeting date was a pivot moment.
    Pivot = first cut after hikes, first hike after cuts, major policy signal
    """
    for date in fed_dates:
        if input == date:
            return True
    else:
        return False


# Test it
if __name__ == "__main__":
    print("Testing Fed Pivot Detection:")
    print(f"2024-07-31 (July pivot): {is_fed_meeting('2024-07-31', get_all_fed_dates())}")  # Should be True
    print(f"2024-06-12 (Regular hold): {is_fed_meeting('2024-06-12', get_all_fed_dates())}")  # Should be False
    print(f"2024-09-18 (First cut): {is_fed_meeting('2024-09-18', get_all_fed_dates())}")  # Should be True