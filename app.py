import streamlit as st
from PIL import Image
import sidebar

st.set_page_config(
    page_title="PredictXplorer",
    page_icon=":crystal_ball:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Render Custom Sidebar
sidebar.render(current_page="home")

# ─── Global CSS + Animations ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

/* ── Keyframes ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-40px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(40px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33%       { transform: translateY(-12px) rotate(1deg); }
    66%       { transform: translateY(-6px) rotate(-1deg); }
}
@keyframes shimmerText {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 8px rgba(135,206,235,0.2); }
    50%       { box-shadow: 0 0 30px rgba(135,206,235,0.6), 0 0 60px rgba(135,206,235,0.2); }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(135,206,235,0.2); }
    50%       { border-color: rgba(135,206,235,0.8); }
}
@keyframes particleDrift {
    0%   { transform: translateY(0) translateX(0) scale(1);   opacity: 0.7; }
    50%  { transform: translateY(-20px) translateX(10px) scale(1.2); opacity: 1; }
    100% { transform: translateY(0) translateX(0) scale(1);   opacity: 0.7; }
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes navSlide {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Base ── */
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.main { background: #06060f; }
[data-testid="stAppViewContainer"] { padding-top: 0.5rem; }


/* ── Feature Cards ── */
.hero-section {
    text-align: center;
    padding: 60px 20px 40px;
    position: relative;
    animation: fadeInUp 1s ease-out;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(135,206,235,0.15), rgba(135,206,235,0.05));
    border: 1px solid rgba(135,206,235,0.4);
    border-radius: 50px;
    padding: 6px 20px;
    color: #87CEEB;
    font-size: 0.85em;
    font-weight: 600;
    margin-bottom: 24px;
    letter-spacing: 2px;
    animation: pulseGlow 3s ease-in-out infinite;
}
.hero-title {
    font-size: clamp(2.5em, 6vw, 5em);
    font-weight: 800;
    background: linear-gradient(135deg, #87CEEB 0%, #ffffff 40%, #87CEEB 70%, #5ba8cc 100%);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmerText 4s linear infinite, fadeInUp 0.8s ease-out;
    line-height: 1.1;
    margin-bottom: 16px;
}
.hero-subtitle {
    color: #8899bb;
    font-size: 1.2em;
    max-width: 800px;
    margin: 0 auto 40px !important;
    line-height: 1.7;
    text-align: center !important;
    animation: fadeInUp 1s ease-out 0.2s both;
}
.hero-particles {
    position: relative;
    height: 80px;
    overflow: hidden;
    pointer-events: none;
}
.particle {
    position: absolute;
    border-radius: 50%;
    background: rgba(135,206,235,0.6);
    animation: particleDrift ease-in-out infinite;
}

/* ── Feature Cards ── */
.feature-card {
    background: linear-gradient(135deg, #0d1b2e 0%, #111827 50%, #0d1b2e 100%);
    border: 1px solid rgba(135,206,235,0.15);
    border-radius: 24px;
    padding: 32px 28px;
    margin: 12px 0;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    animation: scaleIn 0.7s ease-out;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #87CEEB, transparent);
    animation: shimmerText 3s linear infinite;
    background-size: 200% auto;
}
.feature-card:hover {
    transform: translateY(-10px) scale(1.01);
    border-color: rgba(135,206,235,0.5);
    box-shadow: 0 20px 50px rgba(135,206,235,0.15), 0 0 0 1px rgba(135,206,235,0.1);
}
.card-icon {
    font-size: 3.5em;
    margin-bottom: 16px;
    display: block;
    animation: float 4s ease-in-out infinite;
}
.card-title {
    color: #87CEEB;
    font-size: 1.6em;
    font-weight: 700;
    margin-bottom: 12px;
}
.card-desc {
    color: #8899bb;
    font-size: 0.95em;
    line-height: 1.7;
    margin-bottom: 20px;
}
.card-pill {
    display: inline-block;
    background: rgba(135,206,235,0.1);
    border: 1px solid rgba(135,206,235,0.25);
    color: #87CEEB;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78em;
    margin: 3px;
}

/* ── Section Divider ── */
.section-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 40px 0 30px;
    animation: fadeInLeft 0.6s ease-out;
}
.section-divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(135,206,235,0.3), transparent);
}
.section-divider-text {
    color: #87CEEB;
    font-size: 0.8em;
    font-weight: 600;
    letter-spacing: 3px;
    white-space: nowrap;
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
    animation: fadeInUp 0.8s ease-out 0.4s both;
    margin-bottom: 50px;
}
.stat-pill {
    background: linear-gradient(135deg, #0d1b2e, #111827);
    border: 1px solid rgba(135,206,235,0.2);
    border-radius: 50px;
    padding: 12px 24px;
    text-align: center;
    animation: borderGlow 4s ease-in-out infinite;
    transition: transform 0.3s ease;
}
.stat-pill:hover { transform: scale(1.08); }
.stat-pill-value { color: #87CEEB; font-size: 1.5em; font-weight: 800; display: block; }
.stat-pill-label { color: #8899bb; font-size: 0.75em; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 30px;
    border-top: 1px solid rgba(135,206,235,0.1);
    color: #8899bb;
    font-size: 0.85em;
    margin-top: 60px;
    animation: fadeInUp 0.6s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section" style="text-align: center !important;">
    <div class="hero-badge">✨ AI · ML · PREDICTIONS</div>
    <div class="hero-title" style="text-align: center !important;">PredictXplorer</div>
    <p class="hero-subtitle" style="text-align: center !important; margin: 0 auto 40px !important; max-width: 800px !important; display: block !important;">A unified AI-powered platform for car price prediction, WhatsApp chat insights with emoji sentiment analysis, and stock market forecasting.</p>
</div>
""", unsafe_allow_html=True)

# ─── Stats Pills ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-pill">
        <span class="stat-pill-value">3</span>
        <span class="stat-pill-label">AI Tools</span>
    </div>
    <div class="stat-pill">
        <span class="stat-pill-value">4+</span>
        <span class="stat-pill-label">ML Models</span>
    </div>
    <div class="stat-pill">
        <span class="stat-pill-value">∞</span>
        <span class="stat-pill-label">Predictions</span>
    </div>
    <div class="stat-pill">
        <span class="stat-pill-value">6</span>
        <span class="stat-pill-label">Chat Formats</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-divider">
    <div class="section-divider-line"></div>
    <div class="section-divider-text">EXPLORE TOOLS</div>
    <div class="section-divider-line"></div>
</div>
""", unsafe_allow_html=True)

# ─── Feature Cards ────────────────────────────────────────────────────────────
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
    <div class="feature-card">
        <span class="card-icon">💬</span>
        <div class="card-title">WhatsApp Analyzer</div>
        <div class="card-desc">
            Dive deep into your chats with message stats, timeline analysis,
            word clouds, activity heatmaps — and our unique <strong style="color:#87CEEB">
            emoji sentiment engine</strong> that scores conversations as positive, neutral, or negative.
        </div>
        <span class="card-pill">😄 Sentiment Analysis</span>
        <span class="card-pill">📊 Activity Maps</span>
        <span class="card-pill">☁️ Word Cloud</span>
        <span class="card-pill">🔢 Emoji Frequency</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Analyze WhatsApp Chats →", key="btn_wa", use_container_width=True):
        st.switch_page("pages/whatsapp.py")

with col_b:
    st.markdown("""
    <div class="feature-card" style="animation-delay:0.15s">
        <span class="card-icon" style="animation-delay:0.5s">🚗</span>
        <div class="card-title">Car Price Predictor</div>
        <div class="card-desc">
            Get instant second-hand car valuations powered by a
            <strong style="color:#87CEEB">Linear Regression model</strong> trained on real market data.
            Just enter the brand, model, year, fuel type, and kilometres driven.
        </div>
        <span class="card-pill">🏷️ Real-time Valuation</span>
        <span class="card-pill">⛽ Fuel Aware</span>
        <span class="card-pill">📅 Year Adjusted</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Predict Car Price →", key="btn_car", use_container_width=True):
        st.switch_page("pages/car.py")

with col_c:
    st.markdown("""
    <div class="feature-card" style="animation-delay:0.3s">
        <span class="card-icon" style="animation-delay:1s">📈</span>
        <div class="card-title">Stock Forecaster</div>
        <div class="card-desc">
            Forecast 1–4 years of stock prices using
            <strong style="color:#87CEEB">Meta's Prophet time-series model</strong>.
            Visualise historical trends, seasonality decomposition, and future price trajectories
            for 30+ popular stocks.
        </div>
        <span class="card-pill">🔮 Prophet Model</span>
        <span class="card-pill">📅 4-year Forecast</span>
        <span class="card-pill">📉 Trend Decomposition</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Predict Stock Price →", key="btn_stock", use_container_width=True):
        st.switch_page("pages/stock.py")

# ─── How It Works ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-divider" style="margin-top:50px;">
    <div class="section-divider-line"></div>
    <div class="section-divider-text">HOW IT WORKS</div>
    <div class="section-divider-line"></div>
</div>
""", unsafe_allow_html=True)

hw1, hw2, hw3, hw4 = st.columns(4)
steps = [
    (hw1, "01", "🎯", "Choose a Tool", "Select from WhatsApp Analyzer, Car Predictor, or Stock Forecaster."),
    (hw2, "02", "📤", "Upload / Select", "Upload your chat file or choose a car/stock from the dropdowns."),
    (hw3, "03", "🤖", "AI Processes", "Our ML models analyse your data and run predictions in seconds."),
    (hw4, "04", "✨", "Get Insights", "Explore interactive charts, sentiment scores, and accurate predictions."),
]
for col, num, icon, title, desc in steps:
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:24px 12px;animation:fadeInUp 0.7s ease-out;">
            <div style="color:rgba(135,206,235,0.3);font-size:0.75em;font-weight:800;
                        letter-spacing:2px;margin-bottom:8px;">{num}</div>
            <div style="font-size:2.5em;animation:float 3s ease-in-out infinite;
                        animation-delay:{steps.index((col,num,icon,title,desc))*0.3}s">{icon}</div>
            <div style="color:#87CEEB;font-weight:700;font-size:1em;margin:10px 0 6px;">{title}</div>
            <div style="color:#8899bb;font-size:0.85em;line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p>📬 Contact: <a href="mailto:indrasishadhya770@gmail.com" style="color:#87CEEB">indrasishadhya770@gmail.com</a>
    &nbsp;·&nbsp;
    <a href="mailto:dashimadri1412@gmail.com" style="color:#87CEEB">dashimadri1412@gmail.com</a></p>
    <p style="margin-top:8px;">© 2024 PredictXplorer · Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)