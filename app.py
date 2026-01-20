# app.py - Dashboard Macroéconomique Mauritanie - Toutes visualisations avec animations Plotly
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ===============================================
# CONFIGURATION PAGE
# ===============================================
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS (à compléter avec ton CSS complet ultra-moderne)
st.markdown("""
<style>
    /* Ton CSS complet ici – je mets juste un squelette pour que ça tourne */
    .main { background: linear-gradient(-45deg, #f8fafc, #e0f2fe, #dbeafe, #f1f5f9); }
    h1, h2, h3 { color: #0B3C5D; }
    /* ... ton CSS complet ... */
</style>
""", unsafe_allow_html=True)

# ===============================================
# CHARGEMENT ET NETTOYAGE (ton code exact)
# ===============================================
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
    except:
        st.error("Erreur lors du chargement du fichier CSV")
        return pd.DataFrame()

df = load_and_clean_data()
if df.empty:
    st.stop()

# Couleurs harmonisées avec tes graphiques
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"
BLEU_TRES_CLAIR = "#E6F0FA"
GRIS = "gray"

# ===============================================
# SIDEBAR
# ===============================================
with st.sidebar:
    st.title("Dashboard Mauritanie")
    page = st.radio("Navigation", [
        "Vue d'ensemble",
        "Croissance & Inflation",
        "Secteur Externe",
        "Finances Publiques",
        "Analyses Avancées"
    ])
    
    year_range = st.slider("Période", int(df["Année"].min()), int(df["Année"].max()), (2000, 2024))

df_filtered = df[(df["Année"] >= year_range[0]) & (df["Année"] <= year_range[1])].copy()

# ===============================================
# Helper : animation progressive ligne
# ===============================================
def add_animated_line(fig, x, y, name, color, width=2.5, dash=None):
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=name, line=dict(color=color, width=width, dash=dash or 'solid')))
    frames = []
    for k in range(1, len(x)+1):
        frames.append(go.Frame(
            data=[go.Scatter(x=x[:k], y=y[:k])],
            name=str(x[k-1])
        ))
    fig.update(frames=frames)
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            buttons=[
                dict(label="Play", method="animate", args=[None, {"frame": {"duration": 600, "redraw": False}, "fromcurrent": True}]),
                dict(label="Pause", method="animate", args=[[None], {"mode": "immediate"}])
            ]
        )],
        sliders=[{"steps": [{"method": "animate", "args": [[f.name]], "label": f.name} for f in frames]}]
    )

# ===============================================
# PAGE : VUE D'ENSEMBLE
# ===============================================
if page == "Vue d'ensemble":

    st.title("Croissance du PIB - cycles économiques et chocs")
    df_p = df_filtered.dropna(subset=['Croissance_PIB_pct'])
    fig_pib = go.Figure()
    add_animated_line(fig_pib, df_p["Année"], df_p["Croissance_PIB_pct"], "Croissance", BLEU_FONCE)
    add_animated_line(fig_pib, df_p["Année"], df_p["Croissance_PIB_pct"].rolling(10).mean(), "Tendance long terme", BLEU_MOYEN, dash='dash')
    fig_pib.add_hline(y=0, line_dash="dash", line_color=GRIS)
    
    for year, label in [(1975, "Choc pétrolier"), (2009, "Crise financière"), (2020, "COVID-19")]:
        if year in df_p["Année"].values:
            val = df_p[df_p["Année"] == year]["Croissance_PIB_pct"].values[0]
            fig_pib.add_annotation(x=year, y=val, text=label, showarrow=True, arrowhead=2, ax=0, ay=-50)
    
    fig_pib.update_layout(
        title="Croissance du PIB - cycles économiques et chocs<br><sub>Source : BCM, FMI, Banque Mondiale</sub>",
        yaxis_title="%", height=550, hovermode="x unified"
    )
    st.plotly_chart(fig_pib, use_container_width=True)

    # Inflation régimes
    st.title("Inflation - régimes macroéconomiques")
    df_i = df_filtered.dropna(subset=['Inflation_pct'])
    median_i = df_i["Inflation_pct"].median()
    fig_inf = go.Figure()
    add_animated_line(fig_inf, df_i["Année"], df_i["Inflation_pct"], "Inflation", BLEU_FONCE)
    fig_inf.add_hline(y=median_i, line_dash="dash", line_color=BLEU_MOYEN, annotation_text=f"Inflation médiane ({median_i:.1f}%)", annotation_position="right")
    fig_inf.add_trace(go.Scatter(
        x=df_i["Année"], y=np.maximum(df_i["Inflation_pct"], median_i),
        fill='tonexty', fillcolor=BLEU_CLAIR+"50", line_width=0, name="Régime inflation élevée"
    ))
    fig_inf.update_layout(title="Inflation - régimes macroéconomiques<br><sub>Source : BCM, FMI</sub>", yaxis_title="%", height=550)
    st.plotly_chart(fig_inf, use_container_width=True)

