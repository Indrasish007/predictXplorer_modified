import streamlit as st
import datetime as dt
import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

# Custom CSS to style the page
st.markdown("""
    <style>
        .main {
            background-color: Black;
        }
        h1 {
            color: #87CEEB;
            text-align: center;
            font-family: 'Trebuchet MS', sans-serif;
            font-size: 3em;
        }
        .stButton>button {
            background-color: #87CEEB;
            color: Black;
            font-size: 1.2em;
            font-family: 'Trebuchet MS', sans-serif;
            border-radius: 12px;
        }
        .stButton>button:hover {
            background-color: #357ABD;
            color: white;
        }
        .css-18e3th9 {
            padding-top: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

empty_col,col1,col2,col3,col4=st.columns([0.15,1,1,1,1])
with col1:
    if st.button("Home Page"):
        st.switch_page("app.py")
with col2:
     if st.button("Whatsapp Chat Analyzer"):
        st.switch_page("pages/whatsapp.py")
with col3:
    if st.button("Car Price Prediction"):
        st.switch_page("pages/car.py")
with col4:
    if st.button("Stock Price Prediction"):
        st.switch_page("pages/stock.py")

START="2015-01-01"
TODAY=dt.date.today().strftime("%Y-%m-%d")

# Load popular stock tickers and names
@st.cache_data
def load_popular_stocks():
    # Fallback to hardcoded popular stocks if CSV doesn't exist
    try:
        df = pd.read_csv('stocks.csv', header=None)
        stock_list = []
        for ticker in df[0].tolist():
            try:
                stock_info = yf.Ticker(ticker)
                stock_name = stock_info.info.get('longName', ticker)
                stock_list.append((stock_name, ticker))
            except:
                stock_list.append((ticker, ticker))  # Fallback to ticker as name
        return stock_list
    except FileNotFoundError:
        # Hardcoded popular stocks as fallback
        st.warning("stocks.csv not found. Using default popular stocks.")
        return [
            ("Apple Inc.", "AAPL"),
            ("Microsoft Corporation", "MSFT"), 
            ("Amazon.com Inc.", "AMZN"),
            ("Alphabet Inc.", "GOOGL"),
            ("Tesla Inc.", "TSLA"),
            ("Meta Platforms Inc.", "META"),
            ("NVIDIA Corporation", "NVDA"),
            ("Netflix Inc.", "NFLX"),
            ("Adobe Inc.", "ADBE"),
            ("Salesforce Inc.", "CRM")
        ]

stocks = load_popular_stocks()

st.title("Stock prediction app")
selected_stock_name, selected_ticker = st.selectbox(
    "Select dataset for prediction", stocks, format_func=lambda x: x[0]
)

n_years=st.slider("Years of prediction:", 1, 4)
period=n_years*365

@st.cache_data
def load_data(ticker):
    try:
        st.info(f"Attempting to download data for {ticker} from {START} to {TODAY}")
        
        # Try downloading with different parameters
        data = yf.download(ticker, START, TODAY, progress=False, timeout=10, 
                          threads=False, group_by=None, auto_adjust=True)
        
        # Debug info
        st.info(f"Downloaded data shape: {data.shape if not data.empty else 'Empty'}")
        
        # Check if data is empty
        if data.empty:
            st.error(f"❌ No data found for ticker {ticker}")
            st.error("Possible causes:")
            st.error("• 404 Error: Ticker symbol might be invalid or changed")
            st.error("• Stock might be delisted")
            st.error("• Yahoo Finance API temporary issues")
            
            # Try alternative approach
            st.info("🔄 Trying alternative download method...")
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(start=START, end=TODAY)
                if not data.empty:
                    st.success("✅ Alternative method worked!")
                else:
                    st.error("❌ Alternative method also failed")
                    return None
            except Exception as alt_error:
                st.error(f"Alternative method error: {str(alt_error)}")
                return None
            
        # Check if we have the required columns
        # Handle new yfinance column structure with ticker prefixes
        if data.columns.nlevels > 1:
            # Multi-level columns like ('AAPL', 'Close')
            data.columns = [col[1] if isinstance(col, tuple) else col for col in data.columns]
        
        if 'Close' not in data.columns or 'Open' not in data.columns:
            st.error("Data doesn't contain required columns (Open, Close)")
            st.error(f"Available columns: {list(data.columns)}")
            return None
            
        data.reset_index(inplace=True)
        
        # Additional validation
        if len(data) < 100:  # Need sufficient data for Prophet
            st.error(f"Insufficient data for prediction. Only {len(data)} data points found.")
            return None
            
        st.success(f"✅ Successfully loaded {len(data)} data points for {ticker}")
        return data
        
    except Exception as e:
        error_msg = str(e).lower()
        if "404" in error_msg or "not found" in error_msg:
            st.error(f"❌ HTTP 404 Error for {ticker}")
            st.error("This ticker symbol might be:")
            st.error("• Invalid or misspelled")
            st.error("• Changed (company merged/renamed)")
            st.error("• Delisted from exchanges")
            st.info("💡 Try selecting a different stock from the dropdown")
        else:
            st.error(f"Error loading data for {ticker}: {str(e)}")
            st.error("Try selecting a different stock or check your internet connection.")
        return None

data_load_state=st.text("Loading data...")
data=load_data(selected_ticker)

if data is None:
    st.stop()  # Stop execution if no data

data_load_state.text("Loading data... done!")

st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data():
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
    fig.update_layout(title_text="Time Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting with error handling
try:
    df_train = data[['Date','Close']].copy()
    df_train = df_train.rename(columns={"Date":"ds","Close":"y"})
    
    # Remove any NaN values
    df_train = df_train.dropna()
    
    # Ensure ds column is datetime
    df_train['ds'] = pd.to_datetime(df_train['ds'])
    
    # Additional validation for Prophet
    if len(df_train) < 50:
        st.error("Not enough valid data points for prediction")
        st.stop()
    
    # Check for null values properly
    if df_train['y'].isnull().sum() > 0:
        st.error("Contains null values in price data")
        st.stop()
        
    m = Prophet()
    m.fit(df_train)
    
    # Make future dataframe and predict
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader("Forecast data")
    st.write(forecast.tail())
    
    st.write('Forecast data')
    try:
        fig1 = plot_plotly(m, forecast)
        fig1.update_traces(line=dict(color='cyan'))
        fig1.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='black',
            font=dict(color='yellow')
        )
        st.plotly_chart(fig1)
    except Exception as plot_error:
        st.error(f"Plotting error: {str(plot_error)}")
        # Fallback to simple line chart
        chart_data = forecast[['ds', 'yhat']].set_index('ds')
        st.line_chart(chart_data)
    
    st.write("Forecast components")
    try:
        fig2 = m.plot_components(forecast)
        st.pyplot(fig2)
    except Exception as comp_error:
        st.error(f"Components plot error: {str(comp_error)}")

except Exception as e:
    st.error(f"Prediction error: {str(e)}")
    st.error("This might be due to:")
    st.error("• Data format issues")
    st.error("• Prophet library compatibility")
    st.error("• Insufficient or invalid data")
    
    # Debug information
    st.subheader("Debug Information")
    if 'data' in locals():
        st.write(f"Data shape: {data.shape}")
        st.write(f"Data columns: {data.columns.tolist()}")
        st.write("Data sample:")
        st.write(data.head())