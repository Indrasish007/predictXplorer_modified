import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

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


st.title("Whatsapp chat analyzer")
st.subheader("Analyse your whats app chat")
uploaded_file = st.file_uploader("Choose a text file")
try:
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        data= bytes_data.decode("utf-8")
        # st.text(data)
        df=preprocessor.preprocess(data)

        
        # st.dataframe(df)

        # fetch unique users
        user_list=df["users"].unique().tolist()
        user_list.remove("group_notification")
        user_list.sort()
        user_list.insert(0,"Overall")
        st.sidebar.title("Analysis")
        selected_user= st.sidebar.selectbox("The analysis with respect to",user_list)
        # 1st level analysis
        if st.sidebar.button('Show analysis'):

            num_messeges,words,media,num_links= helper.fetch_stats(selected_user,df)
            st.sidebar.header(selected_user)
            st.title("Top Stats")
            col1,col2,col3,col4= st.columns([2,2,1,2])
            with col1:
                st.header("Total messeges")
                st.subheader(num_messeges)
            with col2:
                st.header("Total words")
                st.subheader(words)
            with col3:
                st.header("Total media")
                st.subheader(media)
            with col4:
                st.header("Links shared")
                st.subheader(num_links)
                
            
        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="indigo")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        #daily timeline
        st.title("DailyTimeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(daily_timeline['specific_date'],daily_timeline['message'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        #weekly activity map
        st.title("Weekly Activity Map")
        col1,col2= st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            # st.dataframe(busy_day)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            # st.dataframe(busy_day)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="red")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        #HEATMAP
        st.title("Weekly Activity Heatmap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #  Bar chart and percentage of chatting
        if selected_user=="Overall":
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                st.header("Most busy user")
                ax.pie(x.values,labels=x.index, colors=['red', 'green', 'blue', 'orange','yellow'])
                # plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.header("Percentage of chatting")
                st.dataframe(new_df)
        # word cloud
        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])

        st.title("Most common words")
        st.pyplot(fig)
        # st.dataframe(most_common_df)
        # Display an error message if the user is not found in
except UnicodeDecodeError:
    st.error("Error: The file is not in the correct format. Please upload a valid text file.")
except ValueError:
    st.error("Error: There was an issue processing the file. Please make sure the file format is correct.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")