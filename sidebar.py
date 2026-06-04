"""
sidebar.py — Reusable stylish sidebar for PredictXplorer.
Usage: import sidebar; sidebar.render(current_page="home")
"""

import streamlit as st

def render(current_page: str = "home") -> None:
    """
    Render a stylish sidebar with a custom PredictXplorer brand logo and navigation links.
    Utilizes Streamlit's native sidebar navigation styled via CSS to prevent unmounting/flashing.

    Parameters
    ----------
    current_page : str
        Currently active page key (not strictly needed for links now as CSS styles active elements natively,
        but kept for backward compatibility with import calls).
    """

    # Inject CSS style block (absolutely NO leading spaces to prevent markdown code block parsing)
    st.sidebar.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

@keyframes sidebarShimmer {
0% { background-position: -200% center; }
100% { background-position: 200% center; }
}
@keyframes sidebarPulseGlow {
0%, 100% { filter: drop-shadow(0 0 4px rgba(135,206,235,0.3)); }
50% { filter: drop-shadow(0 0 12px rgba(135,206,235,0.7)); }
}

/* Base Sidebar Styling */
[data-testid="stSidebar"] {
background: linear-gradient(180deg, #06060f 0%, #0d1226 50%, #06060f 100%) !important;
border-right: 1px solid rgba(135, 206, 235, 0.15) !important;
box-shadow: 4px 0 32px rgba(0, 0, 0, 0.6) !important;
font-family: 'Inter', sans-serif !important;
}

/* Base layout relative positioning and top padding on the scroll container to accommodate logo */
[data-testid="stSidebar"] > div:not([data-testid="stSidebarCollapsedControl"]),
[data-testid="stSidebar"] div:has(> [data-testid="stSidebarUserContent"]) {
position: relative !important;
padding-top: 100px !important;
}

/* Reset UserContent to be static and avoid duplicate padding */
[data-testid="stSidebarUserContent"] {
position: static !important;
padding-top: 0px !important;
display: flex !important;
flex-direction: column !important;
}

/* Disable positioning on element wrappers to let absolute children position relative to the scroll container */
[data-testid="stSidebarUserContent"] div[data-testid="stElementContainer"],
[data-testid="stSidebarUserContent"] div.element-container,
[data-testid="stSidebarUserContent"] div.stMarkdown,
[data-testid="stSidebarUserContent"] div[data-testid="stMarkdownContainer"] {
position: static !important;
}

.px-sidebar-brand {
position: absolute !important;
top: 15px !important;
left: 10px !important;
right: 10px !important;
height: 55px !important;
z-index: 10000 !important;
display: flex;
align-items: center;
gap: 12px;
text-decoration: none !important;
width: auto !important;
}

.px-sidebar-divider {
position: absolute !important;
top: 75px !important;
left: 10px !important;
right: 10px !important;
height: 1px !important;
z-index: 10000 !important;
background: linear-gradient(90deg, transparent, rgba(135, 206, 235, 0.2), transparent) !important;
width: auto !important;
}

.px-sidebar-logo-icon {
font-size: 2.1em;
line-height: 1;
animation: sidebarPulseGlow 3s ease-in-out infinite;
}
.px-sidebar-logo-text {
display: flex;
flex-direction: column;
justify-content: center;
}
.px-sidebar-brand-title {
font-size: 1.25em;
font-weight: 800;
letter-spacing: -0.5px;
background: linear-gradient(120deg, #87CEEB 0%, #ffffff 40%, #87CEEB 80%);
background-size: 200% auto;
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
animation: sidebarShimmer 6s linear infinite;
line-height: 1.2;
}
.px-sidebar-brand-tagline {
font-size: 0.7em;
color: #8899aa;
text-transform: uppercase;
letter-spacing: 1.5px;
font-weight: 600;
margin-top: 2px;
}

/* Navigation List container */
[data-testid="stSidebarNav"] {
margin-top: 0 !important;
margin-bottom: 20px !important;
padding: 0 !important;
}

/* Hide default navigation title/header if any */
[data-testid="stSidebarNav"] > div:first-child {
display: none !important;
}

[data-testid="stSidebarNav"] ul {
list-style: none !important;
padding: 0 !important;
margin: 0 !important;
display: flex !important;
flex-direction: column !important;
gap: 10px !important;
}
[data-testid="stSidebarNav"] ul li {
padding: 0 !important;
margin: 0 !important;
}

/* Customize links to look like stylish buttons */
[data-testid="stSidebarNav"] ul li a {
display: flex !important;
align-items: center !important;
gap: 12px !important;
padding: 12px 16px !important;
border-radius: 12px !important;
text-decoration: none !important;
border: 1px solid transparent !important;
transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
font-size: 0 !important; /* Hide original text */
background: rgba(255, 255, 255, 0.01) !important;
color: rgba(180, 200, 220, 0.72) !important;
}

/* Hide any inner spans or text elements default to Streamlit */
[data-testid="stSidebarNav"] ul li a span {
display: none !important;
}

/* Inactive button hover state */
[data-testid="stSidebarNav"] ul li a:hover {
color: #87CEEB !important;
background: rgba(135, 206, 235, 0.08) !important;
border-color: rgba(135, 206, 235, 0.2) !important;
transform: translateX(4px) !important;
box-shadow: 0 4px 12px rgba(135, 206, 235, 0.06) !important;
}

/* Active button style rules */
[data-testid="stSidebarNav"] ul li a[class*="active"],
[data-testid="stSidebarNav"] ul li a[aria-current="page"],
[data-testid="stSidebarNav"] ul li a[data-selected="true"] {
background: rgba(135, 206, 235, 0.12) !important;
color: #87CEEB !important;
border-color: rgba(135, 206, 235, 0.35) !important;
font-weight: 600 !important;
box-shadow: 0 4px 20px rgba(135, 206, 235, 0.15) !important;
}
[data-testid="stSidebarNav"] ul li a[class*="active"]:hover,
[data-testid="stSidebarNav"] ul li a[aria-current="page"]:hover,
[data-testid="stSidebarNav"] ul li a[data-selected="true"]:hover {
background: rgba(135, 206, 235, 0.16) !important;
border-color: rgba(135, 206, 235, 0.45) !important;
transform: translateX(4px) !important;
}

/* CSS dynamic pseudo-elements for icon and text replacement */
[data-testid="stSidebarNav"] ul li a::before {
font-size: 0.92rem !important;
font-weight: inherit !important;
color: inherit !important;
display: inline-block !important;
transition: transform 0.25s ease !important;
}
[data-testid="stSidebarNav"] ul li a:hover::before {
transform: scale(1.02) !important;
}

/* Page-specific customization */
[data-testid="stSidebarNav"] ul li a[href="/"]::before,
[data-testid="stSidebarNav"] ul li a[href=""]::before,
[data-testid="stSidebarNav"] ul li a[href="./"]::before,
[data-testid="stSidebarNav"] ul li a:not([href*="whatsapp"]):not([href*="car"]):not([href*="stock"])::before {
content: "🏠  Home" !important;
}
[data-testid="stSidebarNav"] ul li a[href*="whatsapp"]::before {
content: "💬  WhatsApp Analyzer" !important;
}
[data-testid="stSidebarNav"] ul li a[href*="car"]::before {
content: "🚗  Car Price Predictor" !important;
}
[data-testid="stSidebarNav"] ul li a[href*="stock"]::before {
content: "📈  Stock Forecaster" !important;
}

.px-sidebar-footer {
display: flex;
flex-direction: column;
gap: 4px;
padding: 15px 10px 5px 10px;
border-top: 1px solid rgba(135, 206, 235, 0.06);
margin-top: auto !important; /* Push footer to the absolute bottom of flex container */
}
.px-sidebar-version {
font-size: 0.75em;
color: rgba(135, 206, 235, 0.35);
font-weight: 600;
}
.px-sidebar-credit {
font-size: 0.7em;
color: #7f8fa4;
}

/* Selectboxes styling */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > label {
color: #8899aa !important;
font-weight: 600 !important;
font-size: 0.85em !important;
margin-bottom: 6px !important;
letter-spacing: 0.5px;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div {
background-color: rgba(6, 6, 15, 0.6) !important;
border: 1px solid rgba(135, 206, 235, 0.18) !important;
border-radius: 10px !important;
color: white !important;
transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div:hover {
border-color: rgba(135, 206, 235, 0.4) !important;
box-shadow: 0 0 10px rgba(135, 206, 235, 0.1) !important;
}

/* Sidebar action buttons styling */
[data-testid="stSidebar"] div.stButton button {
background: linear-gradient(135deg, rgba(135, 206, 235, 0.15), rgba(135, 206, 235, 0.05)) !important;
color: #87CEEB !important;
font-weight: 600 !important;
border-radius: 10px !important;
border: 1px solid rgba(135, 206, 235, 0.3) !important;
padding: 8px 16px !important;
transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
margin-top: 10px !important;
text-align: center !important;
justify-content: center !important;
}
[data-testid="stSidebar"] div.stButton button:hover {
background: linear-gradient(135deg, #87CEEB, #5ba8cc) !important;
color: #06060f !important;
box-shadow: 0 8px 25px rgba(135, 206, 235, 0.35) !important;
border-color: transparent !important;
transform: translateY(-2px) !important;
}
</style>""", unsafe_allow_html=True)

    # Render Brand Logo
    st.sidebar.markdown("""<div class="px-sidebar-brand">
<span class="px-sidebar-logo-icon">🔮</span>
<div class="px-sidebar-logo-text">
<span class="px-sidebar-brand-title">PredictXplorer</span>
<span class="px-sidebar-brand-tagline">AI Prediction Suite</span>
</div>
</div>""", unsafe_allow_html=True)

    # Render Divider
    st.sidebar.markdown("""<div class="px-sidebar-divider"></div>""", unsafe_allow_html=True)

    # Render Footer
    st.sidebar.markdown("""<div class="px-sidebar-footer">
<div class="px-sidebar-version">v1.2.0</div>
<div class="px-sidebar-credit">Built with ❤️ in Python</div>
</div>""", unsafe_allow_html=True)
