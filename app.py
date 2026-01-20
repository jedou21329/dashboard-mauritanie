# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from streamlit_option_menu import option_menu

# -----------------------------
# Configuration globale
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CSS + JavaScript personnalisé
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f7fa 100%);
        min-height: 100vh;
    }
    
    /* Navigation styles */
    .st-emotion-cache-1kyxreq {
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        border-radius: 20px;
        padding: 10px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(12, 74, 110, 0.15);
    }
    
    /* Page header */
    .page-header {
        background: linear-gradient(135deg, rgba(12, 74, 110, 0.9), rgba(3, 105, 161, 0.9));
        border-radius: 24px;
        padding: 40px;
        margin: 20px 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
        color: white;
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s linear infinite;
        z-index: 0;
    }
    
    .page-header-content {
        position: relative;
        z-index: 1;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(135, 206, 235, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 60px rgba(12, 74, 110, 0.2);
        border: 1px solid #87CEEB;
    }
    
    .kpi-value {
        font-size: 42px !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }
    
    .kpi-label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .kpi-delta {
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.08);
        transition: all 0.4s ease;
        border: 1px solid #e2e8f0;
        margin: 20px 0;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #87CEEB, #0c4a6e);
    }
    
    .chart-container:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 60px rgba(0,0,0,0.15);
    }
    
    /* Section headers */
    .section-title {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 25px 0;
        margin: 30px 0;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #87CEEB, #0c4a6e) 1;
        animation: slideInLeft 0.6s ease-out;
    }
    
    .section-icon {
        font-size: 36px;
        background: linear-gradient(135deg, #0c4a6e, #0369a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: bounce 3s infinite;
    }
    
    /* Info boxes */
    .info-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-left: 6px solid #87CEEB;
        animation: fadeIn 1s ease-out;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
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
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-60px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(60px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(50px, 50px) rotate(360deg); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Footer */
    .custom-footer {
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        border-radius: 20px;
        padding: 30px;
        margin-top: 50px;
        color: white;
        text-align: center;
        animation: fadeIn 1.5s ease-out;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #87CEEB, #0c4a6e);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0c4a6e, #87CEEB);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .kpi-value {
            font-size: 32px !important;
        }
        
        .chart-container {
            padding: 20px;
        }
        
        .page-header {
            padding: 30px 20px;
        }
    }
</style>

<script>
    // Animation au défilement
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Appliquer l'animation à tous les éléments avec la classe "animate-on-scroll"
    document.addEventListener('DOMContentLoaded', function() {
        const elements = document.querySelectorAll('.chart-container, .section-title, .info-card');
        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease-out';
            observer.observe(el);
        });
        
        // Animation des KPI cards
        const kpiCards = document.querySelectorAll('[data-testid="stMetricValue"]');
        kpiCards.forEach(card => {
            const value = card.innerText;
            const numValue = parseFloat(value);
            if (!isNaN(numValue)) {
                card.innerText = '0';
                let counter = 0;
                const increment = numValue / 50;
                const timer = setInterval(() => {
                    counter += increment;
                    if (counter >= numValue) {
                        card.innerText = value;
                        clearInterval(timer);
                    } else {
                        card.innerText = counter.toFixed(1);
                    }
                }, 30);
            }
        });
        
        // Effet parallaxe pour le header
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const header = document.querySelector('.page-header');
            if (header) {
                header.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        });
        
        // Effet de particules pour le header
        const header = document.querySelector('.page-header');
        if (header) {
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.style.position = 'absolute';
                particle.style.width = Math.random() * 10 + 5 + 'px';
                particle.style.height = particle.style.width;
                particle.style.background = 'rgba(255, 255, 255, 0.3)';
                particle.style.borderRadius = '50%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animation = `float ${Math.random() * 10 + 10}s linear infinite`;
                header.appendChild(particle);
            }
        }
    });
    
    // Effet de survol pour les cartes
    document.addEventListener('mouseover', function(e) {
        if (e.target.closest('.kpi-card')) {
            const card = e.target.closest('.kpi-card');
            card.style.transform = 'translateY(-10px) scale(1.02)';
        }
    });
    
    document.addEventListener('mouseout', function(e) {
        if (e.target.closest('.kpi-card')) {
            const card = e.target.closest('.kpi-card');
            card.style.transform = 'translateY(0) scale(1)';
        }
    });
