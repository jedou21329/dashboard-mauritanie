# app.py - Dashboard Macroéconomique Mauritanie - Version Complète et Optimisée
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
[data-testid="stSidebar"] .stRadio > label {
font-size: 18px !important;
font-weight: 700 !important;
margin-bottom: 20px;
text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
[data-testid="stSidebar"] [role="radiogroup"] label {
background: rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 16px 20px;
margin: 8px 0;
transition: all 0.3s ease;
cursor: pointer;
backdrop-filter: blur(10px);
border: 2px solid transparent;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
background: rgba(255, 255, 255, 0.2);
transform: translateX(10px);
border: 2px solid #87CEEB;
box-shadow: 0 4px 12px rgba(135, 206, 235, 0.3);
}
/* Titres avec effet */
h1 {
background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
font-weight: 900 !important;
font-size: 3rem !important;
letter-spacing: -2px;
animation: slideInDown 0.8s ease-out;
text-shadow: 0 0 30px rgba(12, 74, 110, 0.3);
}
h2 {
color: #1e293b !important;
font-weight: 800 !important;
animation: fadeInUp 0.6s ease-out;
position: relative;
padding-bottom: 15px;
}
h2::after {
content: '';
position: absolute;
bottom: 0;
left: 0;
width: 80px;
height: 4px;
background: linear-gradient(90deg, #87CEEB, transparent);
border-radius: 2px;
}
h3 {
color: #1e293b !important;
font-weight: 700 !important;
margin-top: 2rem !important;
}
/* KPI Cards Premium */
[data-testid="stMetric"] {
background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
backdrop-filter: blur(20px);
border-radius: 24px;
padding: 28px;
box-shadow:
0 10px 40px rgba(0, 0, 0, 0.1),
inset 0 1px 0 rgba(255, 255, 255, 0.6);
border: 1px solid rgba(255, 255, 255, 0.4);
transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
position: relative;
overflow: hidden;
}
[data-testid="stMetric"]::before {
content: '';
position: absolute;
top: -50%;
left: -50%;
width: 200%;
height: 200%;
background: linear-gradient(
45deg,
transparent,
rgba(135, 206, 235, 0.1),
transparent
);
transform: rotate(45deg);
animation: shimmer 3s infinite;
}
@keyframes shimmer {
0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}
[data-testid="stMetric"]:hover {
transform: translateY(-12px) scale(1.03);
box-shadow:
0 20px 60px rgba(12, 74, 110, 0.25),
inset 0 1px 0 rgba(255, 255, 255, 0.8);
border: 1px solid #87CEEB;
}
[data-testid="stMetricValue"] {
font-size: 42px !important;
font-weight: 900 !important;
background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
animation: countUp 1.2s ease-out;
letter-spacing: -1px;
}
[data-testid="stMetricLabel"] {
color: #64748b !important;
font-weight: 700 !important;
font-size: 13px !important;
text-transform: uppercase;
letter-spacing: 1.5px;
margin-bottom: 8px;
}
[data-testid="stMetricDelta"] {
font-weight: 800 !important;
font-size: 15px !important;
}
/* Charts avec effet 3D */
.stPyplot {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 28px;
padding: 32px;
box-shadow:
0 8px 32px rgba(0,0,0,0.08),
0 2px 8px rgba(0,0,0,0.04);
transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
border: 1px solid rgba(226, 232, 240, 0.8);
animation: fadeInUp 0.8s ease-out;
position: relative;
}
.stPyplot::before {
content: '';
position: absolute;
top: 0;
left: 0;
right: 0;
height: 4px;
background: linear-gradient(90deg, #0B3C5D, #1F77B4, #87CEEB);
border-radius: 28px 28px 0 0;
}
.stPyplot:hover {
transform: translateY(-8px);
box-shadow:
0 16px 48px rgba(0,0,0,0.15),
0 4px 16px rgba(0,0,0,0.1);
border: 1px solid #87CEEB;
}
/* Hero Header */
.hero-header {
background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 50%, #0B3C5D 100%);
border-radius: 32px;
padding: 48px;
margin-bottom: 40px;
position: relative;
overflow: hidden;
box-shadow: 0 20px 60px rgba(11, 60, 93, 0.3);
}
.hero-header::before {
content: '';
position: absolute;
top: -50%;
right: -50%;
width: 200%;
height: 200%;
background: radial-gradient(circle, rgba(135, 206, 235, 0.1) 0%, transparent 70%);
animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse {
0%, 100% { transform: scale(1); opacity: 0.5; }
50% { transform: scale(1.1); opacity: 0.8; }
}
.hero-content {
position: relative;
z-index: 1;
}
.hero-title {
color: white;
font-size: 3.5rem;
font-weight: 900;
margin: 0;
text-shadow: 0 4px 12px rgba(0,0,0,0.3);
letter-spacing: -2px;
}
.hero-subtitle {
color: #E6F0FA;
font-size: 1.3rem;
margin-top: 16px;
font-weight: 500;
text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
/* Badges */
.badge {
display: inline-block;
padding: 8px 16px;
background: linear-gradient(135deg, #87CEEB, #1F77B4);
color: white;
border-radius: 20px;
font-size: 12px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 1px;
box-shadow: 0 4px 12px rgba(135, 206, 235, 0.4);
animation: fadeInUp 0.6s ease-out;
margin-right: 12px;
}
/* Tabs personnalisés */
.stTabs [data-baseweb="tab-list"] {
gap: 12px;
background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
padding: 12px;
border-radius: 20px;
box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab"] {
background: white;
border-radius: 14px;
padding: 12px 28px;
font-weight: 700;
border: 2px solid transparent;
transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(135, 206, 235, 0.3);
}
.stTabs [aria-selected="true"] {
background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%) !important;
color: white !important;
border: 2px solid #87CEEB;
box-shadow: 0 6px 20px rgba(11, 60, 93, 0.4);
}
/* Animations */
@keyframes fadeInUp {
from {
opacity: 0;
transform: translateY(40px);
}
to {
opacity: 1;
transform: translateY(0);
}
}
@keyframes slideInDown {
from {
opacity: 0;
transform: translateY(-40px);
}
to {
opacity: 1;
transform: translateY(0);
}
}
@keyframes countUp {
from {
opacity: 0;
transform: scale(0.3);
}
to {
opacity: 1;
transform: scale(1);
}
}
/* Scrollbar */
::-webkit-scrollbar {
width: 14px;
}
::-webkit-scrollbar-track {
background: linear-gradient(180deg, #f1f5f9, #e0f2fe);
}
::-webkit-scrollbar-thumb {
background: linear-gradient(180deg, #87CEEB, #1F77B4);
border-radius: 10px;
border: 3px solid #f1f5f9;
}
::-webkit-scrollbar-thumb:hover {
background: linear-gradient(180deg, #1F77B4, #0B3C5D);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------
@st.cache_data
def load_and_clean_data():
    """Charge et nettoie les données avec gestion robuste des erreurs"""
    try:
        df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
        df["Année"] = df["Année"].astype(int)
        df = df.groupby("Année", as_index=False).first()
        df = df.sort_values("Année").reset_index(drop=True)
        
        # Imputation ciblée
        df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"] = df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"].interpolate()
        df.loc[df["Année"] >= 1986, "Inflation_pct"] = df.loc[df["Année"] >= 1986, "Inflation_pct"].interpolate()
        df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"].interpolate()
        df.loc[df["Année"] >= 1975, "Envois_de_fonds_pct_PIB"] = df.loc[df["Année"] >= 1975, "Envois_de_fonds_pct_PIB"].interpolate(limit=4).fillna(df["Envois_de_fonds_pct_PIB"].mean())
        df.loc[df["Année"] >= 1970, "Dette_exterieure_USD"] = df.loc[df["Année"] >= 1970, "Dette_exterieure_USD"].interpolate()
        df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"] = df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"].fillna(df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"].mean())
        df.loc[(df["Année"] >= 1963) & (df["Année"] <= 2021), "Reserves_internationales_USD"] = df.loc[(df["Année"] >= 1963) & (df["Année"] <= 2021), "Reserves_internationales_USD"].interpolate()
        df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].fillna(df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].mean())
        return df
    except FileNotFoundError:
        st.error("❌ Fichier 'macro_mauritanie_complet_1960_2024.csv' introuvable. Veuillez le placer dans le même répertoire que app.py")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {str(e)}")
        return pd.DataFrame()

df = load_and_clean_data()
# Vérification des données
if df.empty:
    st.stop()

# Couleurs de la charte graphique
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"
BLEU_TRES_CLAIR = "#E6F0FA"

# Configuration Matplotlib
plt.rcParams.update({
    "axes.edgecolor": BLEU_FONCE,
    "axes.labelcolor": BLEU_FONCE,
    "xtick.color": BLEU_FONCE,
    "ytick.color": BLEU_FONCE,
    "text.color": BLEU_FONCE,
    "font.size": 11,
    "figure.dpi": 150
})

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg'
    width='120' style='border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);'/>
    <h1 style='color: white; margin-top: 24px; font-size: 1.8rem; text-shadow: 0 2px 8px rgba(0,0,0,0.3);'>
    🏦 Dashboard<br/>Mauritanie
    </h1>
    <p style='color: #E6F0FA; font-size: 0.9rem; margin-top: 12px;'>
    Analyse Macroéconomique Avancée
    </p>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio(
        "🧭 Navigation",
        ["🏠 Vue d'ensemble",
         "📈 Croissance & Inflation",
         "🌍 Secteur Externe",
         "💰 Finances Publiques",
         "📊 Analyses Avancées"],
        label_visibility="visible"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    # Filtres temporels
    st.markdown("### ⏱️ Filtres Temporels")
    year_range = st.slider(
        "Période d'analyse",
        int(df["Année"].min()),
        int(df["Année"].max()),
        (2000, 2024)
    )
    st.markdown("<br>", unsafe_allow_html=True)
    # Info sidebar
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 16px; margin-top: 30px;'>
    <p style='color: #E6F0FA; font-size: 0.85rem; margin: 0; line-height: 1.6;'>
    <b>📊 Sources de données:</b><br/>
    • Banque Centrale (BCM)<br/>
    • FMI & Banque Mondiale<br/>
    • Données 1960-2024
    </p>
    </div>
    """, unsafe_allow_html=True)

# Filtrer les données selon la période
df_filtered = df[(df["Année"] >= year_range[0]) & (df["Année"] <= year_range[1])].copy()

# =====================================
# PAGE 1: VUE D'ENSEMBLE
# =====================================
if page == "🏠 Vue d'ensemble":
    # Hero Header
    st.markdown(f"""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">Dashboard Macroéconomique</h1>
    <p class="hero-subtitle">
    République Islamique de Mauritanie • Analyse Économique {year_range[0]}-{year_range[1]}
    </p>
    <div style='margin-top: 24px;'>
    <span class='badge'>✓ Données actualisées 2026</span>
    <span class='badge'>✓ 14 Indicateurs</span>
    <span class='badge'>✓ Multi-sources</span>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Principaux
    st.markdown("### 📊 Indicateurs Clés 2024")
    if 2024 in df["Année"].values:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0] if not df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].isna().iloc[0] else 0
            st.metric("🚀 Croissance PIB", f"{val:.1f}%", delta="+1.9 pts", help="Taux de croissance du PIB réel")
        with col2:
            val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0] if not df.loc[df["Année"] == 2024, "Inflation_pct"].isna().iloc[0] else 0
            st.metric("🔥 Inflation", f"{val:.1f}%", delta="-1.4 pts", delta_color="inverse", help="Taux d'inflation annuel")
        with col3:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0] if not df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].isna().iloc[0] else 0
            st.metric("💼 Recettes Fiscales", f"{val:.1f}% PIB", delta="+3.8 pts", help="Recettes fiscales en % du PIB")
        with col4:
            dette_val = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] if not df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].isna().iloc[0] else 0
            dette = dette_val / 1e9
            st.metric("🌍 Dette Extérieure", f"{dette:.1f} Md$", delta="Stable", delta_color="off", help="Dette extérieure totale")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Évolution du PIB")
        df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        if len(df_pib) > 0:
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2, label="Croissance")
            ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"].rolling(5).mean(), color=BLEU_MOYEN, linewidth=3, label="Tendance")
            ax.fill_between(df_pib["Année"], df_pib["Croissance_PIB_pct"], where=df_pib["Croissance_PIB_pct"] < 0, color=BLEU_CLAIR, alpha=0.6)
            for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
                if year in df_pib["Année"].values and year >= year_range[0] and year <= year_range[1]:
                    y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                    ax.annotate(label, xy=(year, y_val), xytext=(year, y_val-6),
                                arrowprops=dict(arrowstyle="->", color=BLEU_FONCE), ha="center", fontsize=9)
            ax.axhline(0, linestyle="--", color="gray")
            ax.set_title("Croissance du PIB – cycles économiques et chocs\nSource : BCM, FMI, Banque Mondiale", weight="bold")
            ax.set_ylabel("%")
            ax.legend()
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    with col2:
        st.markdown("#### 💸 Inflation & Stabilité")
        df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
        if len(df_infl) > 0:
            median = df_infl["Inflation_pct"].median()
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.plot(df_infl["Année"], df_infl["Inflation_pct"], color=BLEU_FONCE, linewidth=2)
            ax.axhline(median, linestyle="--", color=BLEU_MOYEN, label=f"Inflation médiane ({median:.1f}%)")
            ax.fill_between(df_infl["Année"], median, df_infl["Inflation_pct"], where=df_infl["Inflation_pct"] > median, color=BLEU_CLAIR, alpha=0.6, label="Régime inflation élevée")
            ax.set_title("Inflation – régimes macroéconomiques\nSource : BCM, FMI", weight="bold")
            ax.set_ylabel("%")
            ax.legend()
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    # Tableau de bord consolidé
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Panorama Économique Multi-Indicateurs")
    
    # 1. Balance commerciale
    df_bc = df_filtered.dropna(subset=["Solde_commercial_pct_PIB"])
    if len(df_bc) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        colors = ['#10B981' if x >= 0 else '#EF4444' for x in df_bc["Solde_commercial_pct_PIB"]]
        ax.bar(df_bc["Année"], df_bc["Solde_commercial_pct_PIB"], color=colors)
        ax.axhline(0, color='#475569', linewidth=2)
        ax.set_title("Balance Commerciale (% du PIB)\nSource : Banque Mondiale", weight="bold")
        ax.set_ylabel("% du PIB")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    # 2. Recettes fiscales
    df_rf = df_filtered.dropna(subset=["Recettes_fiscales_pct_PIB"])
    if len(df_rf) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_rf["Année"], df_rf["Recettes_fiscales_pct_PIB"], color=BLEU_FONCE, linewidth=2, marker='o')
        moyenne = df_rf["Recettes_fiscales_pct_PIB"].mean()
        ax.axhline(moyenne, linestyle="--", color=BLEU_MOYEN, label=f"Moyenne ({moyenne:.1f}%)")
        ax.set_title("Recettes Fiscales (% du PIB)\nSource : FMI", weight="bold")
        ax.set_ylabel("% du PIB")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    # 3. Envois de fonds
    df_ef = df_filtered.dropna(subset=["Envois_de_fonds_pct_PIB"])
    if len(df_ef) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_ef["Année"], df_ef["Envois_de_fonds_pct_PIB"], color=BLEU_FONCE, linewidth=2, marker='o')
        ax.set_title("Envois de Fonds (% du PIB)\nSource : Banque Mondiale", weight="bold")
        ax.set_ylabel("% du PIB")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    # 4. Taux de chômage
    df_tc = df_filtered.dropna(subset=["Taux_chomage_pct"])
    if len(df_tc) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_tc["Année"], df_tc["Taux_chomage_pct"], color=BLEU_FONCE, linewidth=2, marker='o')
        ax.set_title("Taux de Chômage (%)\nSource : BCM", weight="bold")
        ax.set_ylabel("%")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    
    # Analyse par décennie
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Moyennes par Décennie")
    df_2000 = df[df["Année"] >= 2000].copy()
    df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
    dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean()
    if len(dec) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        x = [str(int(d)) for d in dec.index]
        ax.bar(x, dec["Croissance_PIB_pct"], label='Croissance PIB', color=BLEU_FONCE)
        ax.bar(x, dec["Inflation_pct"], label='Inflation', color=BLEU_MOYEN)
        ax.bar(x, dec["Taux_chomage_pct"], label='Chômage', color=BLEU_CLAIR)
        ax.set_title("Indicateurs macroéconomiques – moyennes par décennie (depuis 2000)\nSource : Calculs propres", weight="bold")
        ax.set_ylabel("Pourcentage (%)")
        ax.legend()
        ax.grid(axis="y", alpha=0.25)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# =====================================
