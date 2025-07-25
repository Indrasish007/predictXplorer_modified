import streamlit as st
from PIL import Image
# Set custom page configuration
st.set_page_config(
    page_title="PredictXplorer",
    page_icon=":crystal_ball:",
    layout="wide",
    initial_sidebar_state="collapsed"
)
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

empty_col,col1,col2,col3=st.columns([0.1,1,1,1])
with col2:
    st.title("PredictXplorer")
st.markdown('---')
empty_col,col1,col2,col3,col4=st.columns([0.25,1,1,1,1])
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

        
# whatsapp chat analysis
st.markdown("---")
col1, col2,col3= st.columns([1.25,2,1])
with col2:
    st.title("Whatsapp Chat analyzer")
    
col1,col2,col3,col4=st.columns([1,1,1,1])
with col1:
    st.image("x_whatsapp_pic.png",width=600)
with col3:
    st.image("x_whatsapp-icon-6953522.jpg",width=600)

st.markdown("""
### Unleash the Hidden Insights

Dive into the depths of your daily chats or seek meaningful patterns with our cutting-edge ***WhatsApp Chat Analyzer***. This tool provides comprehensive analysis with ease, offering:

- Detailed statistics on the number of messages sent and received.
- Insights into active days and your busiest chat hours.
- Analysis of the most commonly used words in your chats.
- Identification of who you chat with the most and analysis of conversation dynamics with different contacts.

### Interactive and User-Friendly

Enjoy interactive charts and graphs that make it easy to visualize your chat data.Simply export your WhatsApp chat as a text file and upload it to our analyzer. Our powerful algorithms will process the chat data to extract valuable insights.

View and interact with the results through an intuitive and user-friendly interface. Unlock the potential of your conversations today with the WhatsApp Chat Analyzer – your personal window into the world of chat data!

#### Click the button below to analyze your chats 
""")
col1, col2, col3 = st.columns([1, 1, 1])
with col1 :
    if st.button("Analyze WhatsApp Chats"):
        st.switch_page("pages/whatsapp.py")
        
#  car price prediction
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("Car Price Predictor")
    
col1,col2,col3,col4=st.columns([1,1,1,1])
with col1:
     st.image("x_car.jpg",width=600)
with col3:
    st.image("x_car_price_new.jpg",width=600)
st.markdown("""
## Highlights

Unlock the power of accurate car valuations with our state-of-the-art ***Car Price Prediction*** tool, designed to provide precise and insightful assessments of any vehicle's worth. This tool is an invaluable resource for anyone looking to buy, sell, or simply understand the market value of a car. By leveraging advanced algorithms and extensive data analysis, our ***Car Price Prediction tool*** takes into account a multitude of factors including the ***car’s company, model, year, fuel type, and how many kilometers are driven by the car***.

**Key Features:**

- **User-Friendly Interface:** Enter the car's details into our easy-to-use interface and receive an instant, comprehensive price prediction that reflects the car's true market value.
- **In-Depth Analysis:** Our tool goes beyond simple estimates, offering in-depth analysis and visualizations that show how various attributes.
- **Versatile Use:** Perfect for car enthusiasts, dealerships, and anyone in the market for a vehicle. 
- **Informed Decisions:** Equip yourself with the knowledge needed to make informed, confident decisions. Whether you're negotiating a sale, making a purchase, or just curious about a car's value, our tool provides the detailed insights you need to navigate the automotive market effectively.
- **Best Deals:** Make data-driven decisions with confidence and ensure you get the best possible deal with our comprehensive Car Price Prediction tool.
#### Click the button to predict the price of the car you want 
""")
col1, col2, col3 = st.columns([1, 1, 1])
with col1 :
    if st.button("Predict price"):
        st.switch_page("pages/car.py")
        
# Stock price prediction
st.markdown("---")
col1, col2,col3= st.columns([1,2,1])
with col2:
    st.title("Stock Price Predictor")
col1,col2,col3,col4=st.columns([1,1,1,1])
with col1:
    st.image("x_stock_price.jpg",width=600)
with col3:
    st.image("x_stock_price2.jpg",width=600)
import streamlit as st

import streamlit as st

st.markdown("""
### Stock Price Prediction

Welcome to the Stock Price Prediction app, your go-to tool for forecasting future stock prices using advanced machine learning algorithms. This app leverages historical stock data and the powerful Prophet model to provide insightful predictions, helping you make informed investment decisions. 

**Key Features:**

- **Popular Stocks Selection:** Choose from a list of popular stocks fetched from a CSV file for quick access.
- **Interactive User Interface:** Select the number of years for prediction using an intuitive slider.
- **Visual Data Representation:** Display raw stock data and interactive time series plots using Plotly, making it easy to understand the stock's performance over time.
- **Forecasting with Prophet:** Utilize the Prophet model to fit historical data and forecast future stock prices. View detailed forecast data, including forecast components and interactive plots.

**How It Works:**

1. **Load Popular Stocks:** The app reads a list of popular stocks from a CSV file and displays them in a dropdown menu for selection.
2. **Data Fetching:** Once a stock is selected, the app fetches historical stock data from Yahoo Finance, starting from January 1, 2015, to the current date.
3. **Raw Data Display:** The app shows the most recent data entries for transparency.
4. **Data Visualization:** Interactive charts display the stock's opening and closing prices over time, providing a clear visual representation of its historical performance.
5. **Prediction Model:** The Prophet model is applied to the stock's closing price data to generate future price predictions. Users can choose the prediction period, ranging from 1 to 4 years.
6. **Forecast Display:** The app presents the forecast data in an interactive plot, along with detailed forecast components.

Make data-driven decisions with confidence and stay ahead of the market with our comprehensive Stock Price Prediction app.
#### Click the button to predict the stock price of 4 years 
""")
col1, col2, col3 = st.columns([1, 1, 1])
with col1 :
    if st.button("Stock analysis"):
        st.switch_page("pages/stock.py")
st.markdown(
    '''
      ####  ***If you face any kind of inconvenience Contact us : indrasishadhya770@gmail.com ,  dashimadri1412@gmail.com*** 
    '''
)
# Add footer or additional elements if needed
st.markdown('''
    <hr>
    <footer style="text-align: center;">
        <p style="font-size: 0.8em;">&copy; 2024 PredictXplorer. All rights reserved.</p>
    </footer>
''', unsafe_allow_html=True)
  