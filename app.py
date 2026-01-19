
# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# CSS AVANCÉ – Design BCM/FMI
# -----------------------------
st.markdown("""
<style>
    /* Fond principal */
    .main {
        background: linear-gradient(135deg, #0B3C5D 0%, #1F77B4 100%);
        color: white;
    }
    
    /* Titres */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Cartes de graphiques */
    .stPlotlyChart, .stPyplot {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stPlotlyChart:hover, .stPyplot:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }
    
    /* KPIs */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: bold;
        color: #0B3C5D !important;
    }
    [data-testid="stMetricLabel"] {
        color: #1F77B4 !important;
        font-weight: 600;
    }
    
    /* Section méthodologie */
    .streamlit-expanderHeader {
        color: white !important;
        font-weight: bold;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    /* Footer */
    footer { visibility: hidden; }
    
    /* Animation d'apparition */
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
    .fade-in {
        animation: fadeInUp 1s ease-out;
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

BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLANC = "#FFFFFF"

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
# En-tête animé
# -----------------------------
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=80)
with col2:
    st.title("🇲🇷 Dashboard Macroéconomique – Mauritanie")

st.markdown("""
<p style="font-size: 18px; color: #E6F0FA;">
Suivi des indicateurs clés de l’économie mauritanienne — Banque Centrale, FMI, Banque Mondiale
</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# KPIs animés
# -----------------------------
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
    st.metric("Croissance 2024", f"{val:.1f}%")
with col2:
    val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
    st.metric("Inflation 2024", f"{val:.1f}%")
with col3:
    val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
    st.metric("Recettes fiscales", f"{val:.1f}% PIB")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Graphiques animés
# -----------------------------
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.subheader("📊 Analyse macroéconomique")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Croissance du PIB – cycles et chocs**")
    df_pib = df[df["Année"] >= 1962]
    if not df_pib.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2.5)
        ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"].rolling(10).mean(), color=BLEU_MOYEN, linewidth=2)
        ax.fill_between(df_pib["Année"], df_pib["Croissance_PIB_pct"], where=df_pib["Croissance_PIB_pct"] < 0, color="#FF6B6B", alpha=0.3)
        for year in [1975, 2009, 2020]:
            if year in df_pib["Année"].values:
                y = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
                ax.annotate("", xy=(year, y), xytext=(year, y-8),
                            arrowprops=dict(arrowstyle="->", color="white", lw=1.5))
        ax.axhline(0, linestyle="--", color="white", alpha=0.7)
        ax.set_facecolor("#0B3C5D")
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.set_ylabel("Croissance (%)", color="white")
        st.pyplot(fig)

with col2:
    st.markdown("**Inflation – régimes macroéconomiques**")
    df_infl = df[df["Année"] >= 1986]
    if not df_infl.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        median = df_infl["Inflation_pct"].median()
        ax.plot(df_infl["Année"], df_infl["Inflation_pct"], color=BLEU_MOYEN, linewidth=2.5)
        ax.axhline(median, linestyle="--", color="gold", linewidth=2)
        ax.fill_between(df_infl["Année"], median, df_infl["Inflation_pct"], where=df_infl["Inflation_pct"] > median, color="orange", alpha=0.3)
        ax.set_facecolor("#0B3C5D")
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.set_ylabel("Inflation (%)", color="white")
        st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Dette vs Réserves
# -----------------------------
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.subheader("🌍 Soutenabilité externe")
df_ext = df[(df["Année"] >= 1970) & (df["Année"] <= 2021)]
df_ext = df_ext.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"])
if not df_ext.empty:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_ext["Année"], df_ext["Dette_exterieure_USD"]/1e9, color="#FF6B6B", linewidth=2.5, label="Dette extérieure")
    ax.plot(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, color="#4ECDC4", linewidth=2.5, label="Réserves")
    ax.fill_between(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, df_ext["Dette_exterieure_USD"]/1e9,
                    where=df_ext["Dette_exterieure_USD"] > df_ext["Reserves_internationales_USD"],
                    color="#FF6B6B", alpha=0.2)
    ax.set_facecolor("#0B3C5D")
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.set_ylabel("Milliards USD", color="white")
    ax.legend(facecolor="#0B3C5D", labelcolor="white")
    st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Méthodologie
# -----------------------------
with st.expander("📚 Méthodologie et sources"):
    st.markdown("""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
    <h4 style="color: white;">Sources des données</h4>
    <ul>
        <li><b>Banque Centrale de Mauritanie (BCM)</b> : Recettes, chômage, taux d’intérêt (2007–2021)</li>
        <li><b>FMI (Article IV, 2023)</b> : Données 2022–2024</li>
        <li><b>Banque Mondiale</b> : Séries longues (1960–2024)</li>
    </ul>
    
    <h4 style="color: white;">Traitement</h4>
    <ul>
        <li>Imputation par interpolation linéaire</li>
        <li>Moyenne historique pour variables volatiles</li>
        <li>Fusion des doublons annuels</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.caption("© 2026 – Projet académique | Jedou Mohamed Bebacar | Master SSD, Université de Nouakchott")