# PAGE 2: CROISSANCE & INFLATION
# =====================================
elif page == "📈 Croissance & Inflation":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">📈 Croissance & Inflation</h1>
    <p class="hero-subtitle">Analyse des cycles économiques et dynamiques des prix</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Cycles Économiques", "🔥 Régimes d'Inflation", "💹 Courbe Phillips", "📈 Volatilité"])
    
    with tab1:
        st.markdown("### 🔄 Croissance du PIB – Cycles et Chocs")
        df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        if len(df_pib) > 0:
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2, label="Croissance")
            ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"].rolling(10).mean(), color=BLEU_MOYEN, linewidth=3, label="Tendance long terme")
            ax.fill_between(df_pib["Année"], df_pib["Croissance_PIB_pct"], where=df_pib["Croissance_PIB_pct"] < 0, color=BLEU_CLAIR, alpha=0.6)
            for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
                if year in df_pib["Année"].values and year >= year_range[0] and year <= year_range[1]:
                    y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                    ax.annotate(label, xy=(year, y_val), xytext=(year, y_val-6),
                                arrowprops=dict(arrowstyle="->", color=BLEU_FONCE), ha="center", fontsize=9)
            ax.axhline(0, linestyle="--", color="gray")
            ax.set_title("Croissance du PIB – cycles économiques et chocs\nSource : BCM, FMI, Banque Mondiale", weight="bold")
            ax.set_ylabel("%")
            ax.legend()
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Moyenne", f"{df_pib['Croissance_PIB_pct'].mean():.2f}%")
            with col2:
                st.metric("📈 Maximum", f"{df_pib['Croissance_PIB_pct'].max():.2f}%")
            with col3:
                st.metric("📉 Minimum", f"{df_pib['Croissance_PIB_pct'].min():.2f}%")
            with col4:
                st.metric("📏 Écart-type", f"{df_pib['Croissance_PIB_pct'].std():.2f}%")
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    with tab2:
        st.markdown("### 🔥 Inflation – Régimes Macroéconomiques")
        df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
        if len(df_infl) > 0:
            median = df_infl["Inflation_pct"].median()
            fig, ax = plt.subplots(figsize=(14, 4))
            ax.plot(df_infl["Année"], df_infl["Inflation_pct"], color=BLEU_FONCE, linewidth=2)
            ax.axhline(median, linestyle="--", color=BLEU_MOYEN, label=f"Inflation médiane ({median:.1f}%)")
            ax.fill_between(df_infl["Année"], median, df_infl["Inflation_pct"], where=df_infl["Inflation_pct"] > median, color=BLEU_CLAIR, alpha=0.6, label="Régime inflation élevée")
            ax.set_title("Inflation – régimes macroéconomiques\nSource : BCM, FMI", weight="bold")
            ax.set_ylabel("%")
            ax.legend()
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.hist(df_infl["Inflation_pct"], bins=20, color=BLEU_MOYEN, edgecolor='white')
                ax.set_title("Distribution de l'inflation")
                ax.set_xlabel("Inflation (%)")
                ax.set_ylabel("Fréquence")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            with col2:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.boxplot(df_infl["Inflation_pct"], patch_artist=True, boxprops=dict(facecolor=BLEU_FONCE))
                ax.set_title("Statistiques descriptives")
                ax.set_ylabel("Inflation (%)")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    with tab3:
        st.markdown("### 💹 Courbe de Phillips")
        df_ph = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        if len(df_ph) > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            sc = ax.scatter(df_ph["Taux_chomage_pct"], df_ph["Inflation_pct"], c=df_ph["Année"], cmap="Blues", s=90, edgecolor="black")
            plt.colorbar(sc, ax=ax, label="Année")
            ax.set_xlabel("Chômage (%)")
            ax.set_ylabel("Inflation (%)")
            ax.set_title("Courbe de Phillips – Mauritanie (2007–2021)\nSource : BCM", weight="bold")
            ax.grid(alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Données insuffisantes pour la période sélectionnée")
    
    with tab4:
        st.markdown("### 📉 Volatilité de la Croissance")
        df_vol = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        if len(df_vol) >= 10:
            roll_mean = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
            roll_std = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).std()
            fig, ax = plt.subplots(figsize=(13, 4))
            ax.plot(df_vol["Année"], roll_mean, color=BLEU_FONCE, linewidth=2.5, label="Moyenne mobile (10 ans)")
            ax.fill_between(df_vol["Année"], roll_mean - roll_std, roll_mean + roll_std,
                            color=BLEU_CLAIR, alpha=0.6, label="± 1 écart-type")
            ax.set_title("Croissance du PIB – volatilité et incertitude\nSource : Banque Mondiale", weight="bold")
            ax.set_ylabel("%")
            ax.legend()
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Période trop courte pour l'analyse de volatilité")

