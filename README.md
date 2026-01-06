# Market Volatility Score

Daily market volatility scoring based on Fed meetings, VIX levels, earnings, and economic data.

**Simple idea:** Score each day 0-9 points. More catalysts = higher volatility risk.

## Quick Start

```bash
pip install flask pandas yfinance
python app.py
```

Visit `http://localhost:5001`

## Scoring System

Each catalyst adds points (max 9):

| Catalyst | Points | Description |
|----------|--------|-------------|
| Fed Meeting | +2 | FOMC policy decision |
| VIX < 18 | +2 | Low volatility environment |
| Tech Earnings | +3 | FAANG earnings ±5 days from Fed |
| CPI/NFP Data | +2 | Economic data ±5 days from Fed |

**Risk Levels:**
- 7-9 points: 🔥 HIGH - Multiple catalysts
- 4-6 points: ⚠️ MODERATE - Some catalysts  
- 0-3 points: ✅ LOW - Few catalysts

## Usage

**Web Dashboard:**
```bash
python app.py
# Visit http://localhost:5001
```

**CLI Report:**
```bash
python daily_volatility_score.py
```

**Check Specific Date:**
```bash
python daily_volatility_score.py 2025-11-20
```

**API:**
```bash
curl http://localhost:5001/api/score
```

## Features

- 🌐 Web dashboard with daily score
- 📅 7-day outlook calendar
- 🏛️ Fed meeting tracker
- 📊 Real-time VIX data
- 📡 JSON API

## Project Structure

```
market-volatility-score/
├── app.py                      # Flask web app
├── entry_score.py              # Scoring engine
├── daily_volatility_score.py   # CLI tool
├── fed_meetings.py             # Fed calendar
├── earnings.py                 # Earnings checker
├── economic_date.py            # CPI/NFP dates
└── below18.py                  # VIX checker
```

## Installation

```bash
git clone https://github.com/yourusername/market-volatility-score.git
cd market-volatility-score
pip install -r requirements.txt
python app.py
```

**Requirements:**
```
flask
pandas
yfinance
```

## Data Sources

- VIX: Yahoo Finance (real-time)
- Fed dates: federalreserve.gov (updated annually)
- Earnings: Yahoo Finance API (automatic)
- CPI/NFP: BLS calendars


**Port 5001 in use:**
Change port in `app.py`: `app.run(port=5002)`

**VIX download fails:**
Check internet connection or wait (Yahoo Finance rate limits)


---

**Disclaimer:** Educational purposes only. Markets are unpredictable. Not financial advice.
