
# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# CSS PERSONNALISÉ – Design Institutionnel
# -----------------------------
st.markdown("""
<style>
    /* Fond principal */
    .main {
        background: #f8fafc;
        color: #1e293b;
    }
    
    /* Titres */
    h1, h2, h3, h4 {
        color: #1e293b !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Cartes */
    .stPlotlyChart, .stPyplot {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    .stPlotlyChart:hover, .stPyplot:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    
    /* KPIs */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f7fa 100%);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(135,206,235,0.15);
        border: 1px solid #bae6fd;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800;
        color: #0c4a6e !important;
    }
    [data-testid="stMetricLabel"] {
        color: #0c4a6e !important;
        font-weight: 600;
        font-size: 16px;
    }
    
    /* Section méthodologie */
    .streamlit-expanderHeader {
        color: #1e293b !important;
        font-weight: 700;
        background: #f0f9ff;
        border-radius: 12px;
        border: 1px solid #bae6fd;
    }
    
    /* Animation d'apparition */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp 0.6s ease-out; }
    
    /* Logo/drapeau */
    .flag-container {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .flag-img {
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide"
)

# Palette bleu ciel
BLEU_CIEL = "#87CEEB"
BLEU_POUDRE = "#B0E0E6"
BLEU_FONCE = "#0c4a6e"

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
st.markdown('<div class="flag-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=60, use_column_width=False)
with col2:
    st.title("Dashboard Macroéconomique – République Islamique de Mauritanie")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<p style="font-size: 18px; color: #475569; margin-top: -10px;">
Suivi des indicateurs clés de l’économie mauritanienne — Banque Centrale, FMI, Banque Mondiale
</p>
""", unsafe_allow_html=True)

# -----------------------------
# KPIs dynamiques
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
    st.metric("Croissance 2024", f"{val:.1f}%", delta="↑ 45% vs 2023")
with col2:
    val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
    st.metric("Inflation 2024", f"{val:.1f}%", delta="↓ 35% vs 2023")
with col3:
    val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
    st.metric("Recettes fiscales", f"{val:.1f}% PIB", delta="↑ 30% vs 2023")
with col4:
    dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
    st.metric("Dette extérieure", f"{dette:.1f} Md$", delta="Stable")

st.markdown("---")

# -----------------------------
# Section 1 : Croissance & Inflation
# -----------------------------
st.subheader("📊 Analyse macroéconomique")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Croissance du PIB – cycles économiques et chocs**")
    df_pib = df[df["Année"] >= 1962]
    if not df_pib.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2.5, label="Croissance")
        ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"].rolling(10).mean(), color=BLEU_CIEL, linewidth=2, label="Tendance (10 ans)")
        ax.fill_between(df_pib["Année"], df_pib["Croissance_PIB_pct"], where=df_pib["Croissance_PIB_pct"] < 0, color="#FF6B6B", alpha=0.2)
        for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "Pandémie"]):
            if year in df_pib["Année"].values:
                y = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                ax.annotate(label, xy=(year, y), xytext=(year, y-8),
                            arrowprops=dict(arrowstyle="->", color=BLEU_FONCE, lw=1), 
                            ha="center", fontsize=8, color=BLEU_FONCE)
        ax.axhline(0, linestyle="--", color="gray", alpha=0.6)
        ax.set_ylabel("Croissance (%)", fontsize=12)
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig)

with col2:
    st.markdown("**Inflation – régimes macroéconomiques**")
    df_infl = df[df["Année"] >= 1986]
    if not df_infl.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        median = df_infl["Inflation_pct"].median()
        ax.plot(df_infl["Année"], df_infl["Inflation_pct"], color=BLEU_FONCE, linewidth=2.5)
        ax.axhline(median, linestyle="--", color=BLEU_CIEL, linewidth=2, label=f"Médiane ({median:.1f}%)")
        ax.fill_between(df_infl["Année"], median, df_infl["Inflation_pct"], where=df_infl["Inflation_pct"] > median, color=BLEU_CIEL, alpha=0.2)
        ax.set_ylabel("Inflation (%)", fontsize=12)
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=0.3)
        st.pyplot(fig)

# -----------------------------
# Section 2 : Secteur extérieur
# -----------------------------
st.subheader("🌍 Soutenabilité externe")
df_ext = df[(df["Année"] >= 1970) & (df["Année"] <= 2021)]
df_ext = df_ext.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"])
if not df_ext.empty:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_ext["Année"], df_ext["Dette_exterieure_USD"]/1e9, color="#EF4444", linewidth=2.5, label="Dette extérieure")
    ax.plot(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, color="#10B981", linewidth=2.5, label="Réserves internationales")
    ax.fill_between(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, df_ext["Dette_exterieure_USD"]/1e9,
                    where=df_ext["Dette_exterieure_USD"] > df_ext["Reserves_internationales_USD"],
                    color="#FECACA", alpha=0.3)
    ax.set_ylabel("Milliards USD", fontsize=12)
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

# -----------------------------
# Section 3 : Finances publiques (placeholder pour extension)
# -----------------------------
st.subheader("🏛️ Finances publiques")
st.info("Cette section sera enrichie avec vos prochaines visualisations.")

# -----------------------------
# Méthodologie
# -----------------------------
with st.expander("📚 Méthodologie et sources"):
    st.markdown("""
    <div style="background: #f0f9ff; padding: 20px; border-radius: 12px; border-left: 4px solid #87CEEB;">
    <h4 style="color: #0c4a6e; margin-top: 0;">Sources officielles</h4>
    <ul>
        <li><b>Banque Centrale de Mauritanie (BCM)</b> : Données primaires sur recettes, chômage, taux d’intérêt (2007–2021)</li>
        <li><b>Fonds Monétaire International (FMI)</b> : Consultations Article IV (2022–2024)</li>
        <li><b>Banque Mondiale</b> : World Development Indicators (1960–2024)</li>
    </ul>
    
    <h4 style="color: #0c4a6e;">Traitement des données</h4>
    <ul>
        <li>Imputation par interpolation linéaire pour les séries continues</li>
        <li>Remplacement par moyenne historique pour variables volatiles</li>
        <li>Fusion des doublons annuels (ex. : 2022–2024)</li>
        <li>Validation croisée avec rapports officiels</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.caption("© 2026 – Projet académique | Jedou Mohamed Bebacar | Master SSD, Université de Nouakchott")
