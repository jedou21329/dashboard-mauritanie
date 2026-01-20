# app.py - Dashboard Macroéconomique Mauritanie - Version Interactive
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# -----------------------------
# CONFIGURATION PAGE
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CSS ULTRA-MODERNE AVEC ANIMATIONS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }

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

[data-testid="stSidebar"] {
background: linear-gradient(180deg, #0B3C5D 0%, #1F77B4 100%);
border-right: 3px solid #87CEEB;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stRadio > label {
font-size: 18px !important;
font-weight: 700 !important;
margin-bottom: 20px;
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

h1 {
color: white !important;
font-weight: 900 !important;
font-size: 3rem !important;
letter-spacing: -2px;
animation: slideInDown 0.8s ease-out;
}
h2 {
color: white !important;
font-weight: 800 !important;
animation: fadeInUp 0.6s ease-out;
}
h3, h4 {
color: #1e293b !important;
font-weight: 700 !important;
}

[data-testid="stMetric"] {
background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
backdrop-filter: blur(20px);
border-radius: 24px;
padding: 28px;
box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
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
background: linear-gradient(45deg, transparent, rgba(135, 206, 235, 0.1), transparent);
transform: rotate(45deg);
animation: shimmer 3s infinite;
}
@keyframes shimmer {
0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}
[data-testid="stMetric"]:hover {
transform: translateY(-12px) scale(1.03);
box-shadow: 0 20px 60px rgba(12, 74, 110, 0.25);
border: 1px solid #87CEEB;
}
[data-testid="stMetricValue"] {
font-size: 42px !important;
font-weight: 900 !important;
background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}
[data-testid="stMetricLabel"] {
color: #64748b !important;
font-weight: 700 !important;
font-size: 13px !important;
text-transform: uppercase;
letter-spacing: 1.5px;
}

.js-plotly-plot {
background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
border-radius: 28px;
padding: 20px;
box-shadow: 0 8px 32px rgba(0,0,0,0.08);
transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
border: 1px solid rgba(226, 232, 240, 0.8);
animation: fadeInUp 0.8s ease-out;
margin: 10px 0;
}
.js-plotly-plot:hover {
transform: translateY(-8px);
box-shadow: 0 16px 48px rgba(0,0,0,0.15);
border: 1px solid #87CEEB;
}

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
.hero-content { position: relative; z-index: 1; }
.hero-title {
color: white;
font-size: 3.5rem;
font-weight: 900;
margin: 0;
text-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.hero-subtitle {
color: #E6F0FA;
font-size: 1.3rem;
margin-top: 16px;
font-weight: 500;
}

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
margin-right: 12px;
}

.stTabs [data-baseweb="tab-list"] {
gap: 12px;
background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
padding: 12px;
border-radius: 20px;
}
.stTabs [data-baseweb="tab"] {
background: white;
border-radius: 14px;
padding: 12px 28px;
font-weight: 700;
transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
transform: translateY(-2px);
}
.stTabs [aria-selected="true"] {
background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%) !important;
color: white !important;
border: 2px solid #87CEEB;
}

@keyframes fadeInUp {
from { opacity: 0; transform: translateY(40px); }
to { opacity: 1; transform: translateY(0); }
}
@keyframes slideInDown {
from { opacity: 0; transform: translateY(-40px); }
to { opacity: 1; transform: translateY(0); }
}

::-webkit-scrollbar { width: 14px; }
::-webkit-scrollbar-track { background: linear-gradient(180deg, #f1f5f9, #e0f2fe); }
::-webkit-scrollbar-thumb {
background: linear-gradient(180deg, #87CEEB, #1F77B4);
border-radius: 10px;
border: 3px solid #f1f5f9;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
        df["Année"] = df["Année"].astype(int)
        df = df.groupby("Année", as_index=False).first()
        df = df.sort_values("Année").reset_index(drop=True)
        
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
        st.error("❌ Fichier introuvable")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
        return pd.DataFrame()

df = load_and_clean_data()
if df.empty:
    st.stop()

# Couleurs
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"
VERT = "#10B981"
ROUGE = "#EF4444"

plotly_config = {'displayModeBar': True, 'displaylogo': False}

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg'
    width='120' style='border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);'/>
    <h1 style='color: white; margin-top: 24px; font-size: 1.8rem;'>
    📊 Dashboard<br/>Mauritanie
    </h1>
    <p style='color: #E6F0FA; font-size: 0.9rem; margin-top: 12px;'>
    Analyse Macroéconomique
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["📍 Vue d'ensemble", "📈 Croissance & Inflation", "🌐 Secteur Externe", 
         "💼 Finances Publiques", "📊 Analyses Avancées"],
        label_visibility="visible"
    )
    
    st.markdown("### ⏱️ Filtres Temporels")
    year_range = st.slider("Période", int(df["Année"].min()), int(df["Année"].max()), (2000, 2024))
    
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 16px; margin-top: 30px;'>
    <p style='color: #E6F0FA; font-size: 0.85rem; margin: 0;'>
    <b>📊 Sources:</b><br/>• BCM<br/>• FMI & BM<br/>• 1960-2024
    </p>
    </div>
    """, unsafe_allow_html=True)

df_filtered = df[(df["Année"] >= year_range[0]) & (df["Année"] <= year_range[1])].copy()

# =====================================
# PAGE 1: VUE D'ENSEMBLE
# =====================================
if page == "📍 Vue d'ensemble":
    st.markdown(f"""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">Dashboard Macroéconomique</h1>
    <p class="hero-subtitle">République Islamique de Mauritanie • {year_range[0]}-{year_range[1]}</p>
    <div style='margin-top: 24px;'>
    <span class='badge'>✓ Actualisé 2026</span>
    <span class='badge'>✓ 14 Indicateurs</span>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Indicateurs Clés 2024")
    if 2024 in df["Année"].values:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0] if not df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].isna().iloc[0] else 0
            st.metric("📈 Croissance PIB", f"{val:.1f}%", delta="+1.9 pts")
        with col2:
            val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0] if not df.loc[df["Année"] == 2024, "Inflation_pct"].isna().iloc[0] else 0
            st.metric("🔥 Inflation", f"{val:.1f}%", delta="-1.4 pts", delta_color="inverse")
        with col3:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0] if not df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].isna().iloc[0] else 0
            st.metric("💼 Recettes", f"{val:.1f}% PIB", delta="+3.8 pts")
        with col4:
            dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9 if not df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].isna().iloc[0] else 0
            st.metric("🌐 Dette Ext.", f"{dette:.1f} Md$", delta="Stable", delta_color="off")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Évolution du PIB")
        df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        if len(df_pib) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"],
                mode='lines', name='Croissance',
                line=dict(color=BLEU_FONCE, width=3),
                hovertemplate='<b>%{x}</b><br>%{y:.2f}%<extra></extra>'
            ))
            fig.add_trace(go.Scatter(
                x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(5).mean(),
                mode='lines', name='Tendance',
                line=dict(color=BLEU_MOYEN, width=3, dash='dash'),
                hovertemplate='<b>%{x}</b><br>%{y:.2f}%<extra></extra>'
            ))
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise 2009", "COVID-19"]):
                if year in df_pib["Année"].values and year_range[0] <= year <= year_range[1]:
                    y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                    fig.add_annotation(
                        x=year, y=y_val, text=label, showarrow=True,
                        arrowhead=2, ax=0, ay=-40, font=dict(size=9)
                    )
            
            fig.update_layout(
                title="Croissance du PIB – cycles économiques<br><sub>Source: BCM, FMI</sub>",
                yaxis_title="Croissance (%)", hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                height=400, showlegend=True
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    with col2:
        st.markdown("#### 🔥 Inflation")
        df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
        if len(df_infl) > 0:
            median = df_infl["Inflation_pct"].median()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_infl["Année"], y=df_infl["Inflation_pct"],
                mode='lines', name='Inflation',
                line=dict(color=BLEU_FONCE, width=3),
                fill='tonexty', fillcolor='rgba(174,199,232,0.2)',
                hovertemplate='<b>%{x}</b><br>%{y:.2f}%<extra></extra>'
            ))
            fig.add_hline(y=median, line_dash="dash", line_color=BLEU_MOYEN,
                         annotation_text=f"Médiane ({median:.1f}%)")
            
            fig.update_layout(
                title="Inflation – régimes macroéconomiques<br><sub>Source: BCM, FMI</sub>",
                yaxis_title="Inflation (%)", hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    st.markdown("### 💰 Balance Commerciale")
    df_bc = df_filtered.dropna(subset=["Solde_commercial_pct_PIB"])
    if len(df_bc) > 0:
        colors = [VERT if x >= 0 else ROUGE for x in df_bc["Solde_commercial_pct_PIB"]]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_bc["Année"], y=df_bc["Solde_commercial_pct_PIB"],
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>%{y:.2f}% PIB<extra></extra>'
        ))
        fig.add_hline(y=0, line_color='#475569', line_width=2)
        fig.update_layout(
            title="Balance Commerciale (% PIB)<br><sub>Source: Banque Mondiale</sub>",
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)',
            height=400, showlegend=False
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# =====================================
# PAGE 2: CROISSANCE & INFLATION
# =====================================
elif page == "📈 Croissance & Inflation":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">📈 Croissance & Inflation</h1>
    <p class="hero-subtitle">Analyse des cycles économiques</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Cycles", "🔥 Régimes", "💹 Phillips"])
    
    with tab1:
        st.markdown("### 🔄 Croissance du PIB")
        df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
        if len(df_pib) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"],
                mode='lines+markers', name='Croissance',
                line=dict(color=BLEU_FONCE, width=3),
                marker=dict(size=6)
            ))
            fig.add_trace(go.Scatter(
                x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(10).mean(),
                mode='lines', name='Tendance 10 ans',
                line=dict(color=BLEU_MOYEN, width=3, dash='dash')
            ))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.update_layout(
                title="Croissance du PIB<br><sub>Source: BCM, FMI</sub>",
                yaxis_title="Croissance (%)", height=500,
                plot_bgcolor='rgba(0,0,0,0)', hovermode='x unified'
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📊 Moyenne", f"{df_pib['Croissance_PIB_pct'].mean():.2f}%")
            col2.metric("📈 Maximum", f"{df_pib['Croissance_PIB_pct'].max():.2f}%")
            col3.metric("📉 Minimum", f"{df_pib['Croissance_PIB_pct'].min():.2f}%")
            col4.metric("📏 Écart-type", f"{df_pib['Croissance_PIB_pct'].std():.2f}%")
    
    with tab2:
        st.markdown("### 🔥 Distribution de l'Inflation")
        df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
        if len(df_infl) > 0:
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=df_infl["Inflation_pct"], nbinsx=20,
                marker_color=BLEU_MOYEN, opacity=0.7,
                hovertemplate='Inflation: %{x:.1f}%<br>Fréquence: %{y}<extra></extra>'
            ))
            fig.update_layout(
                title="Distribution de l'inflation<br><sub>Source: BCM</sub>",
                xaxis_title="Inflation (%)", yaxis_title="Fréquence",
                plot_bgcolor='rgba(0,0,0,0)', height=400
            )
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    with tab3:
        st.markdown("### 💹 Courbe de Phillips")
        df_ph = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        if len(df_ph) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_ph["Taux_chomage_pct"], y=df_ph["Inflation_pct"],
                mode='markers', text=df_ph["Année"],
                marker=dict(size=12, color=df_ph["Année"], colorscale='Blues',
                           showscale=True, colorbar=dict(title="Année")),
                hovertemplate='Année: %{text}<br>Chômage: %{x:.1f}%<br>Inflation: %{y:.1f}%<extra></extra>'
            ))
            fig.update_layout(
                title="Courbe de Phillips<br><sub>Source: BCM</sub>",
                xaxis_title="Chômage (%)", yaxis_title="Inflation (%)",
                plot_bgcolor='rgba(0,0,0,0)', height=500
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# =====================================
# PAGE 3: SECTEUR EXTERNE
# =====================================
elif page == "🌐 Secteur Externe":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">🌐 Secteur Externe</h1>
    <p class="hero-subtitle">Dette, réserves et soutenabilité</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💰 Dette Extérieure vs Réserves")
    df_ext = df_filtered.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"])
    if len(df_ext) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9,
            mode='lines', name='Dette extérieure',
            line=dict(color=ROUGE, width=3),
            hovertemplate='<b>%{x}</b><br>%{y:.2f} Md$<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=df_ext["Année"], y=df_ext["Reserves_internationales_USD"]/1e9,
            mode='lines', name='Réserves',
            line=dict(color=VERT, width=3),
            hovertemplate='<b>%{x}</b><br>%{y:.2f} Md$<extra></extra>'
        ))
        fig.update_layout(
            title="Dette Extérieure vs Réserves Internationales<br><sub>Source: Banque Mondiale</sub>",
            yaxis_title="Milliards USD", hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)', height=500
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        
        if len(df_ext) > 0:
            latest = df_ext.iloc[-1]
            ratio = (latest["Dette_exterieure_USD"] / latest["Reserves_internationales_USD"]) if latest["Reserves_internationales_USD"] > 0 else 0
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Ratio Dette/Réserves", f"{ratio:.2f}x")
            col2.metric("💵 Dette", f"{latest['Dette_exterieure_USD']/1e9:.2f} Md$")
            col3.metric("🏦 Réserves", f"{latest['Reserves_internationales_USD']/1e9:.2f} Md$")
    
    st.markdown("### 📦 Solde Commercial")
    df_bc = df_filtered.dropna(subset=["Solde_commercial_pct_PIB"])
    if len(df_bc) > 0:
        colors = [VERT if x >= 0 else ROUGE for x in df_bc["Solde_commercial_pct_PIB"]]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_bc["Année"], y=df_bc["Solde_commercial_pct_PIB"],
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>%{y:.2f}% PIB<extra></extra>'
        ))
        fig.add_hline(y=0, line_color='#475569', line_width=2)
        fig.update_layout(
            title="Solde Commercial (% PIB)<br><sub>Source: Banque Mondiale</sub>",
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=400
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    st.markdown("### 💸 Envois de Fonds")
    df_ef = df_filtered.dropna(subset=["Envois_de_fonds_pct_PIB"])
    if len(df_ef) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_ef["Année"], y=df_ef["Envois_de_fonds_pct_PIB"],
            mode='lines+markers', line=dict(color=BLEU_FONCE, width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>%{y:.2f}% PIB<extra></extra>'
        ))
        fig.update_layout(
            title="Envois de Fonds (% PIB)<br><sub>Source: Banque Mondiale</sub>",
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=400
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# =====================================
# PAGE 4: FINANCES PUBLIQUES
# =====================================
elif page == "💼 Finances Publiques":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">💼 Finances Publiques</h1>
    <p class="hero-subtitle">Recettes fiscales et viabilité budgétaire</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💼 Évolution des Recettes Fiscales")
    df_rf = df_filtered.dropna(subset=["Recettes_fiscales_pct_PIB"])
    if len(df_rf) > 0:
        moyenne = df_rf["Recettes_fiscales_pct_PIB"].mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_rf["Année"], y=df_rf["Recettes_fiscales_pct_PIB"],
            mode='lines+markers', line=dict(color=BLEU_FONCE, width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>%{y:.2f}% PIB<extra></extra>'
        ))
        fig.add_hline(y=moyenne, line_dash="dash", line_color=BLEU_MOYEN,
                     annotation_text=f"Moyenne ({moyenne:.1f}%)")
        fig.update_layout(
            title="Recettes Fiscales (% PIB)<br><sub>Source: FMI</sub>",
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=500
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Structure 2024")
        if 2024 in df["Année"].values:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
            if pd.notna(val):
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=["Recettes fiscales", "Autres"],
                    values=[val, 100-val],
                    marker=dict(colors=[BLEU_MOYEN, BLEU_CLAIR]),
                    hovertemplate='%{label}: %{value:.1f}%<extra></extra>'
                ))
                fig.update_layout(
                    title="Poids des recettes fiscales 2024",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    with col2:
        st.markdown("#### Évolution 2007-2024")
        df_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
        if len(df_bar) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_bar["Année"], y=df_bar["Recettes_fiscales_pct_PIB"],
                marker_color=BLEU_MOYEN,
                hovertemplate='<b>%{x}</b><br>%{y:.2f}% PIB<extra></extra>'
            ))
            fig.update_layout(
                title="Recettes Fiscales 2007-2024",
                yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=400
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    st.markdown("### 👥 Croissance vs Chômage")
    df_cc = df_filtered.dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
    if len(df_cc) > 0:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_cc["Année"], y=df_cc["Croissance_PIB_pct"],
            name='Croissance PIB', marker_color=BLEU_MOYEN,
            hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            x=df_cc["Année"], y=df_cc["Taux_chomage_pct"],
            name='Chômage', marker_color=BLEU_CLAIR,
            hovertemplate='<b>%{x}</b><br>Chômage: %{y:.1f}%<extra></extra>'
        ))
        fig.update_layout(
            title="Croissance vs Chômage<br><sub>Source: BCM</sub>",
            yaxis_title="%", barmode='group',
            plot_bgcolor='rgba(0,0,0,0)', height=500
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# =====================================
# PAGE 5: ANALYSES AVANCÉES
# =====================================
elif page == "📊 Analyses Avancées":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">📊 Analyses Avancées</h1>
    <p class="hero-subtitle">Corrélations et analyses multidimensionnelles</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔥 Heatmap", "🎲 Trajectoire 3D", "📈 Multi-analyse"])
    
    with tab1:
        st.markdown("### 🔥 Matrice de Corrélation")
        corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
        df_corr = df_filtered[corr_vars].dropna()
        if len(df_corr) > 5:
            corr = df_corr.corr()
            fig = go.Figure()
            fig.add_trace(go.Heatmap(
                z=corr.values, x=corr.columns, y=corr.columns,
                colorscale='Blues', text=corr.values,
                texttemplate='%{text:.2f}', textfont={"size": 12},
                hovertemplate='%{y} vs %{x}<br>Corrélation: %{z:.2f}<extra></extra>'
            ))
            fig.update_layout(
                title="Corrélations entre indicateurs<br><sub>Source: Calculs propres</sub>",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    with tab2:
        st.markdown("### 🎲 Trajectoire Macroéconomique 3D")
        df_3d = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
        if len(df_3d) > 5:
            fig = go.Figure()
            fig.add_trace(go.Scatter3d(
                x=df_3d["Inflation_pct"], y=df_3d["Taux_chomage_pct"], 
                z=df_3d["Croissance_PIB_pct"],
                mode='markers+lines', marker=dict(
                    size=8, color=df_3d["Année"], colorscale='Blues',
                    showscale=True, colorbar=dict(title="Année")
                ),
                line=dict(color=BLEU_FONCE, width=2),
                text=df_3d["Année"],
                hovertemplate='Année: %{text}<br>Inflation: %{x:.1f}%<br>Chômage: %{y:.1f}%<br>Croissance: %{z:.1f}%<extra></extra>'
            ))
            fig.update_layout(
                title="Trajectoire 3D<br><sub>Source: Calculs propres</sub>",
                scene=dict(
                    xaxis_title="Inflation (%)",
                    yaxis_title="Chômage (%)",
                    zaxis_title="Croissance (%)"
                ),
                height=600
            )
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    with tab3:
        st.markdown("### 📈 Pression Macroéconomique")
        df_area = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        if len(df_area) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_area["Année"], y=df_area["Inflation_pct"],
                mode='lines', name='Inflation',
                fill='tonexty', fillcolor='rgba(174,199,232,0.4)',
                line=dict(color=BLEU_CLAIR, width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df_area["Année"], y=df_area["Taux_chomage_pct"],
                mode='lines', name='Chômage',
                fill='tonexty', fillcolor='rgba(31,119,180,0.4)',
                line=dict(color=BLEU_MOYEN, width=2)
            ))
            fig.update_layout(
                title="Pression macroéconomique<br><sub>Source: BCM, FMI</sub>",
                yaxis_title="%", plot_bgcolor='rgba(0,0,0,0)', height=400
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# =====================================
# FOOTER
# =====================================
st.markdown("""
<div style='text-align: center; padding: 48px; margin-top: 60px; background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; color: white;'>
<h2 style="color: white; margin: 0; font-size: 1.5rem;">Dashboard Macroéconomique de la Mauritanie</h2>
<p style="margin: 16px 0 8px 0; font-size: 1.1rem; color: #E6F0FA;">
<b>Jedou Mohamed Bebacar</b> | Master SSD | Université de Nouakchott
</p>
<p style="margin: 8px 0 0 0; font-size: 0.95rem; color: #AEC7E8;">
© 2026 • Visualisations Interactives • Multi-sources • Actualisé janvier 2026
</p>
</div>
""", unsafe_allow_html=True)
