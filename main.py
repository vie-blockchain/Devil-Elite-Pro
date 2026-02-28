from flask import Flask, render_template, request, redirect, url_for, session
import yfinance as yf

app = Flask(__name__)
app.secret_key = "vie_terminal_99" 

ADMIN_EMAIL = "viefeng27@gmail.com"

# TERA SIGNALS DATA
signals_data = [
    {"id": 0, "asset": "GOLD (XAU/USD)", "type": "BUY", "entry": "2035.40", "tgt": "2055.00", "sl": "2028.00", "accuracy": "94%", "reason": "Institutional demand zone at 2035."},
    {"id": 1, "asset": "BITCOIN (BTC)", "type": "BUY", "entry": "68200", "tgt": "71500", "sl": "66800", "accuracy": "91%", "reason": "Liquidity grab at 68k support."},
    {"id": 2, "asset": "ETH (ETHEREUM)", "type": "SELL", "entry": "3550", "tgt": "3380", "sl": "3640", "accuracy": "82%", "reason": "Rejecting from major resistance."}
]

notifications = []

NAME_MAP = {
    'RELIANCE.NS': ('Reliance Industries', 'STOCKS'),
     'TATASTEEL.NS': ('Tata Steel', 'STOCKS'),
    'HDFCBANK.NS': ('HDFC Bank', 'STOCKS'),
    'AAPL': ('Apple Inc.', 'STOCKS'),
    'TSLA': ('Tesla Motors', 'STOCKS'),
      'ETH-USD': ('Ethereum', 'CRYPTO'),
    'SOL-USD': ('Solana', 'CRYPTO'),
    'DOGE-USD': ('Dogecoin', 'CRYPTO'),
  'BNB-USD': ('Binance Coin', 'CRYPTO'),
    'ADA-USD': ('Cardano', 'CRYPTO'),
    'XRP-USD': ('Ripple', 'CRYPTO'),

    # --- CRYPTO: HIGH GROWTH (Altcoins) ---
    'DOT-USD': ('Polkadot', 'CRYPTO'),
    'MATIC-USD': ('Polygon', 'CRYPTO'),
    'LINK-USD': ('Chainlink', 'CRYPTO'),
    'AVAX-USD': ('Avalanche', 'CRYPTO'),
    'NEAR-USD': ('NEAR Protocol', 'CRYPTO'),

    # --- CRYPTO: TRENDING / MEME (High Volatility) ---
    'SHIB-USD': ('Shiba Inu', 'CRYPTO'),
    'PEPE-USD': ('Pepe Coin', 'CRYPTO'),
    'BONK-USD': ('Bonk', 'CRYPTO'),
   '^NSEI': ('NIFTY 50', 'INDEX'),
    '^BSESN': ('SENSEX', 'INDEX'),
    '^IXIC': ('NASDAQ Composite', 'INDEX'),
    '^DJI': ('Dow Jones Industrial', 'INDEX'),
    '^GSPC': ('S&P 500', 'INDEX'),
      'ZOMATO.NS': ('Zomato Ltd', 'MIDCAP'),
    'SUZLON.NS': ('Suzlon Energy', 'SMALLCAP'),
    'IREDA.NS': ('IREDA', 'STOCKS'),
    'IDFCFIRSTB.NS': ('IDFC First Bank', 'STOCKS'),
    'TATASTEEL.NS': ('Tata Steel', 'STOCKS'),
    'RVNL.NS': ('Rail Vikas Nigam', 'MIDCAP'),
    'IRFC.NS': ('IRFC', 'MIDCAP'),
    'NVDA': ('NVIDIA Corporation', 'STOCKS'),
    'BTC-USD': ('Bitcoin', 'CRYPTO'),
    'ETH-USD': ('Ethereum', 'CRYPTO'),
    'GC=F': ('Gold Bullion', 'COMMODITY'),
    'CL=F': ('Crude Oil WTI', 'COMMODITY')
}

def get_complete_data():
    results = []
    for sym, (full_name, cat) in NAME_MAP.items():
        try:
            t = yf.Ticker(sym)
            df = t.history(period="1mo")
            curr = round(df['Close'].iloc[-1], 2)
            change = round(((curr - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100, 2)
            results.append({
                "symbol": sym, "full_name": full_name, "cat": cat,
                "price": curr, "change": change,
                "logic": f"Institutional order flow detected at {curr}. Monthly structure confirmed."
            })
        except: continue
    return results

# --- LOGIC: HAMESHA INTRO DIKHAO ---
@app.route('/')
def splash():
    return render_template('splash.html')

# --- LOGIC: INTRO KE BAAD STATUS CHECK ---
@app.route('/check_status')
def check_status():
    if session.get('authorized'):
        return redirect(url_for('home')) # Login hai toh Dashboard
    return redirect(url_for('login'))    # Nahi hai toh Login Page

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/google_verify', methods=['POST'])
def google_verify():
    email = request.form.get('user_email')
    if email and "@gmail.com" in email:
        session['authorized'] = True
        session['user_email'] = email
        return redirect(url_for('home'))
    return "Invalid Gmail! <a href='/login'>Try Again</a>"

@app.route('/dashboard')
def home():
    if not session.get('authorized'):
        return redirect(url_for('login'))
        
    data = get_complete_data()
    is_admin = session.get('user_email') == ADMIN_EMAIL
    
    news_data = [
        {"title": "US Fed Outlook", "impact": "HIGH", "time": "18:30", "desc": "Yields affecting XAUUSD stability."},
        {"title": "Crypto Whales", "impact": "MEDIUM", "time": "21:00", "desc": "Large BTC transfers to cold storage spotted."}
    ]
    return render_template('index.html', assets=data, signals=signals_data, news=news_data, is_admin=is_admin, notifications=notifications)

@app.route('/update_signal', methods=['POST'])
def update_signal():
    if session.get('user_email') == ADMIN_EMAIL:
        sig_id = int(request.form.get('sig_id'))
        signals_data[sig_id].update({
            "type": request.form.get('type'),
            "entry": request.form.get('entry'),
            "tgt": request.form.get('tgt'),
            "sl": request.form.get('sl'),
            "reason": request.form.get('reason')
        })
        notifications.append(f"UPDATE: {signals_data[sig_id]['asset']} Signal Changed!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)