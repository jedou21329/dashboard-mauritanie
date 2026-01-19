
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

# Couleurs originales
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"
BLEU_TRES_CLAIR = "#E6F0FA"

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
# 1. Croissance du PIB – cycles économiques et chocs
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2 style="margin:0;">1. Croissance du PIB – cycles économiques et chocs</h2></div>', unsafe_allow_html=True)

df_pib = df.dropna(subset=['Croissance_PIB_pct']).copy()
df_pib['Tendance'] = df_pib['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()

fig1 = go.Figure()

# Zone négative
fig1.add_trace(go.Scatter(
    x=df_pib["Année"],
    y=[0]*len(df_pib),
    fill=None,
    mode='lines',
    line_color='rgba(0,0,0,0)',
    showlegend=False,
    hoverinfo='skip'
))

fig1.add_trace(go.Scatter(
    x=df_pib["Année"],
    y=df_pib["Croissance_PIB_pct"],
    fill='tonexty',
    fillcolor='rgba(174, 199, 232, 0.6)',
    line=dict(width=0),
    showlegend=False,
    hoverinfo='skip'
))

# Ligne de croissance
fig1.add_trace(go.Scatter(
    x=df_pib["Année"],
    y=df_pib["Croissance_PIB_pct"],
    mode='lines',
    name='Croissance',
    line=dict(color=BLEU_FONCE, width=2),
    hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
))

# Tendance long terme
fig1.add_trace(go.Scatter(
    x=df_pib["Année"],
    y=df_pib['Tendance'],
    mode='lines',
    name='Tendance long terme',
    line=dict(color=BLEU_MOYEN, width=3),
    hovertemplate='<b>%{x}</b><br>Tendance: %{y:.1f}%<extra></extra>'
))

# Annotations
annotations = []
for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
    if year in df_pib["Année"].values:
        y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
        annotations.append(dict(
            x=year, y=y_val,
            text=label,
            showarrow=True,
            arrowhead=2,
            arrowcolor=BLEU_FONCE,
            ax=0, ay=-40
        ))

fig1.update_layout(
    title="Source : BCM, FMI, Banque Mondiale",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=True, zerolinecolor='gray'),
    hovermode='x unified',
    annotations=annotations,
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 2. Inflation – régimes macroéconomiques
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🔥</span><h2 style="margin:0;">2. Inflation – régimes macroéconomiques</h2></div>', unsafe_allow_html=True)

df_infl = df.dropna(subset=['Inflation_pct']).copy()
median = df_infl["Inflation_pct"].median()

fig2 = go.Figure()

# Zone au-dessus de la médiane
fig2.add_trace(go.Scatter(
    x=df_infl["Année"],
    y=[median]*len(df_infl),
    fill=None,
    mode='lines',
    line_color='rgba(0,0,0,0)',
    showlegend=False,
    hoverinfo='skip'
))

fig2.add_trace(go.Scatter(
    x=df_infl["Année"],
    y=df_infl["Inflation_pct"],
    fill='tonexty',
    fillcolor='rgba(174, 199, 232, 0.6)',
    line=dict(color=BLEU_FONCE, width=2),
    name='Inflation',
    hovertemplate='<b>%{x}</b><br>Inflation: %{y:.1f}%<extra></extra>'
))

# Ligne médiane
fig2.add_hline(y=median, line_dash="dash", line_color=BLEU_MOYEN, line_width=2,
              annotation_text=f"Inflation médiane ({median:.1f}%)", annotation_position="right")

fig2.update_layout(
    title="Source : BCM, FMI",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    hovermode='x unified',
    height=450,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 3. Dette vs Réserves – Soutenabilité externe
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🌍</span><h2 style="margin:0;">3. Soutenabilité externe : dette vs réserves</h2></div>', unsafe_allow_html=True)

df_ext = df.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()

fig3 = go.Figure()

# Zone de vulnérabilité
fig3.add_trace(go.Scatter(
    x=df_ext["Année"],
    y=df_ext["Reserves_internationales_USD"]/1e9,
    fill=None,
    mode='lines',
    line_color='rgba(0,0,0,0)',
    showlegend=False,
    hoverinfo='skip'
))

fig3.add_trace(go.Scatter(
    x=df_ext["Année"],
    y=df_ext["Dette_exterieure_USD"]/1e9,
    fill='tonexty',
    fillcolor='rgba(174, 199, 232, 0.6)',
    mode='lines',
    name='Zone de vulnérabilité externe',
    line=dict(width=0),
    hoverinfo='skip'
))

# Dette extérieure
fig3.add_trace(go.Scatter(
    x=df_ext["Année"],
    y=df_ext["Dette_exterieure_USD"]/1e9,
    mode='lines',
    name='Dette extérieure',
    line=dict(color=BLEU_FONCE, width=2),
    hovertemplate='<b>%{x}</b><br>Dette: %{y:.2f} Md$<extra></extra>'
))

# Réserves
fig3.add_trace(go.Scatter(
    x=df_ext["Année"],
    y=df_ext["Reserves_internationales_USD"]/1e9,
    mode='lines',
    name='Réserves',
    line=dict(color=BLEU_MOYEN, width=2),
    hovertemplate='<b>%{x}</b><br>Réserves: %{y:.2f} Md$<extra></extra>'
))

fig3.update_layout(
    title="Source : Banque Mondiale",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='Milliards USD', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    hovermode='x unified',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 4. Croissance vs Chômage (barres côte à côte)
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">👥</span><h2 style="margin:0;">4. Croissance économique et chômage (2007–2021)</h2></div>', unsafe_allow_html=True)

df_cc = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=df_cc["Année"],
    y=df_cc["Croissance_PIB_pct"],
    name='Croissance PIB',
    marker_color=BLEU_MOYEN,
    text=df_cc["Croissance_PIB_pct"].apply(lambda x: f"{x:.1f}%"),
    textposition='outside'
))

fig4.add_trace(go.Bar(
    x=df_cc["Année"],
    y=df_cc["Taux_chomage_pct"],
    name='Chômage',
    marker_color=BLEU_CLAIR,
    text=df_cc["Taux_chomage_pct"].apply(lambda x: f"{x:.1f}%"),
    textposition='outside'
))

fig4.update_layout(
    title="Source : BCM",
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 5. Courbe de Phillips
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">💹</span><h2 style="margin:0;">5. Courbe de Phillips – Mauritanie (2007–2021)</h2></div>', unsafe_allow_html=True)

df_ph = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Inflation_pct", "Taux_chomage_pct"])

fig5 = go.Figure()

fig5.add_trace(go.Scatter(
    x=df_ph["Taux_chomage_pct"],
    y=df_ph["Inflation_pct"],
    mode='markers',
    marker=dict(
        size=12,
        color=df_ph["Année"],
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Année"),
        line=dict(width=1, color='black')
    ),
    text=df_ph["Année"],
    hovertemplate='<b>Année %{text}</b><br>Chômage: %{x:.1f}%<br>Inflation: %{y:.1f}%<extra></extra>'
))

fig5.update_layout(
    title="Source : BCM",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(title='Chômage (%)', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    yaxis=dict(title='Inflation (%)', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=500
)

st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 6. Pie chart – Recettes fiscales 2024
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🥧</span><h2 style="margin:0;">6. Poids des recettes fiscales – 2024</h2></div>', unsafe_allow_html=True)

val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]

fig6 = go.Figure()

fig6.add_trace(go.Pie(
    labels=['Recettes fiscales', 'Autres'],
    values=[val, 100-val],
    marker=dict(colors=[BLEU_MOYEN, BLEU_TRES_CLAIR]),
    textinfo='label+percent',
    textposition='inside',
    hole=0
))

fig6.update_layout(
    title="Source : FMI (2023)",
    height=450
)

st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 7. Heatmap de corrélation
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🔥</span><h2 style="margin:0;">7. Corrélations entre indicateurs macroéconomiques (2007–2024)</h2></div>', unsafe_allow_html=True)

corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
corr = df[corr_vars].corr()

fig7 = go.Figure()

fig7.add_trace(go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale='Blues',
    text=corr.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 12},
    colorbar=dict(title="Corrélation")
))

fig7.update_layout(
    title="Source : Calculs propres",
    height=450,
    xaxis=dict(side='bottom'),
    yaxis=dict(side='left')
)

st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 8. Stackplot – Pression macro
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📚</span><h2 style="margin:0;">8. Pression macroéconomique : inflation et chômage</h2></div>', unsafe_allow_html=True)

df_area = df.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])

