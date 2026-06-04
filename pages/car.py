import streamlit as st
import pandas as pd
import pickle
import sidebar

# Render Custom Sidebar
sidebar.render(current_page="car")

# ─── Animations & CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

@keyframes fadeInUp   { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes float      { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
@keyframes shimmer    { 0%{background-position:-200% center} 100%{background-position:200% center} }
@keyframes pulseGlow  { 0%,100%{box-shadow:0 0 5px rgba(135,206,235,.3)} 50%{box-shadow:0 0 25px rgba(135,206,235,.8)} }
@keyframes borderGlow { 0%,100%{border-color:rgba(135,206,235,.2)} 50%{border-color:rgba(135,206,235,.7)} }
@keyframes resultPop  { 0%{opacity:0;transform:scale(.7) rotate(-3deg)} 80%{transform:scale(1.05)} 100%{opacity:1;transform:scale(1)} }

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
    margin-bottom: 8px;
}

.form-card {
    background: linear-gradient(135deg, #0d1b2e, #111827);
    border: 1px solid rgba(135,206,235,.2);
    border-radius: 20px;
    padding: 32px;
    animation: fadeInUp .7s ease-out, borderGlow 4s ease-in-out infinite;
    margin: 16px 0;
}

.result-card {
    background: linear-gradient(135deg, #0a2e0a, #0d3d0d);
    border: 2px solid #2ecc71;
    border-radius: 20px;
    padding: 28px;
    text-align: center;
    animation: resultPop .6s cubic-bezier(.175,.885,.32,1.275);
    margin: 16px 0;
}
.result-price {
    font-size: 3em;
    font-weight: 800;
    color: #2ecc71;
    animation: shimmer 2s linear infinite;
    background: linear-gradient(135deg,#2ecc71,#7fff7f,#2ecc71);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.result-label { color: #8899bb; font-size: 0.95em; margin-top: 4px; }

.car-icon { font-size: 4em; animation: float 3s ease-in-out infinite; display: block; text-align: center; }

[data-testid="stSelectbox"] > div { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown('<span class="car-icon">🚗</span>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Car Price Predictor</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8899bb;margin-bottom:24px;'>Get an instant AI-powered second-hand car valuation</p>",
            unsafe_allow_html=True)

# ─── Load Data & Model ────────────────────────────────────────────────────────
car = pd.read_csv("refine_car.csv")
model = pickle.load(open("LinearRegressionModel.pkl", "rb"))

companies = sorted(car["company"].unique())

def get_car_models(company):
    return sorted(car[car["company"] == company]["name"].unique())

year_list = sorted(car["year"].unique(), reverse=True)
fuel_types = car["fuel_type"].unique()

# ─── Form Card ────────────────────────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)

fc1, fc2 = st.columns(2)
with fc1:
    selected_company = st.selectbox("🏭 Car Company", companies)
    selected_year = st.selectbox("📅 Year of Manufacture", year_list)
    selected_fuel_type = st.selectbox("⛽ Fuel Type", fuel_types)

with fc2:
    selected_car_model = st.selectbox("🚙 Car Model",
                                       get_car_models(selected_company))
    selected_kms_driven = st.number_input("🛣️ Kilometres Driven",
                                           min_value=0, step=1000,
                                           help="Enter the total km driven")

st.markdown('</div>', unsafe_allow_html=True)

# ─── Predict Button ───────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([2, 1.5, 2])
with btn_col:
    predict_button = st.button("🔮 Predict Price", use_container_width=True)

if predict_button:
    try:
        input_data = pd.DataFrame(
            [[selected_car_model, selected_company, selected_year,
              selected_kms_driven, selected_fuel_type]],
            columns=["name", "company", "year", "kms_driven", "fuel_type"],
            dtype="object",
        )
        prediction = model.predict(input_data)
        predicted_price = round(float(prediction[0]))

        if predicted_price <= 0:
            st.warning("⚠️ No matching car data found for this combination. Try different inputs.")
        else:
            # Animated result card
            st.markdown(f"""
            <div class="result-card">
                <div style="font-size:2.5em;margin-bottom:8px;animation:float 2s ease-in-out infinite">🎯</div>
                <div class="result-label">Estimated Market Value</div>
                <div class="result-price">₹{predicted_price:,}</div>
                <div class="result-label" style="margin-top:12px;">
                    {selected_company} {selected_car_model} · {selected_year} · {selected_fuel_type} · {selected_kms_driven:,} km
                </div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Prediction error: {e}")