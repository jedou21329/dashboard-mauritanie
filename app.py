# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# -----------------------------
# Configuration + Favicon
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg",  # Favicon = drapeau
    layout="wide"
)

# -----------------------------
# CSS Professionnel – Style BCM/FMI
# -----------------------------
st.markdown("""
<style>
    .main { background: #f8fafc; }
    h1, h2, h3 { color: #0B3C5D; font-weight: bold; }
    .stPlotlyChart {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    [data-testid="stMetric"] {
        background: #f0f9ff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(11,60,93,0.1);
    }
    [data-testid="stMetricValue"] {
        color: #0B3C5D !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
    df["Année"] = df["Année"].astype(int)
    df = df.groupby("Année", as_index=False).first()
    df = df.sort_values("Année").reset_index(drop=True)
    
    # Imputation (ton code original)
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
# Menu latéral – Icônes professionnelles
# -----------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=60)
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Sections économiques",
    [
        "🏠 Accueil",
        "📈 Croissance & Cycles Économiques",
        "📊 Stabilité des Prix (Inflation)",
        "🌍 Soutenabilité du Secteur Extérieur",
        "🏛️ Finances Publiques",
        "👥 Marché du Travail",
        "💸 Flux Financiers Internationaux",
        "🔍 Analyses Transversales",
        "📚 Méthodologie"
    ]
)

# -----------------------------
# En-tête
# -----------------------------
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=80)
with col2:
    st.title("Dashboard Macroéconomique – République Islamique de Mauritanie")
    st.markdown("Banque Centrale de Mauritanie • FMI • Banque Mondiale")

st.markdown("---")

# -----------------------------
# Fonction pour charger une visualisation EXACTE
# -----------------------------
def load_viz(filename):
    """Charge le code exact de ta visualisation Plotly"""
    with open(f"pages/{filename}.py", "r", encoding="utf-8") as f:
        code = f.read()
        exec(code, {"st": st, "pd": pd, "go": go, "df": df})

# -----------------------------
# Affichage par section
# -----------------------------
if page == "🏠 Accueil":
    # KPIs avec ta palette
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
        st.metric("Croissance 2024", f"{val:.1f}%")
    with col2:
        val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
        st.metric("Inflation 2024", f"{val:.1f}%")
    with col3:
        val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
        st.metric("Recettes fiscales", f"{val:.1f}% PIB")
    with col4:
        dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
        st.metric("Dette extérieure", f"{dette:.1f} Md$")
    
    st.markdown("Utilisez le menu de gauche pour explorer les sections.")

elif page == "📈 Croissance & Cycles Économiques":
    load_viz("1_croissance_pib_cycles")

elif page == "📊 Stabilité des Prix (Inflation)":
    load_viz("2_inflation_regimes")

elif page == "🌍 Soutenabilité du Secteur Extérieur":
    load_viz("3_dette_reserves")

elif page == "🏛️ Finances Publiques":
    load_viz("4_recettes_fiscales")

elif page == "👥 Marché du Travail":
    load_viz("5_chomage_barres")

elif page == "💸 Flux Financiers Internationaux":
    load_viz("6_envois_fonds")

elif page == "🔍 Analyses Transversales":
    st.subheader("Corrélations entre indicateurs")
    load_viz("7_heatmap_correlation")
    
    st.subheader("Distribution par période")
    load_viz("9_boxplot_periodes")
    
    st.subheader("Volatilité de la croissance")
    load_viz("11_volatilite_croissance")

elif page == "📚 Méthodologie":
    load_viz("14_methodologie")