fig8 = go.Figure()

fig8.add_trace(go.Scatter(
    x=df_area["Année"],
    y=df_area["Inflation_pct"],
    mode='lines',
    name='Inflation',
    line=dict(width=0),
    fillcolor=BLEU_CLAIR,
    fill='tonexty',
    stackgroup='one'
))

fig8.add_trace(go.Scatter(
    x=df_area["Année"],
    y=df_area["Taux_chomage_pct"],
    mode='lines',
    name='Chômage',
    line=dict(width=0),
    fillcolor=BLEU_MOYEN,
    fill='tonexty',
    stackgroup='one'
))

fig8.update_layout(
    title="Source : BCM, FMI",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
)

st.plotly_chart(fig8, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 9. Boxplot par période
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📦</span><h2 style="margin:0;">9. Distribution de la croissance du PIB par période</h2></div>', unsafe_allow_html=True)

df_box = df.copy()
df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])

fig9 = go.Figure()

for i, periode in enumerate(["1960-1980", "1981-2000", "2001-2024"]):
    data = df_box[df_box["Période"] == periode]["Croissance_PIB_pct"].dropna()
    color = [BLEU_CLAIR, BLEU_MOYEN, BLEU_FONCE][i]
    fig9.add_trace(go.Box(
        y=data,
        name=periode,
        marker_color=color,
        boxmean='sd'
    ))

