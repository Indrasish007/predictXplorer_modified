# 🔮 PredictXplorer

> **A unified AI-powered platform for car price prediction, WhatsApp chat analysis with emoji sentiment, and stock market forecasting — built with Streamlit & Python.**

[![GitHub](https://img.shields.io/badge/GitHub-Indrasish007%2FpredictXplorer__modified-181717?style=flat-square&logo=github)](https://github.com/Indrasish007/predictXplorer_modified)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-FF4B4B?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![ML](https://img.shields.io/badge/ML-scikit--learn%20%7C%20Prophet-orange?style=flat-square)

---

## ✨ Features

### 💬 WhatsApp Chat Analyzer
Upload any WhatsApp `.txt` export and get:
- 📊 **Top statistics** — total messages, words, media, and links shared
- 🎭 **Emoji Sentiment Analysis** — scores conversations as Positive / Neutral / Negative on a –1.0 → +1.0 scale
- 🔢 **Emoji Frequency** — top 15 emojis used, per user or overall
- 📅 **Monthly & Daily timelines** — visualise message activity over time
- 🌡️ **Weekly heatmap** — discover the busiest hours and days
- ☁️ **Word Cloud** — most commonly used words, filtered by stopwords
- 👥 **Most active members** — participation breakdown with percentage share

Supports Android (12h & 24h) and iOS WhatsApp export formats.

---

### 🚗 Car Price Predictor
Get an instant AI-powered valuation for second-hand cars:
- Select **brand**, **model**, **year of manufacture**, **fuel type**, and **kilometres driven**
- Powered by a **Linear Regression model** trained on real Indian used-car market data
- Instant ₹ price estimate rendered in an animated result card

---

### 📈 Stock Price Forecaster
Forecast up to **4 years** of stock prices:
- Supports **30+ popular global stocks** (Apple, Tesla, NVIDIA, Meta, and more)
- Powered by **Meta's Prophet time-series model** or **Linear Regression (Trend Analysis)**
- Interactive **Plotly charts** for historical Open/Close prices
- **Trend decomposition** — visualise yearly and weekly seasonality components
- Live stock data fetched directly from Yahoo Finance API (JSON endpoint) with Stooq fallback from 2015 to today

---

## 🗂️ Project Structure

```
PredictXplorer/
│
├── app.py                      # 🏠 Home / landing page
├── navbar.py                   # Navigation bar component
├── sidebar.py                  # Sidebar navigation component
├── helper.py                   # WhatsApp analysis helper functions
├── preprocessor.py             # WhatsApp chat text parser
│
├── pages/
│   ├── whatsapp.py             # 💬 WhatsApp Analyzer page
│   ├── car.py                  # 🚗 Car Price Predictor page
│   └── stock.py                # 📈 Stock Forecaster page
│
├── LinearRegressionModel.pkl   # Trained car price ML model
├── refine_car.csv              # Cleaned car dataset
├── stocks.csv                  # Stock ticker list
├── bengali_stop_words.txt      # Stop words for word cloud
│
├── .streamlit/                 # Streamlit configuration
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/Indrasish007/predictXplorer_modified.git
cd predictXplorer_modified
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | 1.45.1 | Web app framework |
| `pandas` | 2.2.3 | Data manipulation |
| `numpy` | 1.26.4 | Numerical computing |
| `scikit-learn` | 1.5.2 | Car price ML model |
| `plotly` | 5.24.1 | Interactive charts |
| `matplotlib` | 3.9.4 | Static charts |
| `seaborn` | 0.13.2 | Heatmap visualization |
| `prophet` | 1.1.6 | Time-series forecasting |
| `wordcloud` | 1.9.4 | Word cloud generation |
| `Pillow` | 10.4.0 | Image handling |
| `emoji` | 2.15.0 | Emoji sentiment parsing |
| `pyarrow` | 17.0.0 | DataFrame optimization |

---

## 🌐 Deployment

### Streamlit Community Cloud *(Recommended — Free)*
1. Push the project to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set main file to `app.py`
4. Click **Deploy** — you'll get a public URL instantly

> ⚠️ **Note:** Large image assets (`x_car.jpg`, `x_car_price_new.jpg`) are ~11 MB each. Consider compressing them or adding them to `.gitignore` to stay within GitHub's 100 MB file limit.

### Other Platforms
- **Render.com** — Connect GitHub repo, set start command to `streamlit run app.py --server.port=10000 --server.address=0.0.0.0`
- **Google Cloud Run** — Containerise with Docker and deploy via Cloud Run

---

## 📖 How to Export WhatsApp Chats

1. Open any WhatsApp chat
2. Tap **⋮ (three dots) → More → Export Chat**
3. Choose **"Without Media"**
4. Save the `.txt` file and upload it to the WhatsApp Analyzer

**Supported formats:**
| Format | Pattern |
|---|---|
| Android 24h | `DD/MM/YY, HH:MM - Name: Message` |
| Android 12h | `DD/MM/YY, HH:MM AM/PM - Name: Message` |
| iOS | `[DD/MM/YY, HH:MM:SS] Name: Message` |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📬 Contact

| Name | Email |
|---|---|
| Indrasis Hadhya | [indrasishadhya770@gmail.com](mailto:indrasishadhya770@gmail.com) |
| Madhuri Das | [dashimadri1412@gmail.com](mailto:dashimadri1412@gmail.com) |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ❤️ using Streamlit & Python · © 2024 PredictXplorer</p>
