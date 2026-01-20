# app.py - Dashboard Macroéconomique Mauritanie - Version Finale Interactive
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# -----------------------------
# CONFIGURATION PAGE
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CSS ULTRA-MODERNE AVEC ANIMATIONS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
* {
font-family: 'Inter', sans-serif;
}
/* Fond principal avec gradient animé */
.main {
background: linear-gradient(-45deg, #f8fafc, #e0f2fe, #dbeafe, #f1f5f9);
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
0% { background-position: 0% 50%; }
50% { background-position: 100% 50%; }
100% { background-position: 0% 50%; }
}
/* Sidebar moderne */
[data-testid="stSidebar"] {
background: linear-gradient(180deg, #0B3C5D 0%, #1F77B4 100%);
border-right: 3px solid #87CEEB;
}
[data-testid="stSidebar"] * {
color: white !important;
}
/* Hero Header - Titres en BLANC */
.hero-title {
color: white !important;
font-size: 3.5rem;
font-weight: 900;
margin: 0;
text-shadow: 0 4px 12px rgba(0,0,0,0.3);
letter-spacing: -2px;
}
/* Section headers avec icônes SVG */
.section-header {
display: flex;
align-items: center;
gap: 12px;
margin: 24px 0;
}
.section-icon svg {
width: 28px;
height: 28px;
filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}
/* Charts interactifs */
.stPlotlyChart {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 28px;
padding: 32px;
box-shadow:
0 8px 32px rgba(0,0,0,0.08),
0 2px 8px rgba(0,0,0,0.04);
transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
border: 1px solid rgba(226, 232, 240, 0.8);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
    df["Année"] = df["Année"].astype(int)
    df = df.groupby("Année", as_index=False).first()
    df = df.sort_values("Année").reset_index(drop=True)
    
    # Imputation
    df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"] = df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"].interpolate()
    df.loc[df["Année"] >= 1986, "Inflation_pct"] = df.loc[df["Année"] >= 1986, "Inflation_pct"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"].interpolate()
    df.loc[df["Année"] >= 1975, "Envois_de_fonds_pct_PIB"] = df.loc[df["Année"] >= 1975, "Envois_de_fonds_pct_PIB"].interpolate(limit=4).fillna(df["Envois_de_fonds_pct_PIB"].mean())
    df.loc[df["Année"] >= 1970, "Dette_exterieure_USD"] = df.loc[df["Année"] >= 1970, "Dette_exterieure_USD"].interpolate()
    df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"] = df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"].fillna(df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"].mean())
    df.loc[(df["Année"] >= 1963) & (df["Année"] <= 2021), "Reserves_internationales_USD"] = df.loc[(df["Année"] >= 1963) & (df["Année"] <= 2021), "Reserves_internationales_USD"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].fillna(df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].mean())
    return df

df = load_and_clean_data()

# Couleurs
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg'
    width='120' style='border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);'/>
    <h1 class="hero-title">Dashboard<br/>Mauritanie</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Icône de navigation "hamburger"
    st.markdown('''
    <div style="font-size: 18px; font-weight: 700; margin-bottom: 20px; color: white;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 12H21M3 6H21M3 18H21" stroke="white" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Navigation
    </div>
    ''', unsafe_allow_html=True)
    
    page = st.radio(
        "",
        ["🏠 Vue d'ensemble",
         "📈 Croissance & Inflation",
         "🌍 Secteur Externe",
         "💰 Finances Publiques",
         "📊 Analyses Avancées"],
        label_visibility="collapsed"
    )

# Filtres temporels
year_range = st.sidebar.slider("Période d'analyse", int(df["Année"].min()), int(df["Année"].max()), (2000, 2024))
df_filtered = df[(df["Année"] >= year_range[0]) & (df["Année"] <= year_range[1])].copy()

# =====================================
# PAGE 1: VUE D'ENSEMBLE
# =====================================
if page == "🏠 Vue d'ensemble":
    st.markdown(f"""
    <div class="hero-header" style='background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; padding: 48px; margin-bottom: 40px;'>
    <h1 class="hero-title">Dashboard Macroéconomique</h1>
    <p style='color: #E6F0FA; font-size: 1.3rem; margin-top: 16px;'>
    République Islamique de Mauritanie • Analyse Économique {year_range[0]}-{year_range[1]}
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs
    if 2024 in df["Année"].values:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
            st.metric("Croissance PIB", f"{val:.1f}%", delta="+1.9 pts")
        with col2:
            val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
            st.metric("Inflation", f"{val:.1f}%", delta="-1.4 pts", delta_color="inverse")
        with col3:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
            st.metric("Recettes Fiscales", f"{val:.1f}% PIB", delta="+3.8 pts")
        with col4:
            dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
            st.metric("Dette Extérieure", f"{dette:.1f} Md$", delta="Stable", delta_color="off")
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header"><span class="section-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D"><path d="M17 9L15 11L11 7L9 9L5 5"/><path d="M21 21H3"/></svg></span><h3>Évolution du PIB</h3></div>', unsafe_allow_html=True)
        df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        if len(df_pib) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"], mode='lines', name='Croissance', line=dict(color=BLEU_FONCE, width=3)))
            fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(5).mean(), mode='lines', name='Tendance', line=dict(color=BLEU_MOYEN, width=4, dash='dash')))
            for year in [1975, 2009, 2020]:
                if year in df_pib["Année"].values and year >= year_range[0] and year <= year_range[1]:
                    y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                    fig.add_annotation(x=year, y=y_val, text="", showarrow=True, arrowhead=2, arrowcolor=BLEU_FONCE)
            fig.update_layout(title="Croissance du PIB – cycles économiques et chocs", xaxis_title="Année", yaxis_title="%", hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)  # ✅ INTERACTIF
    
    with col2:
        st.markdown('<div class="section-header"><span class="section-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/></svg></span><h3>Inflation & Stabilité</h3></div>', unsafe_allow_html=True)
        df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
        if len(df_infl) > 0:
            median = df_infl["Inflation_pct"].median()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_infl["Année"], y=df_infl["Inflation_pct"], mode='lines', line=dict(color=BLEU_FONCE, width=3)))
            fig.add_hline(y=median, line_dash="dash", line_color=BLEU_MOYEN, annotation_text=f"Médiane ({median:.1f}%)")
            fig.update_layout(title="Inflation – régimes macroéconomiques", xaxis_title="Année", yaxis_title="%", hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)  # ✅ INTERACTIF

# =====================================
# PAGE 2: CROISSANCE & INFLATION
# =====================================
elif page == "📈 Croissance & Inflation":
    st.markdown('<div class="hero-header" style="background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; padding: 48px; margin-bottom: 40px;"><h1 class="hero-title">Croissance & Inflation</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header"><span class="section-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D"><path d="M17 9L15 11L11 7L9 9L5 5"/><path d="M21 21H3"/></svg></span><h3>Croissance du PIB – Cycles et Chocs</h3></div>', unsafe_allow_html=True)
    df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
    if len(df_pib) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"], mode='lines', name='Croissance', line=dict(color=BLEU_FONCE, width=3)))
        fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(10).mean(), mode='lines', name='Tendance long terme', line=dict(color=BLEU_MOYEN, width=4, dash='dash')))
        for year in [1975, 2009, 2020]:
            if year in df_pib["Année"].values and year >= year_range[0] and year <= year_range[1]:
                y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                fig.add_annotation(x=year, y=y_val, text="", showarrow=True, arrowhead=2, arrowcolor=BLEU_FONCE)
        fig.update_layout(title="Croissance du PIB – cycles économiques et chocs\nSource : BCM, FMI, Banque Mondiale", xaxis_title="Année", yaxis_title="%", hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)  # ✅ INTERACTIF

# =====================================
# PAGE 3: SECTEUR EXTERNE
# =====================================
elif page == "🌍 Secteur Externe":
    st.markdown('<div class="hero-header" style="background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; padding: 48px; margin-bottom: 40px;"><h1 class="hero-title">Secteur Externe</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header"><span class="section-icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg></span><h3>Dette Extérieure vs Réserves</h3></div>', unsafe_allow_html=True)
    df_ext = df_filtered.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()
    if len(df_ext) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9, mode='lines', name='Dette extérieure', line=dict(color=BLEU_FONCE, width=3)))
        fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Reserves_internationales_USD"]/1e9, mode='lines', name='Réserves', line=dict(color=BLEU_MOYEN, width=3)))
        fig.update_layout(title="Soutenabilité externe : dette vs réserves\nSource : Banque Mondiale", xaxis_title="Année", yaxis_title="Milliards USD", hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)  # ✅ INTERACTIF

# =====================================
# FOOTER
# =====================================
st.markdown("""
<div style='text-align: center; padding: 48px; margin-top: 60px; background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; color: white;'>
<h2 style="color: white; margin: 0; font-size: 1.5rem;">Dashboard Macroéconomique de la Mauritanie</h2>
<p style="margin: 16px 0 8px 0; font-size: 1.1rem; color: #E6F0FA;">
<b>Jedou Mohamed Bebacar</b> | Master SSD | Université de Nouakchott
</p>
</div>
""", unsafe_allow_html=True)