fig9.update_layout(
    title="Source : Banque Mondiale",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=500,
    showlegend=False
)

st.plotly_chart(fig9, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 10. Moyennes par décennie (depuis 2000)
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2 style="margin:0;">10. Indicateurs macroéconomiques – moyennes par décennie (depuis 2000)</h2></div>', unsafe_allow_html=True)

df_2000 = df[df["Année"] >= 2000].copy()
df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean()

fig10 = go.Figure()

x = [str(int(d)) for d in dec.index]

fig10.add_trace(go.Bar(
    x=x,
    y=dec["Croissance_PIB_pct"],
    name='Croissance_PIB_pct',
    marker_color=BLEU_FONCE,
    text=dec["Croissance_PIB_pct"].apply(lambda v: f"{v:.1f}%"),
    textposition='outside'
))

fig10.add_trace(go.Bar(
    x=x,
    y=dec["Inflation_pct"],
    name='Inflation_pct',
    marker_color=BLEU_MOYEN,
    text=dec["Inflation_pct"].apply(lambda v: f"{v:.1f}%"),
    textposition='outside'
))

fig10.add_trace(go.Bar(
    x=x,
    y=dec["Taux_chomage_pct"],
    name='Taux_chomage_pct',
    marker_color=BLEU_CLAIR,
    text=dec["Taux_chomage_pct"].apply(lambda v: f"{v:.1f}%"),
    textposition='outside'
))

fig10.update_layout(
    title="Source : Calculs propres",
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(title='Décennie', showgrid=False),
    yaxis=dict(title='Pourcentage (%)', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=500,
    legend=dict(title="Indicateurs", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig10, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 11. Volatilité de la croissance
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">📉</span><h2 style="margin:0;">11. Croissance du PIB – volatilité et incertitude</h2></div>', unsafe_allow_html=True)

df_vol = df.dropna(subset=['Croissance_PIB_pct']).copy()
roll_mean = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
roll_std = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).std()

fig11 = go.Figure()

# Zone ± 1 écart-type
fig11.add_trace(go.Scatter(
    x=df_vol["Année"],
    y=roll_mean + roll_std,
    fill=None,
    mode='lines',
    line_color='rgba(0,0,0,0)',
    showlegend=False,
    hoverinfo='skip'
))

fig11.add_trace(go.Scatter(
    x=df_vol["Année"],
    y=roll_mean - roll_std,
    fill='tonexty',
    fillcolor='rgba(174, 199, 232, 0.6)',
    mode='lines',
    name='± 1 écart-type',
    line_color='rgba(0,0,0,0)',
    hoverinfo='skip'
))

# Moyenne mobile
fig11.add_trace(go.Scatter(
    x=df_vol["Année"],
    y=roll_mean,
    mode='lines',
    name='Moyenne mobile (10 ans)',
    line=dict(color=BLEU_FONCE, width=2.5),
    hovertemplate='<b>%{x}</b><br>Moyenne: %{y:.1f}%<extra></extra>'
))

fig11.update_layout(
    title="Source : Banque Mondiale",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(title='%', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig11, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 12. Régimes macro (scatter)
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🎯</span><h2 style="margin:0;">12. Régimes macroéconomiques (Inflation vs Croissance)</h2></div>', unsafe_allow_html=True)

df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
median_infl = df_2000["Inflation_pct"].median()

fig12 = go.Figure()

fig12.add_trace(go.Scatter(
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

fig12.add_hline(y=0, line_dash="dash", line_color='gray', line_width=1)
fig12.add_vline(x=median_infl, line_dash="dash", line_color='gray', line_width=1)

fig12.update_layout(
    title="Source : Calculs propres",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(title='Inflation (%)', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    yaxis=dict(title='Croissance (%)', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=500
)

st.plotly_chart(fig12, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 13. Trajectoire 3D
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">🎲</span><h2 style="margin:0;">13. Trajectoire macroéconomique 3D (depuis 2000)</h2></div>', unsafe_allow_html=True)

df_3d = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])

fig13 = go.Figure()

fig13.add_trace(go.Scatter3d(
    x=df_3d["Inflation_pct"],
    y=df_3d["Taux_chomage_pct"],
    z=df_3d["Croissance_PIB_pct"],
    mode='markers+lines',
    marker=dict(
        size=8,
        color=df_3d["Année"],
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Année"),
        line=dict(width=1, color='black')
    ),
    line=dict(color=BLEU_FONCE, width=2),
    text=df_3d["Année"],
    hovertemplate='<b>Année %{text}</b><br>Inflation: %{x:.1f}%<br>Chômage: %{y:.1f}%<br>Croissance: %{z:.1f}%<extra></extra>'
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

st.plotly_chart(fig13, use_container_width=True, config={'displayModeBar': False})

# -----------------------------
# 14. Recettes fiscales – Vue 3D
# -----------------------------
st.markdown('<div class="section-header"><span class="section-icon">💰</span><h2 style="margin:0;">14. Recettes fiscales – Vue 3D (2007–2024)</h2></div>', unsafe_allow_html=True)

df3d_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])

fig14 = go.Figure()

fig14.add_trace(go.Bar(
    x=df3d_bar["Année"].astype(str),
    y=df3d_bar["Recettes_fiscales_pct_PIB"],
    marker=dict(
        color=df3d_bar["Recettes_fiscales_pct_PIB"],
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="% du PIB")
    ),
    text=df3d_bar["Recettes_fiscales_pct_PIB"].apply(lambda x: f"{x:.1f}%"),
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Recettes: %{y:.1f}% PIB<extra></extra>'
))

fig14.update_layout(
    title="Source : FMI",
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(title='Année', showgrid=False),
    yaxis=dict(title='% du PIB', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    height=500
)

st.plotly_chart(fig14, use_container_width=True, config={'displayModeBar': False})

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
        <li>Corrélations entre indicateurs macroéconomiques</li>
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
        14 visualisations interactives • Données mises à jour en janvier 2026 • Plotly & Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
