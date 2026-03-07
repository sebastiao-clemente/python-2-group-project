"""
🏠 Home – Automated Daily Trading System
Main landing page (Streamlit entry point).
"""

import streamlit as st

# ── Page Configuration (MUST be first Streamlit command) ─────────────
st.set_page_config(
    page_title="AutoTrader | AI-Powered Trading System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.style import inject_custom_css
from utils.config import TICKERS, TEAM_MEMBERS

# ── Inject Theme ─────────────────────────────────────────────────────
inject_custom_css()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ AutoTrader")
    st.markdown("---")
    st.markdown(
        """
        **AI-Powered Daily Trading System**

        Navigate through the pages:
        - 🏠 **Home** – Overview
        - 📈 **Go Live** – Real-time predictions
        - 🧠 **Model Insights** – ML analysis
        - 📊 **Backtesting** – Strategy simulator
        """
    )
    st.markdown("---")

    # API Key input (persists via session state)
    api_key = st.text_input(
        "🔑 SimFin API Key",
        type="password",
        help="Enter your SimFin API key to fetch real market data. Leave empty for demo mode.",
        key="simfin_api_key",
    )

    if api_key:
        st.success("API key configured ✓")
    else:
        st.info("Running in **Demo Mode** with synthetic data.")

    st.markdown("---")
    st.caption("Built with Streamlit · Python · SimFin")


# ── Hero Section ─────────────────────────────────────────────────────
st.markdown("")
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div class="hero-title">AUTOTRADER</div>
        <div class="hero-subtitle">AI-Powered Daily Trading System</div>
        <br>
        <p style="color: #94a3b8; max-width: 700px; margin: 0 auto; font-size: 1.05rem; line-height: 1.7;">
            A machine-learning-driven platform that analyzes historical stock data,
            predicts next-day market movements, and generates actionable trading signals
            — all in real time through an interactive web interface.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# ── Key Stats Banner ─────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies Tracked", f"{len(TICKERS)}")
with col2:
    st.metric("Prediction Type", "Binary")
with col3:
    st.metric("ML Features", "20+")
with col4:
    st.metric("Signal Frequency", "Daily")

st.markdown("")
st.markdown("---")

# ── System Architecture ──────────────────────────────────────────────
st.markdown("## System Architecture")
st.markdown("")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #00d4ff !important;">
                🔬 Part 1 — Data Analytics (Offline)
            </h3>
            <ul style="color: #94a3b8; line-height: 2;">
                <li><strong style="color: #a855f7;">ETL Pipeline</strong> — Extract & transform SimFin bulk data</li>
                <li><strong style="color: #a855f7;">Feature Engineering</strong> — 20+ technical indicators</li>
                <li><strong style="color: #a855f7;">ML Classification</strong> — Predict UP/DOWN movements</li>
                <li><strong style="color: #a855f7;">Model Export</strong> — Serialized .pkl for production</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #00d4ff !important;">
                🌐 Part 2 — Web System (Online)
            </h3>
            <ul style="color: #94a3b8; line-height: 2;">
                <li><strong style="color: #fbbf24;">PySimFin Wrapper</strong> — OOP API client for real-time data</li>
                <li><strong style="color: #fbbf24;">Go Live Dashboard</strong> — Interactive predictions & charts</li>
                <li><strong style="color: #fbbf24;">Backtesting Engine</strong> — Strategy simulation & comparison</li>
                <li><strong style="color: #fbbf24;">Cloud Deployment</strong> — Streamlit Cloud for public access</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ── Data Flow Diagram (Mermaid rendered via Streamlit) ───────────────
with st.expander("📐 View Detailed Data Flow Diagram", expanded=False):
    st.markdown(
        """
        ```
        ┌──────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
        │   SimFin      │     │  Part 1: Analytics    │     │  Part 2: Web App     │
        │   Platform    │     │                      │     │                      │
        │  ┌─────────┐  │     │  ┌───────┐           │     │  ┌──────────┐        │
        │  │  Bulk   ├──┼────►│  │  ETL  ├──►Features│     │  │ PySimFin ├───┐    │
        │  │Download │  │     │  └───────┘    │      │     │  │ Wrapper  │   │    │
        │  └─────────┘  │     │               ▼      │     │  └──────────┘   │    │
        │  ┌─────────┐  │     │  ┌───────┐  ┌────┐  │     │       │         │    │
        │  │   API   ├──┼────►│  │  ML   ├─►│.pkl│──┼────►│  ┌────▼─────┐   │    │
        │  │Endpoint │  │     │  │ Model │  └────┘  │     │  │ Go Live  │   │    │
        │  └─────────┘  │     │  └───────┘          │     │  │Dashboard │   │    │
        └──────────────┘     │  ┌──────────┐       │     │  └──────────┘   │    │
                              │  │ Strategy ├───────┼────►│  ┌──────────┐   │    │
                              │  │ (Bonus) │       │     │  │Backtester│   │    │
                              │  └──────────┘       │     │  └──────────┘   │    │
                              └──────────────────────┘     └──────────────────────┘
        ```
        """,
    )

st.markdown("---")

# ── Companies We Track ───────────────────────────────────────────────
st.markdown("## Companies We Track")
st.markdown("")

ticker_cols = st.columns(len(TICKERS))
for col, (ticker, info) in zip(ticker_cols, TICKERS.items()):
    with col:
        st.markdown(
            f"""
            <div class="feature-box">
                <div class="icon">{info['icon']}</div>
                <h5>{ticker}</h5>
                <p style="color: #94a3b8 !important; font-size: 0.8rem; margin: 0;">{info['name']}</p>
                <p style="color: #a855f7 !important; font-size: 0.7rem; margin: 0;">{info['sector']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
st.markdown("---")

# ── How It Works ─────────────────────────────────────────────────────
st.markdown("## How It Works")
st.markdown("")

step_cols = st.columns(4)
steps = [
    ("1", "📥", "Data Ingestion", "Fetch real-time prices from SimFin via our PySimFin API wrapper"),
    ("2", "🔧", "ETL Processing", "Clean, normalize, and compute 20+ technical features"),
    ("3", "🤖", "ML Prediction", "Classification model predicts next-day price direction"),
    ("4", "📊", "Signal & Action", "Generate BUY / SELL / HOLD signals with confidence scores"),
]

for col, (num, icon, title, desc) in zip(step_cols, steps):
    with col:
        st.markdown(
            f"""
            <div class="glass-card" style="text-align: center; min-height: 200px;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 2rem;
                            color: #00d4ff; text-shadow: 0 0 15px rgba(0, 212, 255, 0.4);">
                    {icon}
                </div>
                <h4 style="font-family: 'Orbitron', sans-serif; color: #e2e8f0 !important;
                           font-size: 0.9rem; margin: 0.8rem 0 0.4rem 0;">
                    Step {num}: {title}
                </h4>
                <p style="color: #94a3b8 !important; font-size: 0.85rem; line-height: 1.5;">
                    {desc}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
st.markdown("---")

# ── Development Team ─────────────────────────────────────────────────
st.markdown("## Development Team")
st.markdown("")

team_cols = st.columns(len(TEAM_MEMBERS))
for col, member in zip(team_cols, TEAM_MEMBERS):
    with col:
        st.markdown(
            f"""
            <div class="team-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👤</div>
                <h4>{member['name']}</h4>
                <div class="role">{member['role']}</div>
                <div class="focus">{member['focus']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
st.markdown("---")

# ── Technology Stack ─────────────────────────────────────────────────
st.markdown("## Technology Stack")
st.markdown("")

tech_cols = st.columns(5)
techs = [
    ("🐍", "Python 3.11", "Core Language"),
    ("📊", "Streamlit", "Web Framework"),
    ("🧠", "Scikit-learn", "ML Library"),
    ("📈", "Plotly", "Visualization"),
    ("☁️", "Streamlit Cloud", "Deployment"),
]

for col, (icon, name, purpose) in zip(tech_cols, techs):
    with col:
        st.markdown(
            f"""
            <div class="feature-box" style="min-height: 120px;">
                <div class="icon">{icon}</div>
                <h5>{name}</h5>
                <p style="color: #94a3b8 !important; font-size: 0.75rem; margin: 0;">{purpose}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
st.markdown("")

# ── Footer ───────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0; border-top: 1px solid #1e293b; margin-top: 2rem;">
        <p style="color: #475569 !important; font-size: 0.8rem;">
            AutoTrader v1.0 · Automated Daily Trading System · Group Assignment 2025
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
