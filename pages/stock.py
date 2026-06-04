import streamlit as st
import datetime as dt
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import time
import requests
import sidebar

# Render Custom Sidebar
sidebar.render(current_page="stock")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

@keyframes fadeInUp  { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes float     { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
@keyframes shimmer   { 0%{background-position:-200% center} 100%{background-position:200% center} }
@keyframes pulseGlow { 0%,100%{box-shadow:0 0 5px rgba(135,206,235,.3)} 50%{box-shadow:0 0 25px rgba(135,206,235,.8)} }

* { font-family: 'Inter', sans-serif; }
.main { background: #06060f; }
[data-testid="stAppViewContainer"] { padding-top: 0.5rem; }

.stButton>button {
    background: linear-gradient(135deg, rgba(135,206,235,.15), rgba(135,206,235,.05));
    color: #87CEEB;
    font-weight: 600;
    border-radius: 10px;
    border: 1px solid rgba(135,206,235,.3);
    transition: all .3s ease;
    animation: fadeInUp .5s ease-out;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #87CEEB, #5ba8cc);
    color: #06060f;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(135,206,235,.4);
    border-color: transparent;
}

.page-title {
    text-align: center;
    font-size: clamp(2em,5vw,3.5em);
    font-weight: 800;
    background: linear-gradient(135deg, #87CEEB 0%, #fff 50%, #87CEEB 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite, fadeInUp .8s ease-out;
    margin-bottom: 6px;
}
.stock-icon { font-size:3.5em; animation:float 3s ease-in-out infinite; display:block; text-align:center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<span class="stock-icon">📈</span>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Stock Price Forecaster</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8899bb;margin-bottom:20px;'>Predict 1–4 years of stock prices with Meta's Prophet model</p>", unsafe_allow_html=True)

START = "2015-01-01"
TODAY = dt.date.today().strftime("%Y-%m-%d")

# -------------------------------------------------------
# FIX 1: Load stock list WITHOUT making API calls.
# The old code called yf.Ticker(ticker).info for every
# ticker in the CSV — that's 199 network requests on
# startup which caused the infinite loading spinner.
# -------------------------------------------------------
@st.cache_data
def load_popular_stocks():
    # Curated popular stocks — no API calls needed at startup
    popular = [
        ("Apple Inc.", "AAPL"),
        ("Microsoft Corporation", "MSFT"),
        ("Amazon.com Inc.", "AMZN"),
        ("Alphabet Inc. (Google)", "GOOGL"),
        ("Tesla Inc.", "TSLA"),
        ("Meta Platforms Inc.", "META"),
        ("NVIDIA Corporation", "NVDA"),
        ("Netflix Inc.", "NFLX"),
        ("Adobe Inc.", "ADBE"),
        ("Salesforce Inc.", "CRM"),
        ("JPMorgan Chase", "JPM"),
        ("Berkshire Hathaway B", "BRK-B"),
        ("Visa Inc.", "V"),
        ("Johnson & Johnson", "JNJ"),
        ("Pfizer Inc.", "PFE"),
        ("Coca-Cola Co.", "KO"),
        ("Walmart Inc.", "WMT"),
        ("ExxonMobil Corp.", "XOM"),
        ("Chevron Corp.", "CVX"),
        ("Nike Inc.", "NKE"),
        ("McDonald's Corp.", "MCD"),
        ("Boeing Co.", "BA"),
        ("Lockheed Martin", "LMT"),
        ("PayPal Holdings", "PYPL"),
        ("Uber Technologies", "UBER"),
        ("Airbnb Inc.", "ABNB"),
        ("Spotify Technology", "SPOT"),
        ("FedEx Corp.", "FDX"),
        ("UPS", "UPS"),
        ("Caterpillar Inc.", "CAT"),
    ]
    try:
        df = pd.read_csv('stocks.csv', header=None)
        tickers_from_csv = df[0].dropna().astype(str).str.strip().tolist()
        # Only use well-known US tickers from CSV (no Indian NSE tickers — they need .NS suffix)
        us_tickers = [t for t in tickers_from_csv if '.' not in t and len(t) <= 5]
        # Merge: CSV tickers as (ticker, ticker) plus curated names
        known = {t: name for name, t in popular}
        merged = []
        seen = set()
        for t in us_tickers:
            if t not in seen:
                merged.append((known.get(t, t), t))
                seen.add(t)
        return merged if merged else popular
    except FileNotFoundError:
        return popular

stocks = load_popular_stocks()

selected_stock = st.selectbox(
    "Select a stock for prediction",
    stocks,
    format_func=lambda x: f"{x[0]} ({x[1]})"
)
selected_stock_name, selected_ticker = selected_stock

n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

# -------------------------------------------------------
# FIX 2: Correct column flattening for yfinance v0.2+
# yf.download() returns multi-level columns:
#   ('Close', 'AAPL'), ('Open', 'AAPL'), ...
# The old code did col[1] → got 'AAPL' instead of 'Close'
# Fix: use col[0] to get the field name.
# FIX 3: Strip timezone from Date so Prophet works.
# -------------------------------------------------------
def _make_yf_session():
    """Return a requests Session with browser-like headers to avoid Yahoo Finance rate limiting."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return session

def _normalize(data):
    """Flatten columns, reset index, strip timezone. Returns clean df or None."""
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]
    if 'Close' not in data.columns or 'Open' not in data.columns:
        return None
    data = data.reset_index()
    date_col = 'Date' if 'Date' in data.columns else data.columns[0]
    data = data.rename(columns={date_col: 'Date'})
    if pd.api.types.is_datetime64tz_dtype(data['Date']):
        data['Date'] = data['Date'].dt.tz_localize(None)
    if len(data) < 100:
        return None
    return data

@st.cache_data(ttl=3600)
def load_data(ticker):
    """Pure data-fetching function — NO st.* calls inside a cached function."""

    # ── Tier 1: yfinance with browser-like headers ──────────────────────────
    for attempt in range(3):
        try:
            session = _make_yf_session()
            raw = yf.download(ticker, START, TODAY, progress=False, session=session)
            if not raw.empty:
                df = _normalize(raw)
                if df is not None:
                    return df, None
        except Exception as e:
            err = str(e)
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))   # 2s, 4s
                continue

    # ── Tier 2: yfinance Ticker.history() ───────────────────────────────────
    try:
        session = _make_yf_session()
        raw = yf.Ticker(ticker, session=session).history(start=START, end=TODAY)
        if not raw.empty:
            df = _normalize(raw)
            if df is not None:
                return df, None
    except Exception:
        pass

    # ── Tier 3: Stooq via pandas-datareader (cloud-friendly) ────────────────
    try:
        from pandas_datareader import data as pdr
        # Stooq uses TICKER.US for US stocks
        raw = pdr.DataReader(f"{ticker}.US", 'stooq', start=START, end=TODAY)
        if not raw.empty:
            raw = raw.sort_index()          # Stooq returns newest-first
            df = _normalize(raw)
            if df is not None:
                return df, None
    except Exception as e:
        pass

    return None, (
        "Could not fetch data from Yahoo Finance or Stooq. "
        "Both may be temporarily rate-limiting this server. "
        "Please wait 1–2 minutes and try again."
    )

with st.spinner(f"Fetching stock data for {selected_ticker}..."):
    data, error = load_data(selected_ticker)

if error or data is None:
    st.error(f"❌ Could not load data for **{selected_ticker}**.")
    if error:
        st.error(f"Reason: {error}")
    st.info("💡 Try selecting a different stock from the dropdown.")
    st.stop()

st.success(f"✅ Loaded {len(data)} data points for {selected_ticker}")

st.subheader("Raw Data (last 5 rows)")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open', line=dict(color='cyan')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close', line=dict(color='orange')))
    fig.update_layout(
        title_text="Historical Stock Prices",
        xaxis_rangeslider_visible=True,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

plot_raw_data()

# -------------------------------------------------------
# Forecasting with Prophet
# -------------------------------------------------------
st.subheader(f"Forecasting {n_years} year(s) ahead with Prophet")

try:
    df_train = data[['Date', 'Close']].copy()
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    df_train = df_train.dropna()
    df_train['ds'] = pd.to_datetime(df_train['ds'])

    # Ensure tz-naive (double check)
    if hasattr(df_train['ds'].dtype, 'tz') and df_train['ds'].dt.tz is not None:
        df_train['ds'] = df_train['ds'].dt.tz_localize(None)

    if len(df_train) < 50:
        st.error("Not enough valid data points for prediction (need ≥ 50).")
        st.stop()

    with st.spinner("Training Prophet model... this may take a moment ⏳"):
        m = Prophet()
        m.fit(df_train)

    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader("Forecast Data (last 5 rows)")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    st.write("### Forecast Chart")
    try:
        fig1 = plot_plotly(m, forecast)
        fig1.update_layout(
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font=dict(color='white')
        )
        st.plotly_chart(fig1, use_container_width=True)
    except Exception as plot_error:
        st.warning(f"Interactive plot failed ({plot_error}), showing simple chart.")
        chart_data = forecast[['ds', 'yhat']].set_index('ds')
        st.line_chart(chart_data)

    st.write("### Forecast Components")
    try:
        fig2 = m.plot_components(forecast)
        st.pyplot(fig2, use_container_width=True)
    except Exception as comp_error:
        st.warning(f"Components plot error: {comp_error}")

except Exception as e:
    st.error(f"Prediction error: {e}")
    st.write("**Debug info:**")
    st.write(f"Data shape: {data.shape}")
    st.write(f"Columns: {data.columns.tolist()}")
    st.write(data.head())