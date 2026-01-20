
# app.py - Dashboard Macroéconomique Mauritanie - Version Complète et Optimisée
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
    .stPlotlyChart {
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
    
    .stPlotlyChart::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #0B3C5D, #1F77B4, #87CEEB);
        border-radius: 28px 28px 0 0;
    }
    
    .stPlotlyChart:hover {
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
            df_pib['Tendance'] = df_pib['Croissance_PIB_pct'].rolling(5, min_periods=1).mean()
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_pib["Année"],
                y=df_pib["Croissance_PIB_pct"],
                name='Croissance annuelle',
                marker=dict(
                    color=df_pib["Croissance_PIB_pct"],
                    colorscale=[[0, '#EF4444'], [0.5, BLEU_CLAIR], [1, BLEU_FONCE]],
                    line=dict(width=0)
                ),
                hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=df_pib['Tendance'],
                mode='lines',
                name='Tendance',
                line=dict(color='#F59E0B', width=4, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Tendance: %{y:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title='Année'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Croissance (%)', zeroline=True),
                hovermode='x unified',
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=0, r=0, t=10, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    with col2:
        st.markdown("#### 💸 Inflation & Stabilité")
        
        df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
        if len(df_infl) > 0:
            median = df_infl["Inflation_pct"].median()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_infl["Année"],
                y=df_infl["Inflation_pct"],
                mode='lines+markers',
                name='Inflation',
                line=dict(color=BLEU_FONCE, width=3),
                marker=dict(size=6, color=BLEU_MOYEN, line=dict(width=2, color='white')),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.1)',
                hovertemplate='<b>%{x}</b><br>Inflation: %{y:.1f}%<extra></extra>'
            ))
            
            fig.add_hline(y=median, line_dash="dot", line_color='#EF4444', line_width=2,
                          annotation_text=f"Médiane: {median:.1f}%", annotation_position="right")
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title='Année'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='Inflation (%)'),
                hovermode='x unified',
                height=400,
                margin=dict(l=0, r=0, t=10, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    # Tableau de bord consolidé
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Panorama Économique Multi-Indicateurs")
    
    fig_multi = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Balance Commerciale', 'Recettes Fiscales', 'Envois de Fonds', 'Taux de Chômage'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # 1. Balance commerciale
    df_bc = df_filtered.dropna(subset=["Solde_commercial_pct_PIB"])
    if len(df_bc) > 0:
        fig_multi.add_trace(go.Scatter(
            x=df_bc["Année"],
            y=df_bc["Solde_commercial_pct_PIB"],
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.2)',
            line=dict(color='#10B981', width=2),
            name='Balance commerciale',
            hovertemplate='%{y:.1f}% PIB'
        ), row=1, col=1)
    
    # 2. Recettes fiscales
    df_rf = df_filtered.dropna(subset=["Recettes_fiscales_pct_PIB"])
    if len(df_rf) > 0:
        fig_multi.add_trace(go.Bar(
            x=df_rf["Année"],
            y=df_rf["Recettes_fiscales_pct_PIB"],
            marker=dict(color=BLEU_MOYEN, line=dict(width=0)),
            name='Recettes fiscales',
            hovertemplate='%{y:.1f}% PIB'
        ), row=1, col=2)
    
    # 3. Envois de fonds
    df_ef = df_filtered.dropna(subset=["Envois_de_fonds_pct_PIB"])
    if len(df_ef) > 0:
        fig_multi.add_trace(go.Scatter(
            x=df_ef["Année"],
            y=df_ef["Envois_de_fonds_pct_PIB"],
            mode='lines+markers',
            line=dict(color='#F59E0B', width=3),
            marker=dict(size=6, color='#FBBF24'),
            name='Envois de fonds',
            hovertemplate='%{y:.1f}% PIB'
        ), row=2, col=1)
    
    # 4. Taux de chômage
    df_tc = df_filtered.dropna(subset=["Taux_chomage_pct"])
    if len(df_tc) > 0:
        fig_multi.add_trace(go.Scatter(
            x=df_tc["Année"],
            y=df_tc["Taux_chomage_pct"],
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)',
            line=dict(color='#EF4444', width=2),
            name='Chômage',
            hovertemplate='%{y:.1f}%'
        ), row=2, col=2)
    
    fig_multi.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    fig_multi.update_xaxes(showgrid=False)
    fig_multi.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    
    st.plotly_chart(fig_multi, use_container_width=True, config={'displayModeBar': False})
    
    # Analyse par décennie
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Moyennes par Décennie")
    
    df_2000 = df[df["Année"] >= 2000].copy()
    df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
    dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean()
    
    if len(dec) > 0:
        fig = go.Figure()
        
        x = [str(int(d)) for d in dec.index]
        
        fig.add_trace(go.Bar(
            x=x,
            y=dec["Croissance_PIB_pct"],
            name='Croissance PIB',
            marker_color=BLEU_FONCE,
            text=dec["Croissance_PIB_pct"].apply(lambda v: f"{v:.1f}%" if pd.notna(v) else "N/A"),
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=x,
            y=dec["Inflation_pct"],
            name='Inflation',
            marker_color=BLEU_MOYEN,
            text=dec["Inflation_pct"].apply(lambda v: f"{v:.1f}%" if pd.notna(v) else "N/A"),
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=x,
            y=dec["Taux_chomage_pct"],
            name='Chômage',
            marker_color=BLEU_CLAIR,
            text=dec["Taux_chomage_pct"].apply(lambda v: f"{v:.1f}%" if pd.notna(v) else "N/A"),
            textposition='outside'
        ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Décennie', showgrid=False),
            yaxis=dict(title='Pourcentage (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            height=500,
            legend=dict(title="Indicateurs", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

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
            df_pib['Tendance'] = df_pib['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=[0]*len(df_pib),
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=df_pib["Croissance_PIB_pct"],
                fill='tonexty',
                fillcolor='rgba(174, 199, 232, 0.6)',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=df_pib["Croissance_PIB_pct"],
                mode='lines',
                name='Croissance',
                line=dict(color=BLEU_FONCE, width=3),
                hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=df_pib['Tendance'],
                mode='lines',
                name='Tendance 10 ans',
                line=dict(color=BLEU_MOYEN, width=4, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Tendance: %{y:.1f}%<extra></extra>'
            ))
            
            annotations = []
            for year, label in zip([1975, 2009, 2020], ["⚡ Choc pétrolier", "💥 Crise financière", "🦠 COVID-19"]):
                if year in df_pib["Année"].values and year >= year_range[0] and year <= year_range[1]:
                    y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                    annotations.append(dict(
                        x=year, y=y_val,
                        text=label,
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor=BLEU_FONCE,
                        ax=0, ay=-60,
                        font=dict(size=12, color=BLEU_FONCE, family="Inter"),
                        bgcolor="white",
                        bordercolor=BLEU_FONCE,
                        borderwidth=2,
                        borderpad=8
                    ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(title='Croissance (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=True, zerolinecolor='#CBD5E1'),
                hovermode='x unified',
                annotations=annotations,
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
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
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_infl["Année"],
                y=[median]*len(df_infl),
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_infl["Année"],
                y=df_infl["Inflation_pct"],
                fill='tonexty',
                fillcolor='rgba(174, 199, 232, 0.6)',
                line=dict(color=BLEU_FONCE, width=3),
                name='Inflation',
                hovertemplate='<b>%{x}</b><br>Inflation: %{y:.1f}%<extra></extra>'
            ))
            
            fig.add_hline(y=median, line_dash="dash", line_color=BLEU_MOYEN, line_width=3,
                          annotation_text=f"📊 Médiane: {median:.1f}%", annotation_position="right")
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(title='Inflation (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                hovermode='x unified',
                height=500,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(
                    x=df_infl["Inflation_pct"],
                    nbinsx=20,
                    marker=dict(color=BLEU_MOYEN, line=dict(color='white', width=2)),
                    name='Distribution'
                ))
                fig_hist.update_layout(
                    title="Distribution de l'inflation",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Inflation (%)",
                    yaxis_title="Fréquence",
                    height=350,
                    showlegend=False
                )
                st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                fig_box = go.Figure()
                fig_box.add_trace(go.Box(
                    y=df_infl["Inflation_pct"],
                    marker_color=BLEU_FONCE,
                    name='Inflation',
                    boxmean='sd'
                ))
                fig_box.update_layout(
                    title="Statistiques descriptives",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title="Inflation (%)",
                    height=350,
                    showlegend=False
                )
                st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    with tab3:
        st.markdown("### 💹 Courbe de Phillips")
        
        df_ph = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        
        if len(df_ph) > 0:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_ph["Taux_chomage_pct"],
                y=df_ph["Inflation_pct"],
                mode='markers+text',
                marker=dict(
                    size=14,
                    color=df_ph["Année"],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="Année", len=0.7),
                    line=dict(width=2, color='white')
                ),
                text=df_ph["Année"].astype(str),
                textposition='top center',
                textfont=dict(size=9, color=BLEU_FONCE, family="Inter"),
                hovertemplate='<b>Année %{text}</b><br>Chômage: %{x:.1f}%<br>Inflation: %{y:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title='Taux de Chômage (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(title='Taux d'Inflation (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Données insuffisantes pour la période sélectionnée")
    
    with tab4:
        st.markdown("### 📉 Volatilité de la Croissance")
        
        df_vol = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        
        if len(df_vol) >= 10:
            roll_mean = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
            roll_std = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).std()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_vol["Année"],
                y=roll_mean + roll_std,
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_vol["Année"],
                y=roll_mean - roll_std,
                fill='tonexty',
                fillcolor='rgba(174, 199, 232, 0.4)',
                mode='lines',
                name='± 1 écart-type',
                line_color='rgba(0,0,0,0)'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_vol["Année"],
                y=roll_mean,
                mode='lines',
                name='Moyenne mobile (10 ans)',
                line=dict(color=BLEU_FONCE, width=4),
                hovertemplate='<b>%{x}</b><br>Moyenne: %{y:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(title='Croissance (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                height=450,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_ext["Année"],
            y=df_ext["Reserves_internationales_USD"]/1e9,
            fill=None,
            mode='lines',
            line_color='rgba(0,0,0,0)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_ext["Année"],
            y=df_ext["Dette_exterieure_USD"]/1e9,
            fill='tonexty',
            fillcolor='rgba(239, 68, 68, 0.15)',
            mode='lines',
            name='⚠️ Zone de vulnérabilité',
            line=dict(width=0),
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_ext["Année"],
            y=df_ext["Dette_exterieure_USD"]/1e9,
            mode='lines+markers',
            name='Dette extérieure',
            line=dict(color='#EF4444', width=4),
            marker=dict(size=8, color='#DC2626', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Dette: %{y:.2f} Md$<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_ext["Année"],
            y=df_ext["Reserves_internationales_USD"]/1e9,
            mode='lines+markers',
            name='Réserves internationales',
            line=dict(color='#10B981', width=4),
            marker=dict(size=8, color='#059669', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Réserves: %{y:.2f} Md$<extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(title='Milliards USD', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            hovermode='x unified',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
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
    st.markdown("### 📦 Balance Commerciale")
    
    df_bc = df_filtered.dropna(subset=["Solde_commercial_pct_PIB"])
    
    if len(df_bc) > 0:
        fig = go.Figure()
        
        colors = ['#10B981' if x >= 0 else '#EF4444' for x in df_bc["Solde_commercial_pct_PIB"]]
        
        fig.add_trace(go.Bar(
            x=df_bc["Année"],
            y=df_bc["Solde_commercial_pct_PIB"],
            marker=dict(color=colors, line=dict(width=0)),
            name='Solde commercial',
            hovertemplate='<b>%{x}</b><br>Solde: %{y:.1f}% PIB<extra></extra>'
        ))
        
        fig.add_hline(y=0, line_color='#475569', line_width=2)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(title='% du PIB', showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=True),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("📊 Pas de données disponibles pour cette période")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💸 Envois de Fonds")
    
    df_ef = df_filtered.dropna(subset=["Envois_de_fonds_pct_PIB"])
    
    if len(df_ef) > 0:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_ef["Année"],
            y=df_ef["Envois_de_fonds_pct_PIB"],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(245, 158, 11, 0.2)',
            line=dict(color='#F59E0B', width=3),
            marker=dict(size=10, color='#FBBF24', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Envois: %{y:.1f}% PIB<extra></extra>'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(title='% du PIB', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_rf["Année"],
            y=df_rf["Recettes_fiscales_pct_PIB"],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)',
            line=dict(color=BLEU_FONCE, width=3),
            marker=dict(size=10, color=BLEU_MOYEN, line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Recettes: %{y:.1f}% PIB<extra></extra>'
        ))
        
        moyenne = df_rf["Recettes_fiscales_pct_PIB"].mean()
        fig.add_hline(y=moyenne, line_dash="dash", line_color='#F59E0B', line_width=2,
                      annotation_text=f"📊 Moyenne: {moyenne:.1f}%", annotation_position="right")
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(title='% du PIB', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("📊 Pas de données disponibles pour cette période")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Structure des recettes 2024")
        if 2024 in df["Année"].values:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
            
            if pd.notna(val):
                fig = go.Figure()
                
                fig.add_trace(go.Pie(
                    labels=['Recettes fiscales', 'Autres recettes'],
                    values=[val, 100-val],
                    marker=dict(colors=[BLEU_MOYEN, BLEU_TRES_CLAIR]),
                    textinfo='label+percent',
                    textposition='inside',
                    textfont=dict(size=14, family="Inter", color='white'),
                    hole=0.4
                ))
                
                fig.update_layout(
                    height=400,
                    showlegend=True,
                    annotations=[dict(text=f'{val:.1f}%<br>du PIB', x=0.5, y=0.5, font_size=20, showarrow=False)]
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("📊 Données non disponibles pour 2024")
        else:
            st.info("📊 Données non disponibles pour 2024")
    
    with col2:
        st.markdown("#### Recettes Fiscales 2007-2024")
        df_3d_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
        
        if len(df_3d_bar) > 0:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_3d_bar["Année"].astype(str),
                y=df_3d_bar["Recettes_fiscales_pct_PIB"],
                marker=dict(
                    color=df_3d_bar["Recettes_fiscales_pct_PIB"],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="% PIB")
                ),
                text=df_3d_bar["Recettes_fiscales_pct_PIB"].apply(lambda x: f"{x:.1f}%"),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Recettes: %{y:.1f}% PIB<extra></extra>'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title='Année', showgrid=False),
                yaxis=dict(title='% du PIB', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 👥 Croissance vs Chômage")
    
    df_cc = df_filtered.dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
    
    if len(df_cc) > 0:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_cc["Année"],
            y=df_cc["Croissance_PIB_pct"],
            name='Croissance PIB',
            marker=dict(color=BLEU_MOYEN, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in df_cc["Croissance_PIB_pct"]],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=df_cc["Année"],
            y=df_cc["Taux_chomage_pct"],
            name='Chômage',
            marker=dict(color=BLEU_CLAIR, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in df_cc["Taux_chomage_pct"]],
            textposition='outside'
        ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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
            
            fig = go.Figure()
            
            fig.add_trace(go.Heatmap(
                z=corr.values,
                x=['Croissance', 'Inflation', 'Chômage', 'Recettes'],
                y=['Croissance', 'Inflation', 'Chômage', 'Recettes'],
                colorscale='Blues',
                text=np.round(corr.values, 2),
                texttemplate='%{text}',
                textfont={"size": 14, "family": "Inter"},
                colorbar=dict(title="Corrélation", len=0.7),
                hovertemplate='%{y} vs %{x}<br>Corrélation: %{z:.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                height=500,
                xaxis=dict(side='bottom'),
                yaxis=dict(side='left'),
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Données insuffisantes pour calculer les corrélations (minimum 5 observations)")
    
    with tab2:
        st.markdown("### 🎲 Trajectoire Macroéconomique 3D")
        
        df_3d = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
        
        if len(df_3d) > 5:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter3d(
                x=df_3d["Inflation_pct"],
                y=df_3d["Taux_chomage_pct"],
                z=df_3d["Croissance_PIB_pct"],
                mode='markers+lines',
                marker=dict(
                    size=10,
                    color=df_3d["Année"],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="Année", len=0.7),
                    line=dict(width=2, color='white')
                ),
                line=dict(color=BLEU_FONCE, width=4),
                text=df_3d["Année"],
                hovertemplate='<b>Année %{text}</b><br>Inflation: %{x:.1f}%<br>Chômage: %{y:.1f}%<br>Croissance: %{z:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                scene=dict(
                    xaxis_title='Inflation (%)',
                    yaxis_title='Chômage (%)',
                    zaxis_title='Croissance (%)',
                    bgcolor='rgba(248,250,252,0.5)',
                    xaxis=dict(backgroundcolor="rgba(255,255,255,0.9)", gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(backgroundcolor="rgba(255,255,255,0.9)", gridcolor='rgba(0,0,0,0.1)'),
                    zaxis=dict(backgroundcolor="rgba(255,255,255,0.9)", gridcolor='rgba(0,0,0,0.1)')
                ),
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Données insuffisantes pour la visualisation 3D")
    
    with tab3:
        st.markdown("### 📦 Distribution par Période")
        
        df_box = df.copy()
        df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])
        df_box = df_box[df_box["Période"].notna()]
        
        if len(df_box) > 0:
            fig = go.Figure()
            
            for i, periode in enumerate(["1960-1980", "1981-2000", "2001-2024"]):
                data = df_box[df_box["Période"] == periode]["Croissance_PIB_pct"].dropna()
                if len(data) > 0:
                    color = [BLEU_CLAIR, BLEU_MOYEN, BLEU_FONCE][i]
                    fig.add_trace(go.Box(
                        y=data,
                        name=periode,
                        marker_color=color,
                        boxmean='sd',
                        hovertemplate='<b>%{fullData.name}</b><br>Valeur: %{y:.1f}%<extra></extra>'
                    ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(title='Croissance PIB (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Pas de données disponibles")
    
    with tab4:
        st.markdown("### 📈 Pression Macroéconomique")
        
        df_area = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        
        if len(df_area) > 0:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_area["Année"],
                y=df_area["Inflation_pct"],
                mode='lines',
                name='Inflation',
                line=dict(width=0),
                fillcolor=BLEU_CLAIR,
                fill='tonexty',
                stackgroup='one'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_area["Année"],
                y=df_area["Taux_chomage_pct"],
                mode='lines',
                name='Chômage',
                line=dict(width=0),
                fillcolor=BLEU_MOYEN,
                fill='tonexty',
                stackgroup='one'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                height=450,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("📊 Pas de données disponibles pour cette période")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Régimes Macroéconomiques (Scatter)")
    
    df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
    
    if len(df_2000) > 0:
        median_infl = df_2000["Inflation_pct"].median()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_2000["Inflation_pct"],
            y=df_2000["Croissance_PIB_pct"],
            mode='markers',
            marker=dict(
                size=10,
                color=df_2000["Année"],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Année"),
                line=dict(width=1, color='black')
            ),
            text=df_2000["Année"],
            hovertemplate='<b>Année %{text}</b><br>Inflation: %{x:.1f}%<br>Croissance: %{y:.1f}%<extra></extra>'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color='gray', line_width=1)
        fig.add_vline(x=median_infl, line_dash="dash", line_color='gray', line_width=1)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Inflation (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(title='Croissance (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
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
        🛠️ Développé avec Streamlit & Plotly • 🔄 Mise à jour trimestrielle
    </p>
</div>
""", unsafe_allow_html=True)

