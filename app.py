# app.py - Dashboard Macroéconomique Mauritanie - 14 Visualisations Interactives avec animations
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

# CSS ULTRA-MODERNE (inchangé)
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
h1 { color: white !important; font-weight: 900 !important; font-size: 3rem !important; letter-spacing: -2px; animation: slideInDown 0.8s ease-out; }
h2 { color: white !important; font-weight: 800 !important; }
h3, h4 { color: #1e293b !important; font-weight: 700 !important; }
/* ... le reste du CSS reste identique ... */
</style>
""", unsafe_allow_html=True)

# CHARGEMENT DES DONNÉES (inchangé)
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
        df["Année"] = df["Année"].astype(int)
        df = df.groupby("Année", as_index=False).first()
        df = df.sort_values("Année").reset_index(drop=True)
       
        # Imputation (inchangée)
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
BLEU_TRES_CLAIR = "#E6F0FA"
VERT = "#10B981"
ROUGE = "#EF4444"

plotly_config = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToAdd': ['pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d'],
    'scrollZoom': True
}

# SIDEBAR (inchangé)
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
    <span class='badge'>✓ Interactif + Animé</span>
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
   
    # VIS 1: Croissance du PIB avec animation progressive
    st.markdown("### 📈 Croissance du PIB – cycles économiques et chocs")
    df_pib = df_filtered.dropna(subset=['Croissance_PIB_pct']).copy()
    if len(df_pib) > 0:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"],
            mode='lines', name='Croissance',
            line=dict(color=BLEU_FONCE, width=2.5),
            hovertemplate='<b>%{x}</b><br>Croissance: %{y:.2f}%<extra></extra>'
        ))
       
        fig.add_trace(go.Scatter(
            x=df_pib["Année"], y=df_pib["Croissance_PIB_pct"].rolling(10).mean(),
            mode='lines', name='Tendance long terme',
            line=dict(color=BLEU_MOYEN, width=3),
            hovertemplate='<b>%{x}</b><br>Tendance: %{y:.2f}%<extra></extra>'
        ))

        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.3)

        # Annotations des crises
        for year, label in [(1975, "Choc pétrolier"), (2009, "Crise financière"), (2020, "COVID-19")]:
            if year in df_pib["Année"].values and year_range[0] <= year <= year_range[1]:
                y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                fig.add_annotation(x=year, y=y_val, text=label, showarrow=True, arrowhead=2,
                                  ax=0, ay=-50, font=dict(size=10, color=BLEU_FONCE))

        # Animation
        frames = [
            go.Frame(
                data=[
                    go.Scatter(x=df_pib["Année"][:k+1], y=df_pib["Croissance_PIB_pct"][:k+1]),
                    go.Scatter(x=df_pib["Année"][:k+1], y=df_pib["Croissance_PIB_pct"].rolling(10).mean()[:k+1])
                ],
                name=str(df_pib["Année"].iloc[k]),
                traces=[0,1]
            ) for k in range(len(df_pib))
        ]

        fig.update(frames=frames)
        fig.update_layout(
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="Play", method="animate", args=[None, {"frame": {"duration": 800, "redraw": False}, "fromcurrent": True, "transition": {"duration": 300}}]),
                    dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                ],
                direction="left",
                pad={"r": 10, "t": 87},
                showactive=False,
                x=0.1,
                xanchor="right",
                y=0,
                yanchor="top"
            )],
            sliders=[{"steps": [{"method": "animate", "args": [[f.name], {"frame": {"duration": 300, "redraw": False}, "mode": "immediate"}], "label": f.name} for f in frames]}],
            title="Croissance du PIB – animation progressive",
            xaxis_title="", yaxis_title="%",
            hovermode='x unified', height=450,
            plot_bgcolor='white', margin=dict(l=60, r=40, t=100, b=60)
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config)

    # ... (les autres visualisations de la page Vue d'ensemble restent sans animation pour l'instant car moins adaptées : inflation, moyennes décennie)

# =====================================
# PAGE 5: ANALYSES AVANCÉES - TRAJECTOIRE 3D ANIMÉE
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
   
    with tab2:
        st.markdown("### 🎲 Trajectoire Macroéconomique 3D – Animation par année")
        df_3d = df_filtered.dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"]).copy()
        if len(df_3d) > 5:
            df_3d = df_3d.sort_values("Année").reset_index(drop=True)
           
            fig = go.Figure()

            # Trace complète grisée (contexte)
            fig.add_trace(go.Scatter3d(
                x=df_3d["Inflation_pct"], y=df_3d["Taux_chomage_pct"], z=df_3d["Croissance_PIB_pct"],
                mode='lines', line=dict(color='lightgray', width=2),
                showlegend=False, hoverinfo='skip'
            ))

            # Trace animée
            fig.add_trace(go.Scatter3d(
                x=[df_3d["Inflation_pct"].iloc[0]],
                y=[df_3d["Taux_chomage_pct"].iloc[0]],
                z=[df_3d["Croissance_PIB_pct"].iloc[0]],
                mode='markers+lines',
                marker=dict(size=8, color="royalblue"),
                line=dict(color=BLEU_FONCE, width=4),
                name="Trajectoire"
            ))

            frames = [
                go.Frame(
                    data=[go.Scatter3d(
                        x=df_3d["Inflation_pct"].iloc[:k+1],
                        y=df_3d["Taux_chomage_pct"].iloc[:k+1],
                        z=df_3d["Croissance_PIB_pct"].iloc[:k+1],
                        mode='markers+lines'
                    )],
                    name=str(df_3d["Année"].iloc[k]),
                    traces=[1]
                ) for k in range(len(df_3d))
            ]

            fig.update(frames=frames)
            fig.update_layout(
                updatemenus=[dict(
                    type="buttons",
                    buttons=[
                        dict(label="Play", method="animate", args=[None, {"frame": {"duration": 900, "redraw": True}, "fromcurrent": True}]),
                        dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}])
                    ]
                )],
                sliders=[{"steps": [{"method": "animate", "args": [[f.name]], "label": f.name} for f in frames]}],
                title="Trajectoire macroéconomique 3D – animation année par année",
                scene=dict(
                    xaxis_title="Inflation (%)",
                    yaxis_title="Chômage (%)",
                    zaxis_title="Croissance (%)"
                ),
                height=650
            )
            st.plotly_chart(fig, use_container_width=True, config=plotly_config)
        else:
            st.info("📊 Données insuffisantes pour la visualisation 3D animée")

# ... (le reste du code pour les autres pages/visualisations reste identique à ton code original)

# FOOTER (inchangé)
st.markdown("""
<div style='text-align: center; padding: 48px; margin-top: 60px; background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%); border-radius: 32px; color: white;'>
<h2 style="color: white; margin: 0; font-size: 1.5rem;">Dashboard Macroéconomique de la Mauritanie</h2>
<p style="margin: 16px 0 8px 0; font-size: 1.1rem; color: #E6F0FA;">
<b>Jedou Mohamed Bebacar</b> | Master SSD | Université de Nouakchott
</p>
<p style="margin: 8px 0 0 0; font-size: 0.95rem; color: #AEC7E8;">
© 2026 • 14 Visualisations Interactives • Multi-sources • Actualisé janvier 2026
</p>
</div>
""", unsafe_allow_html=True)
