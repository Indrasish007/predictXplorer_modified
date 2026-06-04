"""
navbar.py — Reusable fixed navbar for PredictXplorer.
Usage: import navbar; navbar.render(current_page="home")

Pages map to Streamlit's auto-generated URLs:
  app.py              → /
  pages/whatsapp.py   → /whatsapp
  pages/car.py        → /car
  pages/stock.py      → /stock
"""

import streamlit as st

# (key, url_path, emoji, display_label)
_NAV_ITEMS = [
    ("home",     "/",          "🏠", "Home"),
    ("whatsapp", "/whatsapp",  "💬", "WhatsApp"),
    ("car",      "/car",       "🚗", "Car Price"),
    ("stock",    "/stock",     "📈", "Stocks"),
]


def render(current_page: str = "home") -> None:
    """
    Render a fixed glassmorphism navbar at the top of every page.

    Parameters
    ----------
    current_page : str
        One of "home" | "whatsapp" | "car" | "stock"
        The matching link will be highlighted as active.
    """

    # Build nav links HTML
    links_html = ""
    for key, href, icon, label in _NAV_ITEMS:
        active_cls = "nav-active" if key == current_page else ""
        links_html += (
            f'<a href="{href}" target="_top" class="nav-link {active_cls}">'
            f'<span class="nav-icon">{icon}</span>'
            f'<span class="nav-label">{label}</span>'
            f'</a>'
        )

    st.markdown(f"""
<style>
/* ── Fonts ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Keyframes ──────────────────────────────────────────────── */
@keyframes navSlideDown {{
    from {{ opacity: 0; transform: translateY(-100%); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes brandShimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}
@keyframes activePulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(135,206,235,0); }}
    50%       {{ box-shadow: 0 0 12px 2px rgba(135,206,235,0.3); }}
}}

/* ── Navbar shell ──────────────────────────────────────────── */
.px-navbar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999999;
    height: 66px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 48px 0 76px;
    background: rgba(6, 6, 15, 0.88);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    border-bottom: 1px solid rgba(135, 206, 235, 0.13);
    box-shadow: 0 4px 48px rgba(0, 0, 0, 0.55),
                0 1px 0 rgba(135, 206, 235, 0.06);
    font-family: 'Inter', sans-serif;
    animation: navSlideDown 0.5s cubic-bezier(0.16,1,0.3,1) both;
}}

/* ── Brand / Logo ──────────────────────────────────────────── */
.px-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    flex-shrink: 0;
}}
.px-brand-crystal {{
    font-size: 1.6em;
    line-height: 1;
    filter: drop-shadow(0 0 8px rgba(135,206,235,0.6));
    transition: transform 0.3s ease;
}}
.px-brand:hover .px-brand-crystal {{ transform: rotate(15deg) scale(1.15); }}
.px-brand-text {{
    font-size: 1.22em;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(120deg, #87CEEB 0%, #ffffff 45%, #87CEEB 80%);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: brandShimmer 5s linear infinite;
}}

/* ── Nav links group ───────────────────────────────────────── */
.px-nav-links {{
    display: flex;
    align-items: center;
    gap: 2px;
}}

/* ── Individual link ───────────────────────────────────────── */
.nav-link {{
    display: flex;
    align-items: center;
    gap: 7px;
    color: rgba(180, 200, 220, 0.75);
    text-decoration: none !important;
    font-size: 0.88em;
    font-weight: 500;
    padding: 9px 18px;
    border-radius: 10px;
    border: 1px solid transparent;
    transition: color 0.22s ease,
                background 0.22s ease,
                border-color 0.22s ease,
                transform 0.22s ease,
                box-shadow 0.22s ease;
    white-space: nowrap;
}}
.nav-link:hover {{
    color: #87CEEB !important;
    background: rgba(135, 206, 235, 0.09);
    border-color: rgba(135, 206, 235, 0.22);
    transform: translateY(-2px);
    text-decoration: none !important;
    box-shadow: 0 4px 16px rgba(135, 206, 235, 0.12);
}}
.nav-link:active {{ transform: translateY(0); }}

/* ── Active (current page) ─────────────────────────────────── */
.nav-active {{
    color: #87CEEB !important;
    background: rgba(135, 206, 235, 0.13) !important;
    border-color: rgba(135, 206, 235, 0.38) !important;
    font-weight: 600 !important;
    animation: activePulse 3s ease-in-out infinite;
}}
.nav-active .nav-icon {{ filter: drop-shadow(0 0 6px rgba(135,206,235,0.7)); }}

/* ── Icon ──────────────────────────────────────────────────── */
.nav-icon  {{ font-size: 1.05em; line-height: 1; }}
.nav-label {{ letter-spacing: 0.1px; }}

/* ── Divider dot ───────────────────────────────────────────── */
.nav-dot {{
    width: 4px; height: 4px;
    border-radius: 50%;
    background: rgba(135,206,235,0.25);
    margin: 0 6px;
    flex-shrink: 0;
}}

/* ═══════════════════════════════════════════════════════════
   Global overrides — apply to the entire page
   ═══════════════════════════════════════════════════════════ */

/* Push all page content below the fixed navbar and center content container */
.main .block-container,
[data-testid="stBlockContainer"] {{
    padding-top: 90px !important;
    max-width: 1200px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    float: none !important;
}}

/* Hide Streamlit's own top header bar */
header[data-testid="stHeader"]        {{ display: none !important; }}
[data-testid="stDecoration"]          {{ display: none !important; }}
[data-testid="stToolbar"]             {{ display: none !important; }}
#MainMenu                              {{ display: none !important; }}
footer                                 {{ display: none !important; }}

/* Remove default Streamlit top padding */
[data-testid="stAppViewContainer"] > section:first-child {{
    padding-top: 0 !important;
}}

/* ── Sidebar toggle: visually embedded in the left of the navbar ── */

/* Collapsed-state arrow/chevron button — placed inside the navbar */
[data-testid="stSidebarCollapsedControl"] {{
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 66px !important;
    height: 66px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 10000001 !important;
    background: transparent !important;
    border-right: 1px solid rgba(135,206,235,0.13) !important;
}}

/* Style the button itself to match the navbar */
[data-testid="stSidebarCollapsedControl"] button {{
    background: transparent !important;
    border: 1px solid rgba(135,206,235,0.25) !important;
    border-radius: 10px !important;
    color: rgba(135,206,235,0.85) !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: all 0.22s ease !important;
    font-size: 1.1em !important;
}}
[data-testid="stSidebarCollapsedControl"] button:hover {{
    background: rgba(135,206,235,0.12) !important;
    border-color: rgba(135,206,235,0.6) !important;
    box-shadow: 0 0 14px rgba(135,206,235,0.25) !important;
    color: #87CEEB !important;
}}

/* SVG icon inside the button */
[data-testid="stSidebarCollapsedControl"] button svg {{
    fill: rgba(135,206,235,0.85) !important;
    width: 18px !important;
    height: 18px !important;
}}
[data-testid="stSidebarCollapsedControl"] button:hover svg {{
    fill: #87CEEB !important;
}}

/* Open sidebar panel: start below the navbar */
[data-testid="stSidebar"] {{
    top: 66px !important;
    height: calc(100vh - 66px) !important;
    z-index: 9999998 !important;
}}

/* Collapse button INSIDE the open sidebar: also aligned with navbar top */
[data-testid="stSidebarHeader"] {{
    position: sticky !important;
    top: 0 !important;
    z-index: 10000000 !important;
}}
</style>

<nav class="px-navbar">
  <a href="/" target="_top" class="px-brand">
    <span class="px-brand-crystal">🔮</span>
    <span class="px-brand-text">PredictXplorer</span>
  </a>
  <div class="px-nav-links">
    {links_html}
  </div>
</nav>
""", unsafe_allow_html=True)
