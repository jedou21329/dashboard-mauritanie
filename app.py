# app.py - Dashboard Macroéconomique Mauritanie - 14 Visualisations Interactives
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# CONFIGURATION PAGE
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ULTRA-MODERNE
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
h2 { color: white !important; font-weight: 800 !important; }
h3, h4 { color: #1e293b !important; font-weight: 700 !important; }

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
top: -50%; left: -50%;
width: 200%; height: 200%;
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
top: -50%; right: -50%;
width: 200%; height: 200%;
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

# CHARGEMENT DES DONNÉES
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
        df["Année"] = df["Année"].astype(int)
        df = df.groupby("Année", as_index=False).first()
        df = df.sort_values("Année").reset_index(drop=True)
        
        # Imputation intelligente
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
        st.error("❌ Fichier 'macro_mauritanie_complet_1960_2024.csv' introuvable")
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
BLEU_TRES_CLAIR = "#E6F0FA"
VERT = "#10B981"
ROUGE = "#EF4444"

# Configuration Plotly
plotly_config = {
    'displayModeBar': True, 
    'displaylogo': False,
    'modeBarButtonsToAdd': ['pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d'],
    'scrollZoom': True
}

def apply_plotly_theme(fig, title, height=450):
    """Applique le thème unifié à tous les graphiques"""
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 16, 'color': BLEU_FONCE, 'family': 'Inter', 'weight': 600}
        },
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        height=height,
        hovermode='x unified',
        font=dict(family='Inter', color=BLEU_FONCE, size=11),
        margin=dict(l=60, r=40, t=100, b=60),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.15,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=BLEU_FONCE,
            borderwidth=1
        )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=0.5,
        showline=True,
        linecolor=BLEU_FONCE,
        linewidth=1.5,
        zeroline=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=0.5,
        showline=True,
        linecolor=BLEU_FONCE,
        linewidth=1.5,
        zeroline=False
    )
    
    return fig

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg'
    width='120' style='border-radius: 16px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);'/>
    <h1 style='color: white; margin-top: 24px; font-size: 1.8rem;'>
    📊 Dashboard<br/>Mauritanie
    </h1>
    <p style='color: #E6F0FA; font-size: 0.9rem; margin-top: 12px;'>
    14 Visualisations Interactives
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
    <b>📊 Sources:</b><br/>• BCM<br/>• FMI & Banque Mondiale<br/>• 1960-2024
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
    <span class='badge'>✓ 14 Visualisations</span>
    <span class='badge'>✓ Interactif</span>
    <span class='badge'>✓ Actualisé 2026</span>
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
    
    # VIS 1: Croissance du PIB avec cycles
    st.markdown("### 📈 Visualisation 1 – Croissance du PIB avec cycles économiques")
    df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
    if len(df_pib) > 0:
        fig = go.Figure()
        
        # Zone négative
        fig.add_trace(go.Scatter(
            x=df_pib["Année"],
            y=[0]*len(df_pib),
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_pib["Année"],
            y=df_pib["Croissance_PIB_pct"],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(174, 199, 232, 0.3)',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Ligne principale
        fig.add_trace(go.Scatter(
            x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"],
            mode='lines', name='Croissance PIB',
            line=dict(color=BLEU_FONCE, width=2.5),
            hovertemplate='<b>%{x}</b><br>Croissance: %{y:.2f}%<extra></extra>'
        ))
        
        # Tendance long terme
        fig.add_trace(go.Scatter(
            x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(10, min_periods=1).mean(),
            mode='lines', name='Tendance long terme (10 ans)',
            line=dict(color=BLEU_MOYEN, width=3),
            hovertemplate='<b>%{x}</b><br>Tendance: %{y:.2f}%<extra></extra>'
        ))
        
        # Ligne zéro
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, line_width=1)
        
        # Annotations des crises
        annotations_data = [
            (1975, "Choc pétrolier", -50),
            (2009, "Crise financière", -50),
            (2020, "COVID-19", -50)
        ]
        
        for year, label, ay in annotations_data:
            if year in df_pib["Année"].values and year_range[0] <= year <= year_range[1]:
                y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                fig.add_annotation(
                    x=year, y=y_val, text=label,
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,
                    arrowcolor=BLEU_FONCE, ax=0, ay=ay,
                    font=dict(size=10, color=BLEU_FONCE, weight=600),
                    bgcolor='rgba(255,255,255,0.9)', bordercolor=BLEU_FONCE, borderwidth=1.5
                )
        
        fig = apply_plotly_theme(fig, "Croissance du PIB – cycles économiques et chocs<br><sub>Source : BCM, FMI, Banque Mondiale</sub>", 450)
        fig.update_yaxes(title_text="%")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 2: Inflation – régimes
    st.markdown("### 🔥 Visualisation 2 – Inflation et régimes macroéconomiques")
    df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
    if len(df_infl) > 0:
        median = df_infl["Inflation_pct"].median()
        
        fig = go.Figure()
        
        # Zone de régime inflation élevée
        df_high = df_infl.copy()
        df_high.loc[df_high["Inflation_pct"] <= median, "Inflation_pct"] = median
        
        fig.add_trace(go.Scatter(
            x=df_infl["Année"], 
            y=[median] * len(df_infl),
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_high["Année"], 
            y=df_high["Inflation_pct"],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(174, 199, 232, 0.4)',
            line=dict(width=0),
            name='Régime inflation élevée',
            hoverinfo='skip'
        ))
        
        # Ligne principale
        fig.add_trace(go.Scatter(
            x=df_infl["Année"], y=df_infl["Inflation_pct"],
            mode='lines', name='Inflation',
            line=dict(color=BLEU_FONCE, width=2.5),
            hovertemplate='<b>%{x}</b><br>Inflation: %{y:.2f}%<extra></extra>'
        ))
        
        # Ligne médiane
        fig.add_hline(
            y=median, line_dash="dash", line_color=BLEU_MOYEN, line_width=2,
            annotation_text=f"Inflation médiane ({median:.1f}%)",
            annotation_position="top right",
            annotation=dict(font=dict(size=11, color=BLEU_MOYEN, weight=600))
        )
        
        fig = apply_plotly_theme(fig, "Inflation – régimes macroéconomiques<br><sub>Source : BCM, FMI</sub>", 450)
        fig.update_yaxes(title_text="%")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 10: Moyennes par décennie
    st.markdown("### 📊 Visualisation 10 – Indicateurs moyens par décennie (depuis 2000)")
    df_2000 = df[df["Année"] >= 2000].copy()
    df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
    dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean().reset_index()
    
    if len(dec) > 0:
        fig = go.Figure()
        x_labels = [f"{int(d)}s" for d in dec["Décennie"]]
        
        fig.add_trace(go.Bar(
            x=x_labels, y=dec["Croissance_PIB_pct"],
            name='Croissance PIB', marker_color=BLEU_FONCE,
            text=dec["Croissance_PIB_pct"].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Croissance PIB: %{y:.1f}%<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            x=x_labels, y=dec["Inflation_pct"],
            name='Inflation', marker_color=BLEU_MOYEN,
            text=dec["Inflation_pct"].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Inflation: %{y:.1f}%<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            x=x_labels, y=dec["Taux_chomage_pct"],
            name='Chômage', marker_color=BLEU_CLAIR,
            text=dec["Taux_chomage_pct"].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Chômage: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(barmode='group')
        fig = apply_plotly_theme(fig, "Indicateurs macroéconomiques – moyennes par décennie<br><sub>Source: Calculs propres</sub>", 500)
        fig.update_yaxes(title_text="Pourcentage (%)")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# ===========================
# PAGE 2: CROISSANCE & INFLATION
# ===========================
elif page == "📈 Croissance & Inflation":

    st.markdown("""
    <div class="hero-header">
        <div class="hero-content">
            <h1 class="hero-title">📈 Croissance & Inflation</h1>
            <p class="hero-subtitle">Analyse des cycles économiques et dynamiques des prix</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Volatilité", "🔥 Distribution Inflation", "💹 Courbe de Phillips", "📦 Boxplot Périodes"]
    )

    # =====================================================
    # TAB 1 – VOLATILITÉ (INCHANGÉ)
    # =====================================================
    with tab1:
        st.markdown("### 📉 Volatilité de la croissance du PIB")

        df_pib = df_filtered.dropna(subset=["Croissance_PIB_pct"])

        if len(df_pib) > 10:
            mean = df_pib["Croissance_PIB_pct"].rolling(10).mean()
            std = df_pib["Croissance_PIB_pct"].rolling(10).std()

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=mean,
                name="Moyenne mobile (10 ans)",
                line=dict(color=BLEU_FONCE, width=3)
            ))

            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=mean + std,
                line=dict(width=0),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=df_pib["Année"],
                y=mean - std,
                fill="tonexty",
                fillcolor="rgba(174,199,232,0.4)",
                line=dict(width=0),
                name="±1 écart-type"
            ))

            fig = apply_plotly_theme(
                fig,
                "Volatilité de la croissance du PIB<br><sub>Source : Banque Mondiale</sub>",
                height=450
            )
            fig.update_yaxes(title="%")

            st.plotly_chart(fig, use_container_width=True, config=plotly_config)

    # =====================================================
    # TAB 2 – DISTRIBUTION DE L’INFLATION (PROFESSIONNELLE)
    # =====================================================
    with tab2:
        st.markdown("### 🔥 Distribution Inflation")

        df_inf = df_filtered.dropna(subset=["Inflation_pct"])

        if len(df_inf) > 0:
            col1, col2 = st.columns([3, 1])

            # --- Densité + moyenne ---
            with col1:
                fig = go.Figure()

                fig.add_trace(go.Histogram(
                    x=df_inf["Inflation_pct"],
                    histnorm="probability density",
                    nbinsx=30,
                    marker_color=BLEU_TRES_CLAIR,
                    opacity=0.6,
                    showlegend=False
                ))

                fig.add_trace(go.Scatter(
                    x=np.sort(df_inf["Inflation_pct"]),
                    y=np.exp(
                        -0.5 * (
                            (np.sort(df_inf["Inflation_pct"]) - df_inf["Inflation_pct"].mean())
                            / df_inf["Inflation_pct"].std()
                        ) ** 2
                    ) / (df_inf["Inflation_pct"].std() * np.sqrt(2 * np.pi)),
                    line=dict(color=BLEU_FONCE, width=3),
                    name="Densité"
                ))

                fig.add_vline(
                    x=df_inf["Inflation_pct"].mean(),
                    line=dict(color=BLEU_MOYEN, dash="dash"),
                    annotation_text="Moyenne",
                    annotation_position="top"
                )

                fig = apply_plotly_theme(
                    fig,
                    "Distribution de l’inflation<br><sub>Source : BCM</sub>",
                    height=420
                )
                fig.update_xaxes(title="Inflation (%)")
                fig.update_yaxes(title="Densité")

                st.plotly_chart(fig, use_container_width=True, config=plotly_config)

            # --- Boxplot vertical sobre ---
            with col2:
                fig = go.Figure()

                fig.add_trace(go.Box(
                    y=df_inf["Inflation_pct"],
                    marker_color=BLEU_FONCE,
                    boxmean=True
                ))

                fig = apply_plotly_theme(
                    fig,
                    "Résumé statistique",
                    height=420
                )
                fig.update_yaxes(title="Inflation (%)")

                st.plotly_chart(fig, use_container_width=True, config=plotly_config)

    # =====================================================
    # TAB 3 – COURBE DE PHILLIPS (TOUTES LES ANNÉES)
    # =====================================================
    with tab3:
        st.markdown("### 💹 Courbe de Phillips – Mauritanie")

        df_ph = df_filtered.dropna(
            subset=["Inflation_pct", "Taux_chomage_pct", "Année"]
        )

        if len(df_ph) > 0:
            fig = go.Figure()
            years = df_ph["Année"].sort_values().unique()
            fig.add_trace(go.Scatter(
                x=df_ph["Taux_chomage_pct"],
                y=df_ph["Inflation_pct"],
                mode="markers",
                text=df_ph["Année"],
                marker=dict(
                    size=9,
                    color=df_ph["Année"],
                    colorscale="Blues",
                    cmin=years.min(),
                    cmax=years.max(),
                    showscale=True,
                    colorbar=dict(
                        title="Année",
                        thickness=22,
                        len=0.85,
                        tickmode="array",
                        tickvals=[2000, 2005, 2010, 2015, 2020],
                        ticktext=[str(y) for y in years[::2]]
                    ),
                    line=dict(color=BLEU_FONCE, width=0.5)
                ),
                hovertemplate=(
                    "Année : %{text}<br>"
                    "Chômage : %{x:.1f}%<br>"
                    "Inflation : %{y:.1f}%<extra></extra>"
                )
            ))

            fig = apply_plotly_theme(
                fig,
                "Courbe de Phillips – Mauritanie<br><sub>Source : BCM</sub>",
                height=430
            )
            fig.update_xaxes(title="Chômage (%)")
            fig.update_yaxes(title="Inflation (%)")

            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        else:
            st.info("📊 Données insuffisantes pour la courbe de Phillips")

    # =====================================================
    # TAB 4 – BOXPLOT PAR PÉRIODE (VALIDÉ – INCHANGÉ)
    # =====================================================
    with tab4:
        st.markdown("### 📦 Distribution de la croissance du PIB par période")

        df_box = df.copy()
        df_box["Période"] = pd.cut(
            df_box["Année"],
            bins=[1960, 1980, 2000, 2024],
            labels=["1960–1980", "1981–2000", "2001–2024"]
        )
        df_box = df_box.dropna(subset=["Croissance_PIB_pct", "Période"])

        fig = go.Figure()
        couleurs = [BLEU_CLAIR, BLEU_MOYEN, BLEU_FONCE]

        for periode, couleur in zip(df_box["Période"].cat.categories, couleurs):
            fig.add_trace(go.Box(
                y=df_box[df_box["Période"] == periode]["Croissance_PIB_pct"],
                name=str(periode),
                marker_color=couleur,
                boxmean=True
            ))

        fig = apply_plotly_theme(
            fig,
            "Distribution de la croissance du PIB par période<br><sub>Source : Banque Mondiale</sub>",
            height=480
        )
        fig.update_yaxes(title="Croissance (%)")

        st.plotly_chart(fig, use_container_width=True, config=plotly_config)


# ===================================== 
# PAGE 3: SECTEUR EXTERNE
# =====================================
elif page == "🌐 Secteur Externe":
    st.markdown("""
    <div class="hero-header">
    <div class="hero-content">
    <h1 class="hero-title">🌐 Secteur Externe</h1>
    <p class="hero-subtitle">Dette, réserves, balance commerciale et envois de fonds</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # VIS 3: Dette vs Réserves
    st.markdown("### 💰 Soutenabilité externe : dette vs réserves")
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
        
        # Zone de vulnérabilité
        fig.add_trace(go.Scatter(
            x=df_ext["Année"], 
            y=df_ext["Dette_exterieure_USD"]/1e9,
            fill='tonexty',
            fillcolor='rgba(174,199,232,0.3)',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title="Soutenabilité externe : dette vs réserves<br><sub>Source: Banque Mondiale</sub>",
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
            col1.metric("📊 Ratio Dette/Réserves", f"{ratio:.2f}x", help="Ratio < 3 = soutenable")
            col2.metric("💵 Dette", f"{latest['Dette_exterieure_USD']/1e9:.2f} Md$")
            col3.metric("🏦 Réserves", f"{latest['Reserves_internationales_USD']/1e9:.2f} Md$")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Balance commerciale
    st.markdown("### 📦 Solde Commercial (% du PIB)")
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
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=450
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Envois de fonds
    st.markdown("### 💸 Envois de Fonds (% du PIB)")
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
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=450
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
    <p class="hero-subtitle">Recettes fiscales, dépenses et viabilité budgétaire</p>
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
                     annotation_text=f"Moyenne ({moyenne:.1f}%)", annotation_position="right")
        fig.update_layout(
            title="Recettes Fiscales (% PIB)<br><sub>Source: FMI</sub>",
            yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=500
        )
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # VIS 6: Pie chart 2024
        st.markdown("#### 🥧 Structure des recettes 2024")
        if 2024 in df["Année"].values:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
            if pd.notna(val):
                fig = go.Figure()
                fig.add_trace(go.Pie(
                    labels=["Recettes fiscales", "Autres"],
                    values=[val, 100-val],
                    marker=dict(colors=[BLEU_MOYEN, BLEU_TRES_CLAIR]),
                    hovertemplate='%{label}: %{value:.1f}%<extra></extra>',
                    textinfo='label+percent'
                ))
                fig.update_layout(
                    title="Poids des recettes fiscales – 2024<br><sub>Source: FMI (2023)</sub>",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, config=plotly_config)
            else:
                st.info("📊 Données non disponibles")
    
    with col2:
        # VIS 14: Recettes 3D (converti en bar chart animé)
        st.markdown("#### 📊 Recettes Fiscales 2007-2024")
        df_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
        if len(df_bar) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_bar["Année"], y=df_bar["Recettes_fiscales_pct_PIB"],
                marker_color=BLEU_MOYEN,
                hovertemplate='<b>%{x}</b><br>%{y:.2f}% PIB<extra></extra>',
                text=df_bar["Recettes_fiscales_pct_PIB"].apply(lambda x: f"{x:.1f}%"),
                textposition='outside'
            ))
            fig.update_layout(
                title="Recettes Fiscales 2007-2024<br><sub>Source: FMI</sub>",
                yaxis_title="% PIB", plot_bgcolor='rgba(0,0,0,0)', height=400
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # VIS 4: Croissance vs Chômage (barres côte à côte)
    st.markdown("### 👥 Croissance économique et chômage (2007–2021)")
    df_cc = df_filtered.dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
    if len(df_cc) > 0:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_cc["Année"], y=df_cc["Croissance_PIB_pct"],
            name='Croissance PIB', marker_color=BLEU_MOYEN,
            text=df_cc["Croissance_PIB_pct"].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            x=df_cc["Année"], y=df_cc["Taux_chomage_pct"],
            name='Chômage', marker_color=BLEU_CLAIR,
            text=df_cc["Taux_chomage_pct"].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Chômage: %{y:.1f}%<extra></extra>'
        ))
        fig.update_layout(
            title="Croissance économique et chômage (2007–2021)<br><sub>Source: BCM</sub>",
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
    <p class="hero-subtitle">Corrélations, trajectoires 3D et analyses multidimensionnelles</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Heatmap", "🎲 Trajectoire 3D", "📈 Multi-analyse", "📊 Régimes"])
    
    with tab1:
        # VIS 7: Heatmap de corrélation
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
                title="Corrélations entre indicateurs macroéconomiques (2007–2024)<br><sub>Source: Calculs propres</sub>",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        else:
            st.info("📊 Données insuffisantes pour calculer les corrélations")
    
    with tab2:
        # VIS 13: Trajectoire 3D
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
                    size=8, 
                    color=df_3d["Année"], 
                    colorscale='Blues',
                    showscale=True, 
                    colorbar=dict(title="Année")
                ),
                line=dict(color=BLEU_FONCE, width=2),
                text=df_3d["Année"],
                hovertemplate='Année: %{text}<br>Inflation: %{x:.1f}%<br>Chômage: %{y:.1f}%<br>Croissance: %{z:.1f}%<extra></extra>'
            ))
            fig.update_layout(
                title="Trajectoire macroéconomique 3D (depuis 2000)<br><sub>Source: Calculs propres</sub>",
                scene=dict(
                    xaxis_title="Inflation (%)",
                    yaxis_title="Chômage (%)",
                    zaxis_title="Croissance (%)"
                ),
                height=600
            )
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        else:
            st.info("📊 Données insuffisantes pour la visualisation 3D")
    
    with tab3:
        # VIS 8: Stackplot – Pression macro
        st.markdown("### 📈 Pression Macroéconomique")
        df_area = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
        if len(df_area) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_area["Année"], y=df_area["Inflation_pct"],
                mode='lines', name='Inflation',
                fill='tonexty', fillcolor='rgba(174,199,232,0.4)',
                line=dict(color=BLEU_CLAIR, width=2),
                hovertemplate='<b>%{x}</b><br>Inflation: %{y:.1f}%<extra></extra>'
            ))
            fig.add_trace(go.Scatter(
                x=df_area["Année"], y=df_area["Taux_chomage_pct"],
                mode='lines', name='Chômage',
                fill='tonexty', fillcolor='rgba(31,119,180,0.4)',
                line=dict(color=BLEU_MOYEN, width=2),
                hovertemplate='<b>%{x}</b><br>Chômage: %{y:.1f}%<extra></extra>'
            ))
            fig.update_layout(
                title="Pression macroéconomique : inflation et chômage<br><sub>Source: BCM, FMI</sub>",
                yaxis_title="%", plot_bgcolor='rgba(0,0,0,0)', height=450
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        else:
            st.info("📊 Pas de données disponibles")
    
    with tab4:
        # VIS 12: Régimes macro (scatter)
        st.markdown("### 📊 Régimes Macroéconomiques (Inflation vs Croissance)")
        df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
        if len(df_2000) > 0:
            median_infl = df_2000["Inflation_pct"].median()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_2000["Inflation_pct"], 
                y=df_2000["Croissance_PIB_pct"],
                mode='markers', 
                text=df_2000["Année"],
                marker=dict(
                    size=12, 
                    color=df_2000["Année"], 
                    colorscale='Blues',
                    showscale=True, 
                    colorbar=dict(title="Année"),
                    line=dict(color='black', width=1)
                ),
                hovertemplate='Année: %{text}<br>Inflation: %{x:.1f}%<br>Croissance: %{y:.1f}%<extra></extra>'
            ))
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=median_infl, line_dash="dash", line_color="gray", opacity=0.5,
                         annotation_text=f"Médiane ({median_infl:.1f}%)")
            
            fig.update_layout(
                title="Régimes macroéconomiques (Inflation vs Croissance)<br><sub>Source: Calculs propres</sub>",
                xaxis_title="Inflation (%)", 
                yaxis_title="Croissance (%)",
                plot_bgcolor='rgba(0,0,0,0)', 
                height=500
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        else:
            st.info("📊 Pas de données disponibles depuis 2000")

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
© 2026 • 14 Visualisations Interactives • Multi-sources • Actualisé janvier 2026
</p>
<p style="margin: 12px 0 0 0; font-size: 0.85rem; color: #87CEEB;">
🛠️ Développé avec Streamlit & Plotly • 🔄 Données BCM, FMI, Banque Mondiale
</p>
</div>
""", unsafe_allow_html=True)
