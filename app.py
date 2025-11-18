from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from entry_score import calculate_entry_score
from fed_meetings import get_all_fed_dates

app = Flask(__name__)

def get_volatility_data():
    """Get today's volatility score and info."""
    today = datetime.now()
    
    # Get VIX
    vix = yf.download('^VIX', period='5d', progress=False)
    if isinstance(vix.columns, pd.MultiIndex):
        vix_close = vix['Close']['^VIX']
    else:
        vix_close = vix['Close']
    current_vix = float(vix_close.iloc[-1])
    
    # Get score
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        score_result = calculate_entry_score(today.strftime('%Y-%m-%d'))
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
    
    score = score_result['score']
    breakdown = score_result['breakdown']
    
    # Determine risk level
    if score >= 7:
        risk_level = "HIGH"
        risk_color = "#dc3545"
        risk_emoji = "⚠️"
        description = "Multiple catalysts present - expect significant market swings"
    elif score >= 4:
        risk_level = "MODERATE"
        risk_color = "#ffc107"
        risk_emoji = "⚠️"
        description = "Some catalysts present - potential for increased volatility"
    else:
        risk_level = "LOW"
        risk_color = "#28a745"
        risk_emoji = "✅"
        description = "Few catalysts - relatively calm market expected"
    
    # VIX status
    if current_vix < 15:
        vix_status = "Very Low"
    elif current_vix < 20:
        vix_status = "Low to Moderate"
    elif current_vix < 30:
        vix_status = "Elevated"
    else:
        vix_status = "High"
    
    # Catalysts
    catalysts = []
    if breakdown['fed_meeting']:
        catalysts.append("🏛️ Federal Reserve Meeting")
    if breakdown['earnings']:
        catalysts.append("📊 Major Tech Earnings")
    if breakdown['economic_data']:
        catalysts.append("📈 Economic Data Release")
    if breakdown['vix_low']:
        catalysts.append("💤 VIX Below 18")
    
    if not catalysts:
        catalysts = ["✅ No major catalysts today"]
    
    # Next high-risk day
    next_high_risk = None
    for i in range(1, 31):
        check_date = today + timedelta(days=i)
        if check_date.weekday() >= 5:
            continue
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            future_score = calculate_entry_score(check_date.strftime('%Y-%m-%d'))
            sys.stdout = old_stdout
            
            if future_score['score'] >= 7:
                next_high_risk = {
                    'date': check_date.strftime('%B %d, %Y'),
                    'days_away': i,
                    'score': future_score['score']
                }
                break
        except:
            sys.stdout = old_stdout
    
    if not next_high_risk:
        # Check next Fed meeting
        fed_dates = get_all_fed_dates()
        for fed_date in sorted(fed_dates):
            if pd.to_datetime(fed_date) > today:
                fed_dt = pd.to_datetime(fed_date)
                days_until = (fed_dt - today).days
                if days_until <= 30:
                    next_high_risk = {
                        'date': fed_dt.strftime('%B %d, %Y'),
                        'days_away': days_until,
                        'score': 'Fed Meeting',
                        'type': 'fed'
                    }
                break
    
    return {
        'date': today.strftime('%A, %B %d, %Y'),
        'score': score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'risk_emoji': risk_emoji,
        'description': description,
        'vix': f"{current_vix:.2f}",
        'vix_status': vix_status,
        'catalysts': catalysts,
        'next_high_risk': next_high_risk
    }


def get_weekly_scores():
    """Get scores for next 7 days."""
    today = datetime.now()
    weekly = []
    
    for i in range(7):
        check_date = today + timedelta(days=i)
        
        if check_date.weekday() >= 5:
            continue
        
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            score_result = calculate_entry_score(check_date.strftime('%Y-%m-%d'))
            sys.stdout = old_stdout
            
            score = score_result['score']
            
            if score >= 7:
                color = "#dc3545"
                level = "HIGH"
            elif score >= 4:
                color = "#ffc107"
                level = "MODERATE"
            else:
                color = "#28a745"
                level = "LOW"
            
            weekly.append({
                'date': check_date.strftime('%a, %b %d'),
                'score': score,
                'color': color,
                'level': level
            })
        except:
            sys.stdout = old_stdout
    
    return weekly


@app.route('/')
def index():
    """Main dashboard page."""
    data = get_volatility_data()
    return render_template('index.html', data=data)


@app.route('/weekly')
def weekly():
    """Weekly view page."""
    data = get_volatility_data()
    weekly_data = get_weekly_scores()
    return render_template('weekly.html', data=data, weekly=weekly_data)

@app.route('/fed-calendar')
def fed_calendar():
    """Fed meetings calendar page."""
    data = get_volatility_data()
    
    today = datetime.now()
    fed_dates = get_all_fed_dates()
    
    upcoming_feds = []
    
    for fed_date in sorted(fed_dates):
        fed_dt = pd.to_datetime(fed_date)
        
        # Only show future meetings
        if fed_dt < today:
            continue
        
        # Calculate entry date
        entry_date = fed_dt - timedelta(days=3)
        while entry_date.weekday() >= 5:
            entry_date -= timedelta(days=1)
        
        days_until = (fed_dt - today).days
        days_until_entry = (entry_date - today).days
        
        # Get score
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            score_result = calculate_entry_score(fed_date)
            sys.stdout = old_stdout
            
            score = score_result['score']
            
            if score >= 7:
                color = "#dc3545"
                level = "HIGH"
                emoji = "🔥"
            elif score >= 4:
                color = "#ffc107"
                level = "MODERATE"
                emoji = "⚠️"
            else:
                color = "#28a745"
                level = "LOW"
                emoji = "💤"
            
            upcoming_feds.append({
                'fed_date': fed_dt.strftime('%B %d, %Y'),
                'fed_date_short': fed_dt.strftime('%b %d'),
                'entry_date': entry_date.strftime('%B %d, %Y'),
                'entry_date_short': entry_date.strftime('%b %d'),
                'days_until': days_until,
                'days_until_entry': days_until_entry,
                'score': score,
                'level': level,
                'color': color,
                'emoji': emoji,
                'breakdown': score_result['breakdown']
            })
        except:
            sys.stdout = old_stdout
    
    return render_template('fed_calendar.html', data=data, feds=upcoming_feds)

@app.route('/api/score')
def api_score():
    """API endpoint for current score (for mobile apps, etc)."""
    data = get_volatility_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)