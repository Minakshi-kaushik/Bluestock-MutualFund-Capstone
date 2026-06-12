# ==============================================================================
# BLUESTOCK FINTECH: PREMIUM PRO-TERMINAL DASHBOARD ENGINE (FINAL PRODUCTION)
# ==============================================================================

import os
import sqlite3
import traceback
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

# 1. Page Configuration Setup (True Edge-to-Edge Desktop Layout)
st.set_page_config(
    page_title="bluestock capstone project",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# 2. Premium Institutional UI Layout Overrides
st.markdown(
    """
    <style>
        /* Import Web Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@700;800&display=swap');

        /* Global Structural Overrides */
        .main { background-color: #0f1420 !important; color: #d7dce6 !important; font-family: 'Inter', sans-serif !important; padding-top: 0rem !important; }
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0f1420 !important;
            width: 100% !important;
            max-width: none !important;
        }
        header, header * { background-color: #0f1420 !important; }
        section[data-testid="stSidebar"] { background-color: #111827 !important; }
        div[data-testid="stBlock"] { padding: 0px !important; margin: 0px !important; }
        .block-container {
            max-width: none !important;
            width: 100% !important;
            padding: 0 24px 72px 24px !important;
        }
        [data-testid="stVerticalBlock"] {
            width: 100% !important;
            max-width: none !important;
        }
        [data-testid="stHorizontalBlock"] {
            gap: 1.35rem !important;
        }
        
        /* Executive Terminal Header */
        .tv-header {
            background-color: #161d2d;
            border-bottom: 1px solid #2d3648;
            min-height: 112px;
            padding: 34px 44px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 0 -24px 28px -24px;
            box-shadow: 0 14px 30px rgba(0,0,0,0.28);
        }
        .tv-brand {
            font-family: 'Manrope', sans-serif;
            font-size: 32px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.5px;
        }
        .tv-context {
            color: #9aa4b5;
            font-size: 17px;
            font-weight: 700;
            letter-spacing: 0.8px;
            margin-left: 22px;
        }
        .tv-status-group { display: flex; gap: 28px; align-items: center; }
        .tv-engine { font-size: 16px; color: #9aa4b5; font-weight: 700; }
        .tv-market-status {
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            color: #38c7b4;
            font-weight: 700;
            background: rgba(56, 199, 180, 0.10);
            padding: 10px 18px;
            border-radius: 6px;
            border: 1px solid rgba(56, 199, 180, 0.32);
        }
        
        /* Static Institutional Title System */
        .platform-title-container {
            text-align: center;
            margin: 10px auto 36px auto;
            padding: 0 32px;
            max-width: none;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .platform-brand-title {
            font-family: 'Manrope', sans-serif;
            font-size: 72px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0;
            line-height: 1.05;
            margin: 0 0 24px 0;
            text-transform: uppercase;
            animation: titleFadeUp 0.75s ease-out both;
        }
        .platform-fund-title {
            font-family: 'Manrope', sans-serif;
            font-size: 44px;
            font-weight: 800;
            color: #e6edf7;
            line-height: 1.16;
            margin: 0 auto 18px auto;
            max-width: 1480px;
            width: 100%;
            text-align: center;
            animation: titleFadeUp 0.85s ease-out 0.14s both;
        }
        .platform-sub-heading {
            font-family: 'Inter', sans-serif;
            font-size: 26px;
            color: #4fc3f7;
            font-weight: 700;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            margin: 0;
            animation: titleFadeUp 0.95s ease-out 0.28s both;
        }
        @keyframes titleFadeUp {
            from {
                opacity: 0;
                transform: translateY(18px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Atomic KPI Card System */
        .metric-card {
            height: 260px;
            min-height: 260px;
            width: 100%;
            background-color: #1a2335;
            border: 1px solid #303a4d;
            border-radius: 8px;
            padding: 30px 26px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 18px;
            text-align: center;
            overflow: hidden;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 10px 24px rgba(0,0,0,0.22);
        }
        .metric-card.regression-card {
            max-width: 680px;
            margin: 20px auto 48px auto;
            height: 250px;
            min-height: 250px;
        }
        .metric-label {
            font-family: 'Manrope', sans-serif;
            font-size: 24px;
            color: #a4adbc;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 1px;
            margin: 0;
            line-height: 1.25;
        }
        
        /* Metric Typography Scaling */
        .metric-value { font-family: 'Manrope', sans-serif; font-size: 70px; font-weight: 800; line-height: 1; margin: 0; }
        .metric-value.score { color: #38c7b4; }
        .metric-value.cagr { color: #4fc3f7; }
        .metric-value.sharpe { color: #f4c542; }
        .metric-value.drawdown { color: #f05d5e; }
        .metric-unit { font-size: 28px; color: #9aa4b5; }
        .metric-secondary {
            font-family: 'Manrope', sans-serif;
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            line-height: 1.35;
        }
        
        /* Premium Analytics Sections */
        .analytics-card {
            background-color: #151c2b;
            border: 1px solid #2d3648;
            border-radius: 8px;
            padding: 56px 56px 46px 56px;
            margin: 70px auto 24px auto;
            box-shadow: 0 18px 42px rgba(0,0,0,0.34);
            text-align: center;
            width: 100%;
        }
        .section-header {
            font-family: 'Manrope', sans-serif;
            font-size: 54px;
            font-weight: 800;
            color: #ffffff;
            margin: 0 0 14px 0;
            text-transform: uppercase;
            letter-spacing: 0;
            line-height: 1.1;
            text-align: center;
        }
        .section-subheader {
            font-family: 'Inter', sans-serif;
            font-size: 22px;
            font-weight: 500;
            color: #a8b0bf;
            margin: 0 0 34px 0;
            line-height: 1.35;
            text-align: center;
        }
        
        /* Target Symbol Inputs Selector Formatting */
        .stSelectbox { margin-bottom: 52px !important; }
        .stSelectbox div[data-baseweb="select"] {
            background-color: #1a2335 !important;
            border: 1px solid #3b465b !important;
            color: #ffffff !important;
            min-height: 82px !important;
            border-radius: 8px !important;
            font-size: 22px !important;
        }
        .stSelectbox label {
            color: #dce5f2 !important;
            font-size: 24px !important;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 16px;
        }
        .stSelectbox div[data-baseweb="select"] span,
        .stSelectbox div[data-baseweb="select"] input {
            font-size: 22px !important;
            line-height: 1.35 !important;
        }
        div[role="listbox"] li,
        div[role="option"] {
            font-size: 21px !important;
            line-height: 1.35 !important;
        }
        
        /* Safe dataframe frame only. Do not style internal Streamlit grid nodes. */
        [data-testid="stDataFrame"] {
            width: 100% !important;
            border: 1px solid #2d3648;
            border-radius: 8px;
            background: #ffffff;
            overflow: hidden;
            box-shadow: 0 18px 42px rgba(0,0,0,0.30);
        }
        [data-testid="stDataFrame"] > div {
            width: 100% !important;
        }
        [data-testid="stDataFrame"] [role="columnheader"] {
            font-size: 26px !important;
            font-weight: 800 !important;
        }
        [data-testid="stDataFrame"] [role="gridcell"] {
            font-size: 23px !important;
            padding: 12px 16px !important;
        }
        hr { border-color: #2d3648 !important; margin: 42px 0px !important; }

        /* ========================================================================= */
        /* DAY 6 RISK COLORS */
        /* ========================================================================= */
        .risk-danger {
            color: #ff6b6b !important;
        }
        .risk-warning {
            color: #f9c74f !important;
        }
        .risk-success {
            color: #4fd1c5 !important;
        }

        @media (max-width: 1100px) {
            .platform-brand-title { font-size: 56px; }
            .platform-fund-title { font-size: 34px; }
            .platform-sub-heading { font-size: 20px; }
            .tv-header { flex-direction: column; align-items: flex-start; gap: 18px; }
            .metric-card { min-height: 220px; margin-bottom: 18px; }
            .section-header { font-size: 34px; }
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Dynamic Relative Project Path Router
# ==============================================================================
# STREAMLIT CLOUD DEPLOYMENT PATHS
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "bluestock_mf.db"

SCORECARD_PATH = BASE_DIR / "data" / "processed" / "fund_scorecard.csv"

RISK_CSV_PATH = BASE_DIR / "data" / "processed" / "advanced_risk_metrics.csv"

required_files = [DB_PATH, SCORECARD_PATH]

for file in required_files:
    if not file.exists():
        st.error(f"Missing required file: {file}")
        st.stop()

# 4. Data Gathering Pipelines


@st.cache_data(show_spinner=False)
def load_all_system_data(db_path, csv_path):
    nav_matrix, df_scorecard, df_meta = None, None, None
    if db_path.exists():
        try:
            with sqlite3.connect(db_path) as conn:
                query = "SELECT n.date_id as Date, f.scheme_name as Scheme, n.nav as NAV FROM fact_nav n INNER JOIN dim_fund f ON n.amfi_code = f.amfi_code;"
                df = pd.read_sql_query(query, conn)
                nav_matrix = (
                    df.pivot(index="Date", columns="Scheme", values="NAV")
                    .ffill()
                    .bfill()
                )
                df_meta = pd.read_sql_query(
                    "SELECT amfi_code as [AMFI Code], scheme_name as [Scheme Name], plan as [Type], category as [Category] FROM dim_fund;",
                    conn,
                )
        except Exception as e:
            st.error(f"Database loading error: {e}")
            st.code(traceback.format_exc())
    if csv_path.exists():
        df_scorecard = pd.read_csv(csv_path)
    else:
        st.error(f"Missing scorecard file: {csv_path}")
    return nav_matrix, df_scorecard, df_meta


nav_matrix, df_score, df_meta = load_all_system_data(DB_PATH, SCORECARD_PATH)


# ==============================================================================
# DAY 6 RISK DATA LOAD
# ==============================================================================
df_risk = None

try:
    if RISK_CSV_PATH.exists():
        df_risk = pd.read_csv(RISK_CSV_PATH)

except Exception as e:
    st.error(f"Risk metrics loading error: {e}")
# ==============================================================================
# TRADINGVIEW BANNER HUD
# ==============================================================================
st.markdown(
    """
    <div class="tv-header">
        <div>
            <span class="tv-brand">BLUESTOCK FINTECH</span>
            <span class="tv-context">INSTITUTIONAL ANALYTICS CONSOLE</span>
        </div>
        <div class="tv-status-group">
            <span class="tv-engine">ENGINE <strong style="color:#ffffff;">SQLITE V3</strong></span>
            <span class="tv-market-status">SYSTEM DATA OPERATIONAL</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

if df_score is not None and nav_matrix is not None:
    # ==============================================================================
    # STATIC INSTITUTIONAL TITLE SYSTEM
    # ==============================================================================
    sel_col1, sel_col2, sel_col3 = st.columns([1, 2, 1])
    with sel_col2:
        selected_fund = st.selectbox(
            "Select Primary Analysis Tracker", df_score["Fund Name"].unique()
        )

    fund_data = df_score[df_score["Fund Name"] == selected_fund].iloc[0]

    # ==============================================================================
    # SELECTED FUND RISK METRICS
    # ==============================================================================
    selected_risk = None
    if df_risk is not None and not df_risk.empty:
        risk_match = df_risk[df_risk["Fund Name"] == selected_fund]
        if not risk_match.empty:
            selected_risk = risk_match.iloc[0]

    # Splitting the string to print "BlueStock Fintech: Scheme Name" dynamically
    clean_scheme_title = selected_fund.split(" - ")[0]

    st.markdown(
        f"""
        <div class="platform-title-container">
            <h1 class="platform-brand-title">BLUESTOCK FINTECH</h1>
            <h2 class="platform-fund-title">{clean_scheme_title}</h2>
            <p class="platform-sub-heading">Performance & Risk Analytics Dashboard</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # ==============================================================================
    # KPI ANALYTICS CARD SYSTEM
    # ==============================================================================
    hud_col1, hud_col2, hud_col3, hud_col4 = st.columns(4)

    with hud_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Composite Rating Score</div>
                <div class="metric-value score">{fund_data["Fund Score"]:.1f}<span class="metric-unit"> / 100</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hud_col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Geometric 3-Year CAGR</div>
                <div class="metric-value cagr">{fund_data["3Yr CAGR"] * 100:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hud_col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Sharpe Volatility Ratio</div>
                <div class="metric-value sharpe">{fund_data["Sharpe Ratio"]:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hud_col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Max Historical Drawdown</div>
                <div class="metric-value drawdown">{fund_data["Max Drawdown"] * 100:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="metric-card regression-card">
            <div class="metric-label">Regression Coefficients</div>
            <div class="metric-secondary">Alpha: <span style="color:#38c7b4;">{fund_data["Alpha"]:.4f}</span></div>
            <div class="metric-secondary">Beta: <span style="color:#f4c542;">{fund_data["Beta"]:.2f}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==============================================================================
    # PHASE 4 : ADVANCED RISK ANALYTICS
    # ==============================================================================
    if selected_risk is not None:
        st.markdown(
            """
            <div class="analytics-card" style="margin-top: 20px; margin-bottom: 20px;">
                <p class="section-header">PHASE 4 : ADVANCED RISK ANALYTICS</p>
                <p class="section-subheader">Tail-risk limits and historical volatility sensitivities calculated for the active tracker.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">DAILY VAR (95%)</div>
                    <div class="metric-value risk-danger">{selected_risk["Daily VaR 95%"]:.4%}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">DAILY CVAR (95%)</div>
                    <div class="metric-value risk-danger">{selected_risk["Daily CVaR 95%"]:.4%}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">LIFETIME BETA</div>
                    <div class="metric-value risk-warning">{selected_risk["Lifetime Beta"]:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">60 DAY ROLLING BETA</div>
                    <div class="metric-value risk-success">{selected_risk["Latest 60_Day Rolling Beta"]:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

    # ==============================================================================
    # MASSIVE TRADINGVIEW DARK CHART FOOTPRINT (650px EXPANSIVE VERTICAL SCALE)
    # ==============================================================================
    fig = go.Figure()
    top_5 = df_score.head(5)["Fund Name"].tolist()
    if selected_fund not in top_5:
        top_5.append(selected_fund)

    for scheme in top_5:
        if scheme in nav_matrix.columns:
            norm_path = (nav_matrix[scheme] / nav_matrix[scheme].iloc[0]) * 100
            is_target = scheme == selected_fund

            fig.add_trace(
                go.Scatter(
                    x=nav_matrix.index,
                    y=norm_path,
                    mode="lines",
                    name=scheme.split(" - ")[0][:35],
                    line=dict(
                        width=6.5 if is_target else 2.0,
                        color="#38c7b4" if is_target else "#6f7d92",
                    ),
                    opacity=1.0 if is_target else 0.20,
                )
            )

    # Add peak value annotation point for clarity
    target_norm_series = (
        nav_matrix[selected_fund] / nav_matrix[selected_fund].iloc[0]
    ) * 100
    peak_date = target_norm_series.idxmax()
    peak_val = target_norm_series.max()

    fig.add_annotation(
        x=peak_date,
        y=peak_val,
        text=f"Peak: {peak_val:.1f} pts",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#38c7b4",
        bgcolor="#161d2d",
        font=dict(color="#ffffff", size=18, family="Inter"),
        bordercolor="#2d3648",
        borderwidth=1,
        borderpad=8,
        ay=-60,
    )

    # Restored to beautiful, authentic TradingView dark mode charting background
    fig.update_layout(
        paper_bgcolor="#0f1420",
        plot_bgcolor="#0f1420",
        margin=dict(l=44, r=104, t=56, b=64),
        height=950,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(color="#b1bac9", size=20),
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#161d2d",
            bordercolor="#38445a",
            font=dict(color="#ffffff", size=19, family="Inter"),
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#283244",
            linecolor="#38445a",
            tickfont=dict(color="#a7b0c0", size=19),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#283244",
            linecolor="#38445a",
            tickfont=dict(color="#a7b0c0", size=19),
            side="right",
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ==============================================================================
    # SEQUENTIAL STACKED DATA TABLES LAYER (HIGH READABILITY STARK WHITE BACKGROUNDS)
    # ==============================================================================

    # Screener 1
    st.markdown(
        """
        <div class="analytics-card">
            <p class="section-header">Phase 1: Risk-Adjusted Performance Evaluation</p>
            <p class="section-subheader">Fund ranking matrix across return efficiency, volatility discipline, alpha generation, and drawdown control.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    clean_score = df_score[
        [
            "Fund Name",
            "3Yr CAGR",
            "Sharpe Ratio",
            "Sortino Ratio",
            "Alpha",
            "Beta",
            "Max Drawdown",
            "Fund Score",
        ]
    ].copy()
    clean_score["3Yr CAGR"] = (clean_score["3Yr CAGR"] * 100).map("{:,.2f}%".format)
    clean_score["Max Drawdown"] = (clean_score["Max Drawdown"] * 100).map(
        "{:,.2f}%".format
    )
    clean_score["Alpha"] = clean_score["Alpha"].map("{:,.4f}".format)
    clean_score["Beta"] = clean_score["Beta"].map("{:,.2f}".format)
    clean_score["Fund Score"] = clean_score["Fund Score"].map("{:,.1f}".format)
    st.dataframe(clean_score, use_container_width=True, height=620, row_height=64)

    # Screener 2
    st.markdown(
        """
        <div class="analytics-card">
            <p class="section-header">Phase 2: Historical NAV Timeline</p>
            <p class="section-subheader">Continuous normalized asset value history for all tracked schemes in the analysis universe.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    raw_nav_preview = nav_matrix.reset_index().sort_values(by="Date", ascending=False)
    st.dataframe(raw_nav_preview, use_container_width=True, height=680, row_height=64)

    # Screener 3
    st.markdown(
        """
        <div class="analytics-card">
            <p class="section-header">Phase 3: Master Data Ledger</p>
            <p class="section-subheader">Relational fund metadata sourced from dim_fund, including AMFI identity, scheme name, plan, and category.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if df_meta is not None:
        st.dataframe(df_meta, use_container_width=True, height=620, row_height=64)
    else:
        st.info("Relational database link unpopulated.")

    # ==============================================================================
    # ADVANCED RISK MATRIX TABLE
    # ==============================================================================
    if df_risk is not None and not df_risk.empty:
        st.markdown(
            """
            <div class="analytics-card">
                <p class="section-header">ADVANCED RISK MATRIX</p>
                <p class="section-subheader">Institutional tail-risk matrix mapping Value at Risk, Expected Shortfall, and systemic window indicators.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_risk = df_risk.copy()
        render_risk["Daily VaR 95%"] = (render_risk["Daily VaR 95%"] * 100).map(
            "{:,.3f}%".format
        )
        render_risk["Daily CVaR 95%"] = (render_risk["Daily CVaR 95%"] * 100).map(
            "{:,.3f}%".format
        )
        render_risk["Lifetime Beta"] = render_risk["Lifetime Beta"].map(
            "{:,.2f}".format
        )
        render_risk["Latest 60_Day Rolling Beta"] = render_risk[
            "Latest 60_Day Rolling Beta"
        ].map("{:,.2f}".format)

        st.dataframe(render_risk, use_container_width=True, height=550)

else:
    st.error(
        "System Initialization Interrupted. Ensure 'bluestock_mf.db' and 'data/processed/fund_scorecard.csv' are present."
    )