# ===============================================
# PAGE : Croissance & Inflation
# ===============================================
elif page == "Croissance & Inflation":

    # Volatilité
    st.title("Croissance du PIB - volatilité et incertitude")
    df_v = df_filtered.dropna(subset=['Croissance_PIB_pct'])
    rm = df_v['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()
    rs = df_v['Croissance_PIB_pct'].rolling(10, min_periods=1).std()
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=df_v["Année"], y=rm, name="Moyenne mobile (10 ans)", line=dict(color=BLEU_FONCE, width=2.5)))
    fig_vol.add_trace(go.Scatter(x=df_v["Année"], y=rm + rs, line_width=0, showlegend=False))
    fig_vol.add_trace(go.Scatter(x=df_v["Année"], y=rm - rs, fill='tonexty', fillcolor=BLEU_CLAIR+"40", name="± 1 écart-type"))
    fig_vol.update_layout(title="Croissance du PIB - volatilité et incertitude<br><sub>Source : Banque Mondiale</sub>", yaxis_title="%", height=550)
    st.plotly_chart(fig_vol, use_container_width=True)

    # Courbe Phillips
    st.title("Courbe de Phillips - Mauritanie (2007–2021)")
    df_ph = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
    fig_ph = go.Figure()
    fig_ph.add_trace(go.Scatter(
        x=df_ph["Taux_chomage_pct"], y=df_ph["Inflation_pct"],
        mode='markers', marker=dict(size=10, color=df_ph["Année"], colorscale='Blues', showscale=True),
        text=df_ph["Année"], hovertemplate="Année: %{text}<br>Chômage: %{x:.2f}%<br>Inflation: %{y:.2f}%"
    ))
    fig_ph.update_layout(
        title="Courbe de Phillips - Mauritanie (2007–2021)<br><sub>Source : BCM</sub>",
        xaxis_title="Chômage (%)", yaxis_title="Inflation (%)", height=600
    )
    st.plotly_chart(fig_ph, use_container_width=True)

# ===============================================
# PAGE : Secteur Externe
# ===============================================
elif page == "Secteur Externe":

    st.title("Soutenabilité externe : dette vs réserves")
    df_ext = df_filtered.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"])
    fig_ext = go.Figure()
    add_animated_line(fig_ext, df_ext["Année"], df_ext["Dette_exterieure_USD"]/1e9, "Dette extérieure", "darkred")
    add_animated_line(fig_ext, df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, "Réserves", BLEU_MOYEN)
    fig_ext.add_trace(go.Scatter(
        x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9,
        fill='tonexty', fillcolor="rgba(200,50,50,0.2)", line_width=0,
        name="Zone de vulnérabilité externe"
    ))
    fig_ext.update_layout(title="Soutenabilité externe : dette vs réserves<br><sub>Source : Banque Mondiale</sub>", yaxis_title="Milliards USD", height=550)
    st.plotly_chart(fig_ext, use_container_width=True)

# ===============================================
# PAGE : Analyses Avancées
# ===============================================
elif page == "Analyses Avancées":

    # Régimes macro scatter
    st.title("Régimes macroéconomiques (Inflation vs Croissance)")
    df_reg = df_filtered.dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Scatter(
        x=df_reg["Inflation_pct"], y=df_reg["Croissance_PIB_pct"],
        mode='markers', marker=dict(size=10, color=df_reg["Année"], colorscale='Blues', showscale=True),
        text=df_reg["Année"], hovertemplate="Année: %{text}<br>Inflation: %{x:.1f}%<br>Croissance: %{y:.1f}%"
    ))
    fig_reg.add_vline(x=df_reg["Inflation_pct"].median(), line_dash="dash", line_color=GRIS)
    fig_reg.add_hline(y=0, line_dash="dash", line_color=GRIS)
    fig_reg.update_layout(title="Régimes macroéconomiques (Inflation vs Croissance)<br><sub>Source : Calculs propres</sub>", height=600)
    st.plotly_chart(fig_reg, use_container_width=True)

    # Trajectoire 3D
    st.title("Trajectoire macroéconomique 3D (depuis 2000)")
    df_3d = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
    fig_3d = go.Figure()
    fig_3d.add_trace(go.Scatter3d(
        x=df_3d["Inflation_pct"], y=df_3d["Taux_chomage_pct"], z=df_3d["Croissance_PIB_pct"],
        mode='markers+lines', marker=dict(size=6, color=df_3d["Année"], colorscale='Blues', showscale=True),
        line=dict(color=BLEU_FONCE, width=3)
    ))
    fig_3d.update_layout(
        title="Trajectoire macroéconomique 3D (depuis 2000)<br><sub>Source : Calculs propres</sub>",
        scene=dict(xaxis_title="Inflation (%)", yaxis_title="Chômage (%)", zaxis_title="Croissance (%)"),
        height=700
    )
    st.plotly_chart(fig_3d, use_container_width=True)

# ===============================================
# FOOTER
# ===============================================
st.markdown("""
<div style='text-align:center; padding:40px; margin-top:80px; background:#0B3C5D; color:white; border-radius:20px;'>
<h2>Dashboard Macroéconomique Mauritanie</h2>
<p>© 2026 - Jedou Mohamed Bebacar</p>
</div>
""", unsafe_allow_html=True)
