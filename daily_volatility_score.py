from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from entry_score import calculate_entry_score
from fed_meetings import get_all_fed_dates
from earnings import get_earnings_dates
from economic_date import get_all_cpi_dates, get_all_nfp_dates

def get_volatility_outlook(target_date=None):
    """Get volatility score for any date."""
    if target_date is None:
        target_date = datetime.now()
    
    if isinstance(target_date, str):
        target_date = pd.to_datetime(target_date)
    
    target_str = target_date.strftime('%Y-%m-%d')
    
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        score_result = calculate_entry_score(target_str)
        sys.stdout = old_stdout
    except:
        sys.stdout = old_stdout
        score_result = {
            'score': 0,
            'conviction': 'NONE',
            'breakdown': {
                'fed_meeting': False,
                'vix_low': False,
                'earnings': False,
                'economic_data': False
            }
        }
    
    return score_result


def print_market_volatility_report():
    """Print a clean volatility report for all types of traders."""
    
    today = datetime.now()
    
    # Get current VIX
    vix = yf.download('^VIX', period='5d', progress=False)
    if isinstance(vix.columns, pd.MultiIndex):
        vix_close = vix['Close']['^VIX']
    else:
        vix_close = vix['Close']
    current_vix = vix_close.iloc[-1]
    
    # Get score
    score_result = get_volatility_outlook()
    score = score_result['score']
    breakdown = score_result['breakdown']
    
    # Header
    print("\n" + "="*70)
    print(f"📊 MARKET VOLATILITY REPORT - {today.strftime('%A, %B %d, %Y')}")
    print("="*70)
    
    # VIX Level
    print(f"\n📈 CURRENT VIX LEVEL: {current_vix:.2f}")
    
    if current_vix < 15:
        vix_desc = "Very Low (Market calm)"
    elif current_vix < 20:
        vix_desc = "Low to Moderate"
    elif current_vix < 30:
        vix_desc = "Elevated (Caution advised)"
    else:
        vix_desc = "High (Market stress)"
    
    print(f"   Status: {vix_desc}")
    
    # Volatility Score
    print(f"\n🎯 VOLATILITY CATALYST SCORE: {score}/9")
    
    if score >= 7:
        risk_level = "⚠️  HIGH RISK"
        description = "Multiple catalysts present - expect significant market swings"
        trader_advice = "Consider tighter stops, reduce position sizes, or wait for clarity"
    elif score >= 4:
        risk_level = "⚠️  MODERATE RISK"
        description = "Some catalysts present - potential for increased volatility"
        trader_advice = "Stay alert, monitor positions closely"
    else:
        risk_level = "✅ LOW RISK"
        description = "Few catalysts - relatively calm market expected"
        trader_advice = "Normal trading conditions"
    
    print(f"   Risk Level: {risk_level}")
    print(f"   Outlook: {description}")
    
    # What's driving volatility
    print(f"\n📋 CATALYSTS TODAY:")
    
    catalysts_present = []
    
    if breakdown['fed_meeting']:
        catalysts_present.append("🏛️  Federal Reserve Meeting")
        print(f"   🏛️  Federal Reserve Meeting - Policy decision expected")
    
    if breakdown['earnings']:
        catalysts_present.append("📊 Major Tech Earnings")
        print(f"   📊 Major Tech Earnings - FAANG companies reporting")
    
    if breakdown['economic_data']:
        catalysts_present.append("📈 Economic Data Release")
        print(f"   📈 Economic Data Release - CPI, Jobs Report, or similar")
    
    if breakdown['vix_low']:
        print(f"   💤 VIX Below 18 - Low volatility environment (may snap back)")
    
    if len(catalysts_present) == 0:
        print(f"   ✅ No major catalysts - Typical trading day expected")
    
    # Trader-specific guidance
    print(f"\n💡 GUIDANCE FOR TRADERS:")
    print(f"   {trader_advice}")
    
    if score >= 7:
        print(f"\n⚠️  HEIGHTENED VOLATILITY WARNING:")
        print(f"   • Expect larger-than-normal price swings")
        print(f"   • Option premiums likely elevated")
        print(f"   • Consider waiting for post-catalyst clarity")
        print(f"   • If holding positions, set protective stops")
    
    elif score >= 4:
        print(f"\n⚠️  VOLATILITY WATCH:")
        print(f"   • Some market-moving events today")
        print(f"   • Monitor news and announcements closely")
        print(f"   • Be prepared for intraday swings")
    
    # Next high-risk period
    print(f"\n🔮 LOOKING AHEAD:")
    
    # Find next high-score day in next 30 days
    found_high_score = False
    for i in range(1, 31):
        check_date = today + timedelta(days=i)
        
        if check_date.weekday() >= 5:
            continue
        
        future_score = get_volatility_outlook(check_date)
        
        if future_score['score'] >= 7:
            days_away = i
            print(f"   ⚠️  High volatility expected on {check_date.strftime('%B %d')} ({days_away} days)")
            print(f"      Score: {future_score['score']}/9")
            found_high_score = True
            break
    
    if not found_high_score:
        # Check next Fed meeting
        fed_dates = get_all_fed_dates()
        next_fed = None
        for fed_date in sorted(fed_dates):
            if pd.to_datetime(fed_date) > today:
                next_fed = fed_date
                break
        
        if next_fed:
            fed_dt = pd.to_datetime(next_fed)
            days_until = (fed_dt - today).days
            
            if days_until <= 30:
                print(f"   📅 Next Fed meeting: {fed_dt.strftime('%B %d')} ({days_until} days)")
                print(f"      Potential for increased volatility around this date")
            else:
                print(f"   ✅ No major volatility events in next 30 days")
        else:
            print(f"   ✅ No major volatility events in next 30 days")
    
    print("\n" + "="*70)
    print("💬 This report updates daily. Run again tomorrow for latest outlook.")
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Check specific date
        target_date = sys.argv[1]
        print(f"\nGenerating report for {target_date}...\n")
        
        score_result = get_volatility_outlook(target_date)
        score = score_result['score']
        
        print(f"Volatility Score: {score}/9")
        
        if score >= 7:
            print("⚠️  HIGH VOLATILITY expected - Multiple catalysts present")
        elif score >= 4:
            print("⚠️  MODERATE VOLATILITY - Some catalysts present")
        else:
            print("✅ LOW VOLATILITY - Normal trading conditions")
    else:
        # Today's report
        print_market_volatility_report()