</script>
""", unsafe_allow_html=True)

# -----------------------------
# Fonctions de chargement des données
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

# -----------------------------
# Fonctions de visualisation
# -----------------------------
def create_growth_chart(df):
    df_pib = df.dropna(subset=['Croissance_PIB_pct']).copy()
    df_pib['Tendance'] = df_pib['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_pib["Année"], y=[0]*len(df_pib), fill=None, mode='lines', 
                           line_color='rgba(0,0,0,0)', showlegend=False))
    fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"], fill='tonexty',
                           fillcolor='rgba(174, 199, 232, 0.6)', line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"], mode='lines',
                           name='Croissance', line=dict(color="#0c4a6e", width=2)))
    fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib['Tendance'], mode='lines',
                           name='Tendance long terme', line=dict(color="#1F77B4", width=3)))
    
    fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white')
    return fig

def create_inflation_chart(df):
    df_infl = df.dropna(subset=['Inflation_pct']).copy()
    median = df_infl["Inflation_pct"].median()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_infl["Année"], y=[median]*len(df_infl), fill=None, mode='lines',
                           line_color='rgba(0,0,0,0)', showlegend=False))
    fig.add_trace(go.Scatter(x=df_infl["Année"], y=df_infl["Inflation_pct"], fill='tonexty',
                           fillcolor='rgba(174, 199, 232, 0.6)', line=dict(color="#0c4a6e", width=2),
                           name='Inflation'))
    fig.add_hline(y=median, line_dash="dash", line_color="#1F77B4", line_width=2,
                  annotation_text=f"Inflation médiane ({median:.1f}%)", annotation_position="right")
    
    fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white')
    return fig

def create_debt_reserves_chart(df):
    df_ext = df.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Reserves_internationales_USD"]/1e9,
                           fill=None, mode='lines', line_color='rgba(0,0,0,0)', showlegend=False))
    fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9,
                           fill='tonexty', fillcolor='rgba(174, 199, 232, 0.6)', mode='lines',
                           name='Zone de vulnérabilité', line=dict(width=0)))
    fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9,
                           mode='lines', name='Dette extérieure', line=dict(color="#0c4a6e", width=2)))
    fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Reserves_internationales_USD"]/1e9,
                           mode='lines', name='Réserves', line=dict(color="#1F77B4", width=2)))
    
    fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='white')
    return fig

# -----------------------------
# Navigation
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="📊 Navigation",
        options=["🏠 Accueil", "📈 Vue Macro", "💰 Finances Publiques", "🌍 Commerce Extérieur", "📊 Analyses Avancées"],
        icons=["house", "graph-up", "currency-dollar", "globe-americas", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "#0c4a6e", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#e9ecef"},
            "nav-link-selected": {"background-color": "#0c4a6e", "color": "white"},
        }
    )

# -----------------------------
# Page 1: Accueil
# -----------------------------
if selected == "🏠 Accueil":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-content">
            <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg" 
                     style="width: 80px; height: 80px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
                <div>
                    <h1 style="margin: 0; font-size: 3rem; font-weight: 900;">🇲🇷 Dashboard Macroéconomique</h1>
                    <p style="font-size: 1.5rem; opacity: 0.9; margin: 10px 0 0 0;">
                    République Islamique de Mauritanie
                    </p>
                </div>
            </div>
            <p style="font-size: 1.2rem; margin-top: 20px; max-width: 800px;">
            Plateforme interactive de suivi des indicateurs économiques nationaux - 
            Données actualisées de 1960 à 2024
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Principaux
    st.markdown('<div class="section-title"><span class="section-icon">📈</span><h2 style="margin:0;">Indicateurs Clés 2024</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Croissance du PIB</div>
            <div class="kpi-value">5.2%</div>
            <div class="kpi-delta" style="background: #d1fae5; color: #065f46;">+1.9 pts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Inflation</div>
            <div class="kpi-value">3.8%</div>
            <div class="kpi-delta" style="background: #fee2e2; color: #991b1b;">-1.4 pts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Recettes Fiscales</div>
            <div class="kpi-value">22.5%</div>
            <div class="kpi-delta" style="background: #d1fae5; color: #065f46;">+3.8 pts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Dette Extérieure</div>
            <div class="kpi-value">4.3 Md$</div>
            <div class="kpi-delta" style="background: #e5e7eb; color: #374151;">Stable</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🌟 À propos de ce Dashboard
    
    Cette plateforme interactive offre une analyse complète de l'économie mauritanienne à travers :
    
    - **📈 14 visualisations interactives** couvrant tous les aspects macroéconomiques
    - **📊 Données historiques** de 1960 à 2024
    - **🔍 Analyses thématiques** par secteur économique
    - **📱 Interface moderne** avec animations fluides
    
    Naviguez à travers les différentes sections via le menu latéral pour explorer :
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        ### 📈 Vue Macro
        - Croissance du PIB
        - Inflation
        - Cycles économiques
        """)
    
    with col2:
        st.markdown("""
        ### 💰 Finances Publiques
        - Recettes fiscales
        - Dépenses publiques
        - Dette extérieure
        """)
    
    with col3:
        st.markdown("""
        ### 🌍 Commerce Extérieur
        - Balance commerciale
        - Réserves internationales
        - Envois de fonds
        """)
    
    with col4:
        st.markdown("""
        ### 📊 Analyses Avancées
        - Corrélations
        - Régimes macroéconomiques
        - Projections
        """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aperçu des données
    st.markdown('<div class="section-title"><span class="section-icon">📋</span><h2 style="margin:0;">Aperçu des Données</h2></div>', unsafe_allow_html=True)
    
    df = load_and_clean_data()
    with st.expander("🔍 Visualiser les données brutes (1960-2024)", expanded=False):
        st.dataframe(df.style.background_gradient(cmap='Blues'), use_container_width=True)
    
    # Statistiques descriptives
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Statistiques Descriptives")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats_df = df[numeric_cols].describe().T
    st.dataframe(stats_df.style.format("{:.2f}").background_gradient(cmap='Blues'), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Page 2: Vue Macro
# -----------------------------
elif selected == "📈 Vue Macro":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-content">
            <h1 style="margin: 0; font-size: 2.8rem; font-weight: 900;">📈 Vue Macroéconomique</h1>
            <p style="font-size: 1.2rem; margin-top: 10px; opacity: 0.9;">
            Analyse des principaux indicateurs macroéconomiques et cycles économiques
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_and_clean_data()
    
    # Section 1: Croissance du PIB
    st.markdown('<div class="section-title"><span class="section-icon">📊</span><h2 style="margin:0;">1. Croissance du PIB – Cycles économiques et chocs</h2></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig1 = create_growth_chart(df)
    fig1.update_layout(
        title="Source : BCM, FMI, Banque Mondiale",
        yaxis=dict(title='%'),
        hovermode='x unified'
    )
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Inflation
    st.markdown('<div class="section-title"><span class="section-icon">🔥</span><h2 style="margin:0;">2. Inflation – Régimes macroéconomiques</h2></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig2 = create_inflation_chart(df)
    fig2.update_layout(
        title="Source : BCM, FMI",
        yaxis=dict(title='%'),
        hovermode='x unified'
    )
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Croissance vs Chômage
    st.markdown('<div class="section-title"><span class="section-icon">👥</span><h2 style="margin:0;">3. Croissance économique et chômage (2007–2021)</h2></div>', unsafe_allow_html=True)
    
    df_cc = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=df_cc["Année"], y=df_cc["Croissance_PIB_pct"], name='Croissance PIB',
                         marker_color="#1F77B4", text=df_cc["Croissance_PIB_pct"].apply(lambda x: f"{x:.1f}%")))
    fig4.add_trace(go.Bar(x=df_cc["Année"], y=df_cc["Taux_chomage_pct"], name='Chômage',
                         marker_color="#AEC7E8", text=df_cc["Taux_chomage_pct"].apply(lambda x: f"{x:.1f}%")))
    fig4.update_layout(
        title="Source : BCM",
        barmode='group',
        yaxis=dict(title='%'),
        height=500
    )
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Volatilité de la croissance
    st.markdown('<div class="section-title"><span class="section-icon">📉</span><h2 style="margin:0;">4. Croissance du PIB – Volatilité et incertitude</h2></div>', unsafe_allow_html=True)
    
    df_vol = df.dropna(subset=['Croissance_PIB_pct']).copy()
    roll_mean = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
    roll_std = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).std()
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig11 = go.Figure()
    fig11.add_trace(go.Scatter(x=df_vol["Année"], y=roll_mean + roll_std, fill=None, mode='lines',
                              line_color='rgba(0,0,0,0)', showlegend=False))
    fig11.add_trace(go.Scatter(x=df_vol["Année"], y=roll_mean - roll_std, fill='tonexty',
                              fillcolor='rgba(174, 199, 232, 0.6)', mode='lines',
                              name='± 1 écart-type', line_color='rgba(0,0,0,0)'))
    fig11.add_trace(go.Scatter(x=df_vol["Année"], y=roll_mean, mode='lines',
                              name='Moyenne mobile (10 ans)', line=dict(color="#0c4a6e", width=2.5)))
    
    fig11.update_layout(
        title="Source : Banque Mondiale",
        yaxis=dict(title='%'),
        height=450
    )
    st.plotly_chart(fig11, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Page 3: Finances Publiques
# -----------------------------
elif selected == "💰 Finances Publiques":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-content">
            <h1 style="margin: 0; font-size: 2.8rem; font-weight: 900;">💰 Finances Publiques</h1>
            <p style="font-size: 1.2rem; margin-top: 10px; opacity: 0.9;">
            Analyse des recettes fiscales, dépenses publiques et dette extérieure
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_and_clean_data()
    
    # Section 1: Dette vs Réserves
    st.markdown('<div class="section-title"><span class="section-icon">🌍</span><h2 style="margin:0;">1. Soutenabilité externe : dette vs réserves</h2></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig3 = create_debt_reserves_chart(df)
    fig3.update_layout(
        title="Source : Banque Mondiale",
        yaxis=dict(title='Milliards USD'),
        hovermode='x unified'
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Recettes fiscales
    st.markdown('<div class="section-title"><span class="section-icon">🥧</span><h2 style="margin:0;">2. Poids des recettes fiscales – 2024</h2></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
    fig6 = go.Figure(go.Pie(
        labels=['Recettes fiscales', 'Autres'],
        values=[val, 100-val],
        marker=dict(colors=["#1F77B4", "#E6F0FA"]),
        textinfo='label+percent',
        hole=0
    ))
    fig6.update_layout(title="Source : FMI (2023)", height=450)
    st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Recettes fiscales - Vue temporelle
    st.markdown('<div class="section-title"><span class="section-icon">💰</span><h2 style="margin:0;">3. Recettes fiscales – Évolution temporelle (2007–2024)</h2></div>', unsafe_allow_html=True)
    
    df3d_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig14 = go.Figure()
    fig14.add_trace(go.Bar(
        x=df3d_bar["Année"].astype(str),
        y=df3d_bar["Recettes_fiscales_pct_PIB"],
        marker=dict(color=df3d_bar["Recettes_fiscales_pct_PIB"], colorscale='Blues'),
        text=df3d_bar["Recettes_fiscales_pct_PIB"].apply(lambda x: f"{x:.1f}%"),
        textposition='outside'
    ))
    fig14.update_layout(
        title="Source : FMI",
        yaxis=dict(title='% du PIB'),
        height=500
    )
    st.plotly_chart(fig14, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Distribution par période
    st.markdown('<div class="section-title"><span class="section-icon">📦</span><h2 style="margin:0;">4. Distribution de la croissance par période</h2></div>', unsafe_allow_html=True)
    
    df_box = df.copy()
    df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], 
                              labels=["1960-1980", "1981-2000", "2001-2024"])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig9 = go.Figure()
    colors = ["#AEC7E8", "#1F77B4", "#0c4a6e"]
    for i, periode in enumerate(["1960-1980", "1981-2000", "2001-2024"]):
        data = df_box[df_box["Période"] == periode]["Croissance_PIB_pct"].dropna()
        fig9.add_trace(go.Box(y=data, name=periode, marker_color=colors[i], boxmean='sd'))
    
    fig9.update_layout(
        title="Source : Banque Mondiale",
        yaxis=dict(title='%'),
        height=500
    )
    st.plotly_chart(fig9, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Page 4: Commerce Extérieur
# -----------------------------
elif selected == "🌍 Commerce Extérieur":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-content">
            <h1 style="margin: 0; font-size: 2.8rem; font-weight: 900;">🌍 Commerce Extérieur</h1>
            <p style="font-size: 1.2rem; margin-top: 10px; opacity: 0.9;">
            Analyse de la balance commerciale, réserves internationales et flux financiers
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_and_clean_data()
    
    # Section 1: Courbe de Phillips
    st.markdown('<div class="section-title"><span class="section-icon">💹</span><h2 style="margin:0;">1. Courbe de Phillips – Mauritanie (2007–2021)</h2></div>', unsafe_allow_html=True)
    
    df_ph = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=df_ph["Taux_chomage_pct"],
        y=df_ph["Inflation_pct"],
        mode='markers',
        marker=dict(size=12, color=df_ph["Année"], colorscale='Blues',
                   colorbar=dict(title="Année"), line=dict(width=1, color='black')),
        text=df_ph["Année"]
    ))
    fig5.update_layout(
        title="Source : BCM",
        xaxis=dict(title='Chômage (%)'),
        yaxis=dict(title='Inflation (%)'),
        height=500
    )
    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Pression macroéconomique
    st.markdown('<div class="section-title"><span class="section-icon">📚</span><h2 style="margin:0;">2. Pression macroéconomique : inflation et chômage</h2></div>', unsafe_allow_html=True)
    
    df_area = df.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(
        x=df_area["Année"], y=df_area["Inflation_pct"],
        mode='lines', name='Inflation',
        line=dict(width=0), fillcolor="#AEC7E8",
        fill='tonexty', stackgroup='one'
    ))
    fig8.add_trace(go.Scatter(
        x=df_area["Année"], y=df_area["Taux_chomage_pct"],
        mode='lines', name='Chômage',
        line=dict(width=0), fillcolor="#1F77B4",
        fill='tonexty', stackgroup='one'
    ))
    fig8.update_layout(
        title="Source : BCM, FMI",
        yaxis=dict(title='%'),
        height=450
    )
    st.plotly_chart(fig8, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Moyennes par décennie
    st.markdown('<div class="section-title"><span class="section-icon">📊</span><h2 style="margin:0;">3. Indicateurs macro – moyennes par décennie (depuis 2000)</h2></div>', unsafe_allow_html=True)
    
    df_2000 = df[df["Année"] >= 2000].copy()
    df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
    dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean()
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig10 = go.Figure()
    x = [str(int(d)) for d in dec.index]
    fig10.add_trace(go.Bar(x=x, y=dec["Croissance_PIB_pct"], name='Croissance',
                          marker_color="#0c4a6e",
                          text=dec["Croissance_PIB_pct"].apply(lambda v: f"{v:.1f}%")))
    fig10.add_trace(go.Bar(x=x, y=dec["Inflation_pct"], name='Inflation',
                          marker_color="#1F77B4",
                          text=dec["Inflation_pct"].apply(lambda v: f"{v:.1f}%")))
    fig10.add_trace(go.Bar(x=x, y=dec["Taux_chomage_pct"], name='Chômage',
                          marker_color="#AEC7E8",
                          text=dec["Taux_chomage_pct"].apply(lambda v: f"{v:.1f}%")))
    fig10.update_layout(
        title="Source : Calculs propres",
        barmode='group',
        yaxis=dict(title='Pourcentage (%)'),
        height=500
    )
    st.plotly_chart(fig10, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Page 5: Analyses Avancées
# -----------------------------
elif selected == "📊 Analyses Avancées":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-content">
            <h1 style="margin: 0; font-size: 2.8rem; font-weight: 900;">📊 Analyses Avancées</h1>
            <p style="font-size: 1.2rem; margin-top: 10px; opacity: 0.9;">
            Corrélations, régimes macroéconomiques et analyses multidimensionnelles
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_and_clean_data()
    
    # Section 1: Heatmap de corrélation
    st.markdown('<div class="section-title"><span class="section-icon">🔥</span><h2 style="margin:0;">1. Corrélations entre indicateurs macroéconomiques</h2></div>', unsafe_allow_html=True)
    
    corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
    corr = df[corr_vars].corr()
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig7 = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale='Blues', text=corr.values.round(2),
        texttemplate='%{text}', colorbar=dict(title="Corrélation")
    ))
    fig7.update_layout(title="Source : Calculs propres", height=450)
    st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: Régimes macroéconomiques
    st.markdown('<div class="section-title"><span class="section-icon">🎯</span><h2 style="margin:0;">2. Régimes macroéconomiques (Inflation vs Croissance)</h2></div>', unsafe_allow_html=True)
    
    df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
    median_infl = df_2000["Inflation_pct"].median()
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig12 = go.Figure()
    fig12.add_trace(go.Scatter(
        x=df_2000["Inflation_pct"],
        y=df_2000["Croissance_PIB_pct"],
        mode='markers',
        marker=dict(size=10, color=df_2000["Année"], colorscale='Blues',
                   colorbar=dict(title="Année"), line=dict(width=1, color='black')),
        text=df_2000["Année"]
    ))
    fig12.add_hline(y=0, line_dash="dash", line_color='gray')
    fig12.add_vline(x=median_infl, line_dash="dash", line_color='gray')
    fig12.update_layout(
        title="Source : Calculs propres",
        xaxis=dict(title='Inflation (%)'),
        yaxis=dict(title='Croissance (%)'),
        height=500
    )
    st.plotly_chart(fig12, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: Trajectoire 3D
    st.markdown('<div class="section-title"><span class="section-icon">🎲</span><h2 style="margin:0;">3. Trajectoire macroéconomique 3D (depuis 2000)</h2></div>', unsafe_allow_html=True)
    
    df_3d = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig13 = go.Figure()
    fig13.add_trace(go.Scatter3d(
        x=df_3d["Inflation_pct"],
        y=df_3d["Taux_chomage_pct"],
        z=df_3d["Croissance_PIB_pct"],
        mode='markers+lines',
        marker=dict(size=8, color=df_3d["Année"], colorscale='Blues',
                   colorbar=dict(title="Année"), line=dict(width=1, color='black')),
        line=dict(color="#0c4a6e", width=2),
        text=df_3d["Année"]
    ))
    fig13.update_layout(
        title="Source : Calculs propres",
        scene=dict(
            xaxis_title='Inflation (%)',
            yaxis_title='Chômage (%)',
            zaxis_title='Croissance (%)',
            bgcolor='white'
        ),
        height=600
    )
    st.plotly_chart(fig13, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer commun
# -----------------------------
st.markdown("""
<div class="custom-footer">
    <h3 style="margin: 0; color: white;">🇲🇷 Dashboard Macroéconomique de la Mauritanie</h3>
    <p style="margin: 15px 0; color: rgba(255, 255, 255, 0.9);">
    Plateforme interactive de suivi des indicateurs économiques • Données mises à jour en janvier 2026
    </p>
    <div style="display: flex; justify-content: center; gap: 30px; margin-top: 20px;">
        <div>
            <p style="margin: 0; font-weight: 600; color: white;">Sources</p>
            <p style="margin: 5px 0; color: rgba(255, 255, 255, 0.8); font-size: 14px;">
            Banque Centrale de Mauritanie<br>FMI • Banque Mondiale
            </p>
        </div>
        <div>
            <p style="margin: 0; font-weight: 600; color: white;">Technologies</p>
            <p style="margin: 5px 0; color: rgba(255, 255, 255, 0.8); font-size: 14px;">
            Streamlit • Plotly • Pandas<br>HTML/CSS • JavaScript
            </p>
        </div>
        <div>
            <p style="margin: 0; font-weight: 600; color: white;">Développeur</p>
            <p style="margin: 5px 0; color: rgba(255, 255, 255, 0.8); font-size: 14px;">
            Jedou Mohamed Bebacar<br>Master SSD • Université de Nouakchott
            </p>
        </div>
    </div>
    <p style="margin-top: 25px; color: rgba(255, 255, 255, 0.7); font-size: 12px;">
    14 visualisations interactives • 5 pages thématiques • Interface responsive
    </p>
</div>
""", unsafe_allow_html=True)
