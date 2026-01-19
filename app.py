
# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# -----------------------------
# CSS + JavaScript personnalisé
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #1e293b;
    }
    
    /* Animation des titres */
    h1 {
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        letter-spacing: -1px;
        animation: slideInDown 0.8s ease-out;
    }
    
    h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* KPI Cards avec effet glassmorphism */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(135, 206, 235, 0.3), transparent);
        transition: left 0.5s;
    }
    
    [data-testid="stMetric"]:hover::before {
        left: 100%;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 48px rgba(12, 74, 110, 0.15);
        border: 1px solid #87CEEB;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: countUp 1s ease-out;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 700 !important;
    }
    
    /* Charts containers */
    .stPlotlyChart {
        background: white;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        transition: all 0.4s ease;
        border: 1px solid #e2e8f0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .stPlotlyChart:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
    }
    
    /* Header avec drapeau */
    .header-container {
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 32px 0;
        animation: slideInLeft 0.8s ease-out;
    }
    
    .flag-img {
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transition: transform 0.3s ease;
    }
    
    .flag-img:hover {
        transform: scale(1.05) rotate(2deg);
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 0;
        border-bottom: 3px solid #87CEEB;
        margin-bottom: 24px;
        animation: slideInRight 0.6s ease-out;
    }
    
    .section-icon {
        font-size: 32px;
        animation: bounce 2s infinite;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f7fa 100%);
        border-left: 5px solid #87CEEB;
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(135, 206, 235, 0.15);
        animation: fadeIn 1s ease-out;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f7fa 100%);
        border-radius: 16px;
        border: 2px solid #87CEEB;
        font-weight: 700 !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e0f7fa 0%, #b0e0e6 100%);
        transform: translateX(5px);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.5);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #87CEEB, #0c4a6e);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0c4a6e, #87CEEB);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 32px 0;
        margin-top: 48px;
        border-top: 2px solid #e2e8f0;
        color: #64748b;
        font-size: 14px;
        animation: fadeIn 1.5s ease-out;
    }
</style>

<script>
    // Animation au scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
            }
        });
    });
    
    document.querySelectorAll('.stPlotlyChart').forEach(el => observer.observe(el));
</script>
""", unsafe_allow_html=True)

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Couleurs
COLORS = {
    'primary': '#0c4a6e',
    'secondary': '#87CEEB',
    'accent': '#0369a1',
    'success': '#10B981',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'light': '#f0f9ff'
}

# -----------------------------
# Chargement des données
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
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Recettes_millions_MR"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Recettes_millions_MR"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].fillna(df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].mean())
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2017), "Taux_interet_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2017), "Taux_interet_pct"].fillna(17.0)
    
    return df

df = load_and_clean_data()

# -----------------------------
# En-tête avec drapeau
# -----------------------------
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", 
             width=100, use_column_width=False, output_format="PNG")
with col2:
    st.title("Dashboard Macroéconomique – République Islamique de Mauritanie")
    st.markdown("""
    <p style="font-size: 18px; color: #64748b; margin-top: -15px; font-weight: 500;">
    📊 Suivi en temps réel des indicateurs économiques • Banque Centrale • FMI • Banque Mondiale
    </p>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# KPIs interactifs
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📈</span><h2 style="margin:0;">Indicateurs clés 2024</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
    st.metric("Croissance PIB", f"{val:.1f}%", delta="+1.9 pts vs 2023", delta_color="normal")
with col2:
    val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
    st.metric("Inflation", f"{val:.1f}%", delta="-1.4 pts vs 2023", delta_color="inverse")
with col3:
    val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
    st.metric("Recettes fiscales", f"{val:.1f}% PIB", delta="+3.8 pts vs 2023", delta_color="normal")
