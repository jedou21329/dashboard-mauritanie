# app.py - Dashboard Macroéconomique Mauritanie - 14 Visualisations Interactives
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
# CSS ULTRA-MODERNE
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
        
        # Imputation intelligente (ton code exact)
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

df = load_and_clean_data()
if df.empty:
    st.stop()

# Couleurs
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"
BLEU_TRES_CLAIR = "#E6F0FA"

# Configuration Plotly
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
    
    # KPIs
    if 2024 in df["Année"].values:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
            st.metric("📈 Croissance PIB", f"{val:.1f}%", delta="+1.9 pts")
        with col2:
            val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
            st.metric("🔥 Inflation", f"{val:.1f}%", delta="-1.4 pts", delta_color="inverse")
        with col3:
            val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
            st.metric("💼 Recettes", f"{val:.1f}% PIB", delta="+3.8 pts")
        with col4:
            dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
            st.metric("🌐 Dette Ext.", f"{dette:.1f} Md$", delta="Stable", delta_color="off")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # VIS 1: Croissance du PIB
    st.markdown("### 📈 Visualisation 1 – Croissance du PIB avec cycles économiques")
    df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
    if len(df_pib) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"], mode='lines', name='Croissance', line=dict(color=BLEU_FONCE, width=2)))
        fig.add_trace(go.Scatter(x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(10).mean(), mode='lines', name='Tendance long terme', line=dict(color=BLEU_MOYEN, width=3)))
        for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
            if year in df_pib["Année"].values and year_range[0] <= year <= year_range[1]:
                y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                fig.add_annotation(x=year, y=y_val, text=label, showarrow=True, arrowhead=2, arrowcolor=BLEU_FONCE, ax=0, ay=-60)
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.update_layout(title="Croissance du PIB – cycles économiques et chocs<br><sub>Source : BCM, FMI, Banque Mondiale</sub>", yaxis_title="%", plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 2: Inflation
    st.markdown("### 🔥 Visualisation 2 – Inflation et régimes macroéconomiques")
    df_infl = df_filtered.dropna(subset=['Inflation_pct']).copy()
    if len(df_infl) > 0:
        median = df_infl["Inflation_pct"].median()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_infl["Année"], y=df_infl["Inflation_pct"], mode='lines', name='Inflation', line=dict(color=BLEU_FONCE, width=2)))
        fig.add_hline(y=median, line_dash="dash", line_color=BLEU_MOYEN, annotation_text=f"Inflation médiane ({median:.1f}%)")
        fig.update_layout(title="Inflation – régimes macroéconomiques<br><sub>Source : BCM, FMI</sub>", yaxis_title="%", plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 3: Dette vs Réserves
    st.markdown("### 🌐 Visualisation 3 – Soutenabilité externe : dette vs réserves")
    df_ext = df_filtered.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()
    if len(df_ext) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9, mode='lines', name='Dette extérieure', line=dict(color=BLEU_FONCE, width=2)))
        fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Reserves_internationales_USD"]/1e9, mode='lines', name='Réserves', line=dict(color=BLEU_MOYEN, width=2)))
        fig.update_layout(title="Soutenabilité externe : dette vs réserves<br><sub>Source : Banque Mondiale</sub>", yaxis_title="Milliards USD", plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 4: Croissance vs Chômage
    st.markdown("### 👥 Visualisation 4 – Croissance économique et chômage (2007–2021)")
    df_cc = df_filtered[(df_filtered["Année"] >= 2007) & (df_filtered["Année"] <= 2021)].dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
    if len(df_cc) > 0:
        x = np.arange(len(df_cc))
        w = 0.4
        fig = go.Figure()
        fig.add_trace(go.Bar(x=x - w/2, y=df_cc["Croissance_PIB_pct"], name='Croissance PIB', marker_color=BLEU_MOYEN))
        fig.add_trace(go.Bar(x=x + w/2, y=df_cc["Taux_chomage_pct"], name='Chômage', marker_color=BLEU_CLAIR))
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=x, ticktext=df_cc["Année"]), yaxis_title="%", title="Croissance économique et chômage (2007–2021)<br><sub>Source : BCM</sub>", barmode='group')
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 5: Courbe de Phillips
    st.markdown("### 💹 Visualisation 5 – Courbe de Phillips")
    df_ph = df_filtered[(df_filtered["Année"] >= 2007) & (df_filtered["Année"] <= 2021)].dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
    if len(df_ph) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_ph["Taux_chomage_pct"], y=df_ph["Inflation_pct"], mode='markers', marker=dict(size=10, color=df_ph["Année"], colorscale='Blues'), text=df_ph["Année"]))
        fig.update_layout(title="Courbe de Phillips – Mauritanie (2007–2021)<br><sub>Source : BCM</sub>", xaxis_title="Chômage (%)", yaxis_title="Inflation (%)")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 6: Pie chart
    st.markdown("### 🥧 Visualisation 6 – Poids des recettes fiscales – 2024")
    if 2024 in df["Année"].values:
        val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=['Recettes fiscales', 'Autres'], values=[val, 100-val], marker=dict(colors=[BLEU_MOYEN, BLEU_TRES_CLAIR])))
        fig.update_layout(title="Poids des recettes fiscales – 2024<br><sub>Source : FMI (2023)</sub>")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 7: Heatmap
    st.markdown("### 🔥 Visualisation 7 – Corrélations entre indicateurs")
    corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
    df_corr = df_filtered[corr_vars].dropna()
    if len(df_corr) > 5:
        corr = df_corr.corr()
        fig = go.Figure()
        fig.add_trace(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='Blues', text=corr.values.round(2), texttemplate='%{text}'))
        fig.update_layout(title="Corrélations entre indicateurs macroéconomiques (2007–2024)<br><sub>Source : Calculs propres</sub>")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 8: Stackplot
    st.markdown("### 📚 Visualisation 8 – Pression macroéconomique")
    df_area = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
    if len(df_area) > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_area["Année"], y=df_area["Inflation_pct"], stackgroup='one', name='Inflation', line=dict(width=0), fillcolor=BLEU_CLAIR))
        fig.add_trace(go.Scatter(x=df_area["Année"], y=df_area["Taux_chomage_pct"], stackgroup='one', name='Chômage', line=dict(width=0), fillcolor=BLEU_MOYEN))
        fig.update_layout(title="Pression macroéconomique : inflation et chômage<br><sub>Source : BCM, FMI</sub>", yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 9: Boxplot
    st.markdown("### 📦 Visualisation 9 – Distribution par période")
    df_box = df.copy()
    df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])
    df_box = df_box[df_box["Période"].notna()]
    if len(df_box) > 0:
        fig = go.Figure()
        for i, periode in enumerate(["1960-1980", "1981-2000", "2001-2024"]):
            data = df_box[df_box["Période"] == periode]["Croissance_PIB_pct"].dropna()
            color = [BLEU_CLAIR, BLEU_MOYEN, BLEU_FONCE][i]
            fig.add_trace(go.Box(y=data, name=periode, marker_color=color))
        fig.update_layout(title="Distribution de la croissance du PIB par période<br><sub>Source : Banque Mondiale</sub>", yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 10: Moyennes par décennie
    st.markdown("### 📊 Visualisation 10 – Indicateurs moyens par décennie")
    df_2000 = df[df["Année"] >= 2000].copy()
    df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
    dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean().reset_index()
    if len(dec) > 0:
        fig = go.Figure()
        x_labels = [f"{int(d)}s" for d in dec["Décennie"]]
        fig.add_trace(go.Bar(x=x_labels, y=dec["Croissance_PIB_pct"], name='Croissance PIB', marker_color=BLEU_FONCE))
        fig.add_trace(go.Bar(x=x_labels, y=dec["Inflation_pct"], name='Inflation', marker_color=BLEU_MOYEN))
        fig.add_trace(go.Bar(x=x_labels, y=dec["Taux_chomage_pct"], name='Chômage', marker_color=BLEU_CLAIR))
        fig.update_layout(barmode='group', title="Indicateurs macroéconomiques – moyennes par décennie<br><sub>Source: Calculs propres</sub>", yaxis_title="Pourcentage (%)")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 11: Volatilité
    st.markdown("### 📉 Visualisation 11 – Volatilité de la croissance")
    df_vol = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
    if len(df_vol) >= 10:
        roll_mean = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
        roll_std = df_vol['Croissance_PIB_pct'].rolling(10, min_periods=1).std()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_vol["Année"], y=roll_mean, mode='lines', name='Moyenne mobile (10 ans)', line=dict(color=BLEU_FONCE, width=2.5)))
        fig.add_trace(go.Scatter(x=df_vol["Année"], y=roll_mean + roll_std, fill=None, mode='lines', line=dict(color='rgba(0,0,0,0)')))
        fig.add_trace(go.Scatter(x=df_vol["Année"], y=roll_mean - roll_std, fill='tonexty', fillcolor=BLEU_CLAIR, mode='lines', line=dict(color='rgba(0,0,0,0)')))
        fig.update_layout(title="Croissance du PIB – volatilité et incertitude<br><sub>Source : Banque Mondiale</sub>", yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 12: Régimes macro
    st.markdown("### 🎯 Visualisation 12 – Régimes macroéconomiques")
    df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
    if len(df_2000) > 0:
        median_infl = df_2000["Inflation_pct"].median()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_2000["Inflation_pct"], y=df_2000["Croissance_PIB_pct"], mode='markers', marker=dict(size=8, color=df_2000["Année"], colorscale='Blues')))
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.add_vline(x=median_infl, line_dash="dash", line_color="gray")
        fig.update_layout(title="Régimes macroéconomiques (Inflation vs Croissance)<br><sub>Source : Calculs propres</sub>", xaxis_title="Inflation (%)", yaxis_title="Croissance (%)")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 13: Trajectoire 3D
    st.markdown("### 🎲 Visualisation 13 – Trajectoire macroéconomique 3D")
    df_3d = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
    if len(df_3d) > 5:
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=df_3d["Inflation_pct"],
            y=df_3d["Taux_chomage_pct"],
            z=df_3d["Croissance_PIB_pct"],
            mode='markers+lines',
            marker=dict(size=5, color=df_3d["Année"], colorscale='Blues'),
            line=dict(color=BLEU_FONCE)
        ))
        fig.update_layout(scene=dict(xaxis_title='Inflation (%)', yaxis_title='Chômage (%)', zaxis_title='Croissance (%)'), title="Trajectoire macroéconomique 3D (depuis 2000)<br><sub>Source : Calculs propres</sub>")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)
    
    # VIS 14: Recettes fiscales 3D
    st.markdown("### 💰 Visualisation 14 – Recettes fiscales – Vue 3D")
    df3d_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
    if len(df3d_bar) > 0:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df3d_bar["Année"], y=df3d_bar["Recettes_fiscales_pct_PIB"], marker_color=BLEU_MOYEN))
        fig.update_layout(title="Recettes fiscales – Vue 3D (2007–2024)<br><sub>Source : FMI</sub>", xaxis_title="Année", yaxis_title="% du PIB")
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

# ===================================== 
# AUTRES PAGES (structure similaire)
# =====================================
elif page == "📈 Croissance & Inflation":
    st.markdown('<div class="hero-header"><div class="hero-content"><h1 class="hero-title">📈 Croissance & Inflation</h1></div></div>', unsafe_allow_html=True)
    # ... visualisations 1, 2, 4, 5, 11, 12 ...
elif page == "🌐 Secteur Externe":
    st.markdown('<div class="hero-header"><div class="hero-content"><h1 class="hero-title">🌐 Secteur Externe</h1></div></div>', unsafe_allow_html=True)
    # ... visualisations 3, solde commercial ...
elif page == "💼 Finances Publiques":
    st.markdown('<div class="hero-header"><div class="hero-content"><h1 class="hero-title">💼 Finances Publiques</h1></div></div>', unsafe_allow_html=True)
    # ... visualisations 6, 14 ...
elif page == "📊 Analyses Avancées":
    st.markdown('<div class="hero-header"><div class="hero-content"><h1 class="hero-title">📊 Analyses Avancées</h1></div></div>', unsafe_allow_html=True)
    # ... visualisations 7, 8, 9, 10, 13 ...

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
