import streamlit as st
import datetime as dt
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

model_option = st.selectbox(
    "Select Forecasting Model",
    ["Linear Regression (Statistical Trend)", "Prophet (Meta's Time-Series)"],
    help="Linear Regression projects the long-term trend, while Prophet captures seasonality (weekly/yearly) and trends."
)

@st.cache_data(ttl=3600)
def load_data(ticker):
    """Pure data-fetching function — NO st.* calls inside a cached function."""
    start_ts = int(time.mktime(time.strptime(START, "%Y-%m-%d")))
    end_ts = int(time.mktime(time.strptime(TODAY, "%Y-%m-%d")))
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start_ts}&period2={end_ts}&interval=1d"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                if 'chart' in res_json and res_json['chart']['result']:
                    result = res_json['chart']['result'][0]
                    timestamps = result.get('timestamp', [])
                    indicators = result.get('indicators', {}).get('quote', [{}])[0]
                    
                    # Try to get adjusted close if available, else standard close
                    adjclose_data = result.get('indicators', {}).get('adjclose', [{}])[0]
                    close_prices = adjclose_data.get('adjclose', indicators.get('close', []))
                    open_prices = indicators.get('open', [])
                    
                    if timestamps and close_prices and open_prices:
                        df = pd.DataFrame({
                            'Date': pd.to_datetime(timestamps, unit='s'),
                            'Open': open_prices,
                            'Close': close_prices
                        })
                        # Drop rows with missing values
                        df = df.dropna(subset=['Open', 'Close'])
                        # Ensure timezone-naive and normalized
                        df['Date'] = df['Date'].dt.tz_localize(None).dt.normalize()
                        
                        if len(df) >= 50:
                            return df, None
            elif response.status_code == 429:
                time.sleep(2 ** (attempt + 1))
        except Exception:
            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

    # Fallback: Direct Stooq CSV fetch (cloud-friendly alternative)
    try:
        stooq_url = f"https://stooq.com/q/d/l/?s={ticker}.US&d1={START.replace('-', '')}&d2={TODAY.replace('-', '')}&i=d"
        res = requests.get(stooq_url, headers=headers, timeout=10)
        if res.status_code == 200 and "Get your apikey" not in res.text:
            from io import StringIO
            df_stooq = pd.read_csv(StringIO(res.text))
            if 'Close' in df_stooq.columns and 'Open' in df_stooq.columns:
                df_stooq['Date'] = pd.to_datetime(df_stooq['Date'])
                df_stooq = df_stooq[['Date', 'Open', 'Close']]
                df_stooq = df_stooq.sort_values('Date').reset_index(drop=True)
                return df_stooq, None
    except Exception:
        pass

    return None, (
        "Could not fetch data from Yahoo Finance API or Stooq. "
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
st.subheader(f"Forecasting {n_years} year(s) ahead with {model_option.split(' ')[0]}")

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

    if "Prophet" in model_option:
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

    else:  # Linear Regression
        with st.spinner("Training Linear Regression model... ⏳"):
            from sklearn.linear_model import LinearRegression
            import numpy as np

            # Prepare training features: number of days since the first date in training set
            start_date_train = df_train['ds'].min()
            df_train['days'] = (df_train['ds'] - start_date_train).dt.days
            
            X_train = df_train[['days']].values
            y_train = df_train['y'].values

            lr = LinearRegression()
            lr.fit(X_train, y_train)

            # Create future dataframe
            last_date = df_train['ds'].max()
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=period, freq='D')
            
            # Combine training and future dates for plotting
            all_dates = pd.concat([df_train['ds'], pd.Series(future_dates)]).reset_index(drop=True)
            all_days = (all_dates - start_date_train).dt.days.values.reshape(-1, 1)
            
            predictions = lr.predict(all_days)
            residuals = y_train - lr.predict(X_train)
            res_std = np.std(residuals)
            
            # Create a forecast dataframe matching Prophet's column names for compatibility
            forecast = pd.DataFrame({
                'ds': all_dates,
                'yhat': predictions,
                'yhat_lower': predictions - 1.96 * res_std,
                'yhat_upper': predictions + 1.96 * res_std
            })

        st.subheader("Forecast Data (last 5 rows)")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

        st.write("### Forecast Chart")
        # Plotly chart for Linear Regression
        fig1 = go.Figure()
        # Historical actual prices
        fig1.add_trace(go.Scatter(
            x=df_train['ds'], 
            y=df_train['y'], 
            name='Actual Close', 
            mode='markers', 
            marker=dict(color='cyan', size=3)
        ))
        # Regression trend line
        fig1.add_trace(go.Scatter(
            x=forecast['ds'], 
            y=forecast['yhat'], 
            name='Trend (Fit & Forecast)', 
            line=dict(color='orange', width=2)
        ))
        # Confidence interval upper
        fig1.add_trace(go.Scatter(
            x=forecast['ds'], 
            y=forecast['yhat_upper'], 
            name='Upper Bound', 
            line=dict(dash='dash', color='rgba(255, 165, 0, 0.3)'),
            showlegend=False
        ))
        # Confidence interval lower
        fig1.add_trace(go.Scatter(
            x=forecast['ds'], 
            y=forecast['yhat_lower'], 
            name='Lower Bound (95% CI)', 
            line=dict(dash='dash', color='rgba(255, 165, 0, 0.3)'),
            fill='tonexty',
            fillcolor='rgba(255, 165, 0, 0.05)'
        ))
        
        fig1.update_layout(
            title_text="Stock Price Forecast - Linear Regression",
            xaxis_rangeslider_visible=True,
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font=dict(color='white')
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Add trend explanation for Linear Regression components
        st.write("### Trend Analysis Details")
        slope = lr.coef_[0]
        intercept = lr.intercept_
        st.markdown(f"""
        - **Daily Growth Rate:** `${slope:.4f}` per day (annualized: `${slope * 365.25:.2f}` per year)
        - **Linear Equation:** `Price = {slope:.4f} * Days + {intercept:.2f}`
        - **Residual Std Dev:** `${res_std:.2f}` (represents average prediction deviation)
        """)

except Exception as e:
    st.error(f"Prediction error: {e}")
    if "stan_backend" in str(e):
        st.warning(
            "⚠️ **Prophet Backend Issue:** Streamlit Cloud's container environment has a compilation/dependency issue with the Prophet compiler backend. "
            "Please make sure the **Select Forecasting Model** dropdown above is set to **Linear Regression (Statistical Trend)** to generate the forecast successfully."
        )
    st.write("**Debug info:**")
    st.write(f"Data shape: {data.shape}")
    st.write(f"Columns: {data.columns.tolist()}")
    st.write(data.head())