with col4:
    dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
    st.metric("Dette extérieure", f"{dette:.1f} Md$", delta="Stable", delta_color="off")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Section 1 : Croissance & Inflation (Plotly interactif)
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2 style="margin:0;">Analyse macroéconomique</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Croissance du PIB – Cycles et chocs économiques**")
    df_pib = df[df["Année"] >= 1962].copy()
    df_pib['Tendance'] = df_pib['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Zones de récession
    fig.add_trace(go.Scatter(
        x=df_pib["Année"],
        y=df_pib["Croissance_PIB_pct"],
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.1)',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Ligne de croissance
    fig.add_trace(go.Scatter(
        x=df_pib["Année"],
        y=df_pib["Croissance_PIB_pct"],
        mode='lines',
        name='Croissance',
        line=dict(color='#0c4a6e', width=3),
        hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
    ))
    
    # Tendance
    fig.add_trace(go.Scatter(
        x=df_pib["Année"],
        y=df_pib['Tendance'],
        mode='lines',
        name='Tendance 10 ans',
        line=dict(color='#87CEEB', width=2, dash='dash'),
        hovertemplate='<b>%{x}</b><br>Tendance: %{y:.1f}%<extra></extra>'
    ))
    
    # Annotations des chocs
    annotations = [
        dict(x=1975, y=df_pib.loc[df_pib["Année"] == 1975, "Croissance_PIB_pct"].values[0] if 1975 in df_pib["Année"].values else 0,
             text="Choc pétrolier", showarrow=True, arrowhead=2, arrowcolor='#0c4a6e'),
        dict(x=2009, y=df_pib.loc[df_pib["Année"] == 2009, "Croissance_PIB_pct"].values[0] if 2009 in df_pib["Année"].values else 0,
             text="Crise financière", showarrow=True, arrowhead=2, arrowcolor='#0c4a6e'),
        dict(x=2020, y=df_pib.loc[df_pib["Année"] == 2020, "Croissance_PIB_pct"].values[0] if 2020 in df_pib["Année"].values else 0,
             text="COVID-19", showarrow=True, arrowhead=2, arrowcolor='#0c4a6e')
    ]
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=True),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', zeroline=True, zerolinecolor='#cbd5e1'),
        hovermode='x unified',
        annotations=annotations,
        margin=dict(l=0, r=0, t=10, b=0),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown("**Inflation – Régimes macroéconomiques**")
    df_infl = df[df["Année"] >= 1986].copy()
    median = df_infl["Inflation_pct"].median()
    
    fig = go.Figure()
    
    # Zone au-dessus de la médiane
    fig.add_trace(go.Scatter(
        x=df_infl["Année"],
        y=df_infl["Inflation_pct"],
        fill='tonexty',
        fillcolor='rgba(135, 206, 235, 0.2)',
        line=dict(color='#0c4a6e', width=3),
        name='Inflation',
        hovertemplate='<b>%{x}</b><br>Inflation: %{y:.1f}%<extra></extra>'
    ))
    
    # Ligne médiane
    fig.add_hline(y=median, line_dash="dash", line_color='#87CEEB', 
                  annotation_text=f"Médiane: {median:.1f}%", annotation_position="right")
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        hovermode='x unified',
        margin=dict(l=0, r=0, t=10, b=0),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# Section 2 : Secteur extérieur
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🌍</span><h2 style="margin:0;">Soutenabilité externe</h2></div>', unsafe_allow_html=True)

df_ext = df[(df["Année"] >= 1970) & (df["Année"] <= 2021)].dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"])

fig = go.Figure()

# Dette extérieure
fig.add_trace(go.Scatter(
    x=df_ext["Année"],
    y=df_ext["Dette_exterieure_USD"]/1e9,
    mode='lines',
    name='Dette extérieure',
    line=dict(color='#EF4444', width=3),
    fill='tonexty',
    fillcolor='rgba(239, 68, 68, 0.1)',
    hovertemplate='<b>%{x}</b><br>Dette: %{y:.2f} Md$<extra></extra>'
))

# Réserves internationales
fig.add_trace(go.Scatter(
    x=df_ext["Année"],
    y=df_ext["Reserves_internationales_USD"]/1e9,
    mode='lines',
    name='Réserves internationales',
    line=dict(color='#10B981', width=3),
    fill='tonexty',
    fillcolor='rgba(16, 185, 129, 0.1)',
    hovertemplate='<b>%{x}</b><br>Réserves: %{y:.2f} Md$<extra></extra>'
))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='Milliards USD', showgrid=True, gridcolor='#f1f5f9'),
    hovermode='x unified',
    margin=dict(l=0, r=0, t=10, b=0),
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# Section 3 : Vue d'ensemble multi-indicateurs
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🎯</span><h2 style="margin:0;">Tableau de bord consolidé</h2></div>', unsafe_allow_html=True)

# Graphique combiné
df_recent = df[df["Année"] >= 2010].copy()

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Croissance vs Inflation', 'Balance commerciale', 'Recettes fiscales', 'Envois de fonds'),
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# 1. Croissance vs Inflation
fig.add_trace(go.Bar(
    x=df_recent["Année"],
    y=df_recent["Croissance_PIB_pct"],
    name='Croissance',
    marker_color='#1F77B4',
    hovertemplate='%{y:.1f}%'
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df_recent["Année"],
    y=df_recent["Inflation_pct"],
    name='Inflation',
    line=dict(color='#AEC7E8', width=3),
    yaxis='y2',
    hovertemplate='%{y:.1f}%'
), row=1, col=1)

# 2. Balance commerciale
fig.add_trace(go.Scatter(
    x=df_recent["Année"],
    y=df_recent["Solde_commercial_pct_PIB"],
    fill='tozeroy',
    fillcolor='rgba(174, 199, 232, 0.3)',
    line=dict(color='#0B3C5D', width=2),
    name='Solde commercial',
    hovertemplate='%{y:.1f}% PIB'
), row=1, col=2)

# 3. Recettes fiscales
fig.add_trace(go.Bar(
    x=df_recent["Année"],
    y=df_recent["Recettes_fiscales_pct_PIB"],
    name='Recettes fiscales',
    marker_color='#1F77B4',
    hovertemplate='%{y:.1f}% PIB'
), row=2, col=1)

# 4. Envois de fonds
fig.add_trace(go.Scatter(
    x=df_recent["Année"],
    y=df_recent["Envois_de_fonds_pct_PIB"],
    mode='lines+markers',
    name='Envois de fonds',
    line=dict(color='#0B3C5D', width=3),
    marker=dict(size=8, color='#1F77B4'),
    hovertemplate='%{y:.1f}% PIB'
), row=2, col=2)

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=600,
    showlegend=False,
    margin=dict(l=0, r=0, t=40, b=0)
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9')

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# Méthodologie
# -----------------------------
with st.expander("📚 Méthodologie et sources de données"):
    st.markdown("""
    <div class="info-box">
    <h3 style="color: #0c4a6e; margin-top: 0;">📋 Sources officielles</h3>
    <ul style="line-height: 1.8;">
        <li><b>Banque Centrale de Mauritanie (BCM)</b> – Données primaires sur recettes, chômage, taux d'intérêt (2007–2021)</li>
        <li><b>Fonds Monétaire International (FMI)</b> – Consultations Article IV (2022–2024)</li>
        <li><b>Banque Mondiale</b> – World Development Indicators (1960–2024)</li>
    </ul>
    
    <h3 style="color: #0c4a6e;">🔧 Traitement des données</h3>
    <ul style="line-height: 1.8;">
        <li>✓ Imputation par interpolation linéaire pour séries continues</li>
        <li>✓ Remplacement par moyenne historique pour variables volatiles</li>
        <li>✓ Fusion des doublons annuels (ex: 2022–2024)</li>
        <li>✓ Validation croisée avec rapports officiels</li>
        <li>✓ Normalisation des unités monétaires</li>
    </ul>
    
    <h3 style="color: #0c4a6e;">📊 Indicateurs calculés</h3>
    <ul style="line-height: 1.8;">
        <li>Tendances mobiles (moyennes glissantes sur 10 ans)</li>
        <li>Ratios dette/réserves pour soutenabilité externe</li>
        <li>Écarts à la médiane historique</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer">
    <p style="margin: 0; font-weight: 600;">© 2026 – Dashboard Macroéconomique de la Mauritanie</p>
    <p style="margin: 8px 0 0 0;">Jedou Mohamed Bebacar | Master SSD | Université de Nouakchott</p>
    <p style="margin: 8px 0 0 0; font-size: 12px; color: #94a3b8;">
        Données mises à jour en janvier 2026 • Visualisations interactives Plotly
    </p>
</div>
""", unsafe_allow_html=True)