# =====================================
# PAGE 3: SECTEUR EXTERNE
# =====================================
elif page == "🌍 Secteur Externe":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">🌍 Secteur Externe</h1>
    <p class="hero-subtitle">Soutenabilité, dette extérieure et balance des paiements</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💰 Dette Extérieure vs Réserves")
    df_ext = df_filtered.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()
    if len(df_ext) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_ext["Année"], df_ext["Dette_exterieure_USD"]/1e9, color=BLEU_FONCE, linewidth=2, label="Dette extérieure")
        ax.plot(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, color=BLEU_MOYEN, linewidth=2, label="Réserves")
        ax.fill_between(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, df_ext["Dette_exterieure_USD"]/1e9,
                        where=df_ext["Dette_exterieure_USD"] > df_ext["Reserves_internationales_USD"],
                        color=BLEU_CLAIR, alpha=0.6, label="Zone de vulnérabilité externe")
        ax.set_title("Soutenabilité externe : dette vs réserves\nSource : Banque Mondiale", weight="bold")
        ax.set_ylabel("Milliards USD")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        col1, col2, col3 = st.columns(3)
        if len(df_ext) > 0:
            latest = df_ext.iloc[-1]
            ratio = (latest["Dette_exterieure_USD"] / latest["Reserves_internationales_USD"]) if latest["Reserves_internationales_USD"] > 0 else 0
            with col1:
                st.metric("📊 Ratio Dette/Réserves", f"{ratio:.2f}x", help="Ratio inférieur à 3 = soutenable")
            with col2:
                st.metric("💵 Dette", f"{latest['Dette_exterieure_USD']/1e9:.2f} Md$")
            with col3:
                st.metric("🏦 Réserves", f"{latest['Reserves_internationales_USD']/1e9:.2f} Md$")
    else:
        st.info("📊 Pas de données disponibles pour cette période")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📦 Solde Commercial")
    df_bc = df_filtered.dropna(subset=["Solde_commercial_pct_PIB"])
    if len(df_bc) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        colors = ['#10B981' if x >= 0 else '#EF4444' for x in df_bc["Solde_commercial_pct_PIB"]]
        ax.bar(df_bc["Année"], df_bc["Solde_commercial_pct_PIB"], color=colors)
        ax.axhline(0, color='#475569', linewidth=2)
        ax.set_title("Solde Commercial (% du PIB)\nSource : Banque Mondiale", weight="bold")
        ax.set_ylabel("% du PIB")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("📊 Pas de données disponibles pour cette période")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💸 Envois de Fonds")
    df_ef = df_filtered.dropna(subset=["Envois_de_fonds_pct_PIB"])
    if len(df_ef) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_ef["Année"], df_ef["Envois_de_fonds_pct_PIB"], color=BLEU_FONCE, linewidth=2, marker='o')
        ax.set_title("Envois de Fonds (% du PIB)\nSource : Banque Mondiale", weight="bold")
        ax.set_ylabel("% du PIB")
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("📊 Pas de données disponibles pour cette période")

# =====================================
# PAGE 4: FINANCES PUBLIQUES
# =====================================
elif page == "💰 Finances Publiques":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">💰 Finances Publiques</h1>
    <p class="hero-subtitle">Recettes fiscales, dépenses et viabilité budgétaire</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💼 Évolution des Recettes Fiscales")
    df_rf = df_filtered.dropna(subset=["Recettes_fiscales_pct_PIB"])
    if len(df_rf) > 0:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(df_rf["Année"], df_rf["Recettes_fiscales_pct_PIB"], color=BLEU_FONCE, linewidth=2, marker='o')
        moyenne = df_rf["Recettes_fiscales_pct_PIB"].mean()
        ax.axhline(moyenne, linestyle="--", color=BLEU_MOYEN, label=f"Moyenne ({moyenne:.1f}%)")
        ax.set_title("Évolution des Recettes Fiscales (% du PIB)\nSource : FMI", weight="bold")
        ax.set_ylabel("% du PIB")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("📊 Pas de données disponibles pour cette période")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### Structure des recettes 2024")
        if 2024 in df["Année"].values:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
            if pd.notna(val):
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie([val, 100-val], labels=["Recettes fiscales", "Autres"], colors=[BLEU_MOYEN, BLEU_TRES_CLAIR],
                       autopct="%1.1f%%", startangle=90, wedgeprops=dict(edgecolor="white"))
                ax.set_title("Poids des recettes fiscales – 2024\nSource : FMI (2023)", weight="bold")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            else:
                st.info("📊 Données non disponibles pour 2024")
        else:
            st.info("📊 Données non disponibles pour 2024")
    
    with col2:
        st.markdown("#### Recettes Fiscales 2007-2024")
        df_3d_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
        if len(df_3d_bar) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(df_3d_bar["Année"].astype(str), df_3d_bar["Recettes_fiscales_pct_PIB"], color=BLEU_MOYEN)
            ax.set_title("Recettes Fiscales 2007-2024\nSource : FMI", weight="bold")
            ax.set_ylabel("% du PIB")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax.grid(axis="y", alpha=0.3)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 👥 Croissance vs Chômage")
    df_cc = df_filtered.dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
    if len(df_cc) > 0:
        x = np.arange(len(df_cc))
        w = 0.4
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.bar(x - w/2, df_cc["Croissance_PIB_pct"], w, label="Croissance PIB", color=BLEU_MOYEN)
        ax.bar(x + w/2, df_cc["Taux_chomage_pct"], w, label="Chômage", color=BLEU_CLAIR)
        for i in range(len(df_cc)):
            ax.text(i - w/2, df_cc["Croissance_PIB_pct"].iloc[i] + 0.3, f"{df_cc['Croissance_PIB_pct'].iloc[i]:.1f}%", ha="center", fontsize=8)
            ax.text(i + w/2, df_cc["Taux_chomage_pct"].iloc[i] + 0.3, f"{df_cc['Taux_chomage_pct'].iloc[i]:.1f}%", ha="center", fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(df_cc["Année"], rotation=45)
        ax.set_ylabel("%")
        ax.set_title("Croissance économique et chômage (2007–2021)\nSource : BCM", weight="bold")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("📊 Pas de données disponibles pour cette période")

# =====================================
# PAGE 5: ANALYSES AVANCÉES
# =====================================
elif page == "📊 Analyses Avancées":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">📊 Analyses Avancées</h1>
    <p class="hero-subtitle">Corrélations, trajectoires et analyses multidimensionnelles</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Heatmap", "🎲 Trajectoire 3D", "📦 Boxplots", "📈 Analyses Multi"])
    
    with tab1:
        st.markdown("### 🔥 Matrice de Corrélation")
        corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
        df_corr = df_filtered[corr_vars].dropna()
        if len(df_corr) > 5:
            corr = df_corr.corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.6, linecolor="white", cbar_kws={"shrink": 0.8}, ax=ax)
            ax.set_title("Corrélations entre indicateurs macroéconomiques (2007–2024)\nSource : Calculs propres", weight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Données insuffisantes pour calculer les corrélations (minimum 5 observations)")
    
    with tab2:
        st.markdown("### 🎲 Trajectoire Macroéconomique 3D")
        df_3d = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
        if len(df_3d) > 5:
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection="3d")
            sc = ax.scatter(df_3d["Inflation_pct"], df_3d["Taux_chomage_pct"], df_3d["Croissance_PIB_pct"],
                            c=df_3d["Année"], cmap="Blues", s=70, edgecolor="black", alpha=0.9)
            ax.plot(df_3d["Inflation_pct"], df_3d["Taux_chomage_pct"], df_3d["Croissance_PIB_pct"], color=BLEU_FONCE, alpha=0.6)
            ax.set_xlabel("Inflation (%)")
            ax.set_ylabel("Chômage (%)")
            ax.set_zlabel("Croissance (%)")
            ax.set_title("Trajectoire macroéconomique 3D (depuis 2000)\nSource : Calculs propres", weight="bold")
            fig.colorbar(sc, ax=ax, label="Année")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Données insuffisantes pour la visualisation 3D")
    
    with tab3:
        st.markdown("### 📦 Distribution par Période")
        df_box = df.copy()
        df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])
        df_box = df_box[df_box["Période"].notna()]
        if len(df_box) > 0:
            fig, ax = plt.subplots(figsize=(14, 5))
            sns.boxplot(data=df_box, x="Période", y="Croissance_PIB_pct", palette=[BLEU_CLAIR, BLEU_MOYEN, BLEU_FONCE], ax=ax)
            ax.set_title("Distribution de la croissance du PIB par période\nSource : Banque Mondiale", weight="bold")
            ax.set_ylabel("%")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles")
    
    with tab4:
        st.markdown("### 📈 Pression Macroéconomique")
        df_area = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        if len(df_area) > 0:
            fig, ax = plt.subplots(figsize=(13, 4))
            ax.stackplot(df_area["Année"], df_area["Inflation_pct"], df_area["Taux_chomage_pct"],
                         labels=["Inflation", "Chômage"], colors=[BLEU_CLAIR, BLEU_MOYEN], alpha=0.85)
            ax.set_title("Pression macroéconomique : inflation et chômage\nSource : BCM, FMI", weight="bold")
            ax.set_ylabel("%")
            ax.legend(loc="upper left")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles pour cette période")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 Régimes Macroéconomiques (Scatter)")
        df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
        if len(df_2000) > 0:
            median_infl = df_2000["Inflation_pct"].median()
            fig, ax = plt.subplots(figsize=(9, 6))
            ax.scatter(df_2000["Inflation_pct"], df_2000["Croissance_PIB_pct"], c=df_2000["Année"], cmap="Blues", s=80, edgecolor="black", alpha=0.9)
            plt.colorbar(ax.collections[0], ax=ax, label="Année")
            ax.axhline(0, color="gray", linestyle="--")
            ax.axvline(median_infl, linestyle="--", color="gray")
            ax.set_title("Régimes macroéconomiques (Inflation vs Croissance)\nSource : Calculs propres", weight="bold")
            ax.set_xlabel("Inflation (%)")
            ax.set_ylabel("Croissance (%)")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("📊 Pas de données disponibles depuis 2000")

# =====================================
# FOOTER GLOBAL
# =====================================
st.markdown("""
<div style='text-align: center; padding: 48px; margin-top: 60px; background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; color: white;'>
<h2 style="color: white; margin: 0; font-size: 1.5rem;">Dashboard Macroéconomique de la Mauritanie</h2>
<p style="margin: 16px 0 8px 0; font-size: 1.1rem; color: #E6F0FA;">
<b>Jedou Mohamed Bebacar</b> | Master SSD | Université de Nouakchott
</p>
<p style="margin: 8px 0 0 0; font-size: 0.95rem; color: #AEC7E8;">
© 2026 • 14 Visualisations Interactives • Multi-sources • Données actualisées janvier 2026
</p>
<p style="margin: 12px 0 0 0; font-size: 0.85rem; color: #87CEEB;">
🛠️ Développé avec Streamlit & Matplotlib • 🔄 Mise à jour trimestrielle
</p>
</div>
""", unsafe_allow_html=True)
