# app.py
import streamlit as st
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide"
)

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

# Stocker dans session_state
if 'df' not in st.session_state:
    st.session_state.df = load_and_clean_data()

# -----------------------------
# En-tête
# -----------------------------
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=80)
with col2:
    st.title("Dashboard Macroéconomique – République Islamique de Mauritanie")
    st.markdown("Suivi des indicateurs clés de l’économie mauritanienne — Banque Centrale, FMI, Banque Mondiale")

st.markdown("---")

# -----------------------------
# Menu latéral
# -----------------------------
st.sidebar.header("🧭 Navigation")

page = st.sidebar.radio(
    "Sélectionnez une section",
    [
        "🏠 Accueil",
        "📈 Croissance",
        "🔥 Inflation",
        "🌍 Secteur Extérieur",
        "🏛️ Finances Publiques",
        "👥 Taux de Chômage",
        "💸 Envois de Fond",
        "📊 Dette vs Réserves",
        "💹 Courbe de Phillips",
        "🥧 Pie Chart 2024",
        "🔥 Heatmap",
        "📚 Stackplot",
        "📦 Boxplot par Période",
        "📚 Méthodologie"
    ]
)

# -----------------------------
# Affichage selon la page sélectionnée
# -----------------------------
if page == "🏠 Accueil":
    st.subheader("Bienvenue sur le Dashboard Macroéconomique de la Mauritanie")
    st.markdown("""
    Ce dashboard présente l’évolution des principaux indicateurs économiques de la Mauritanie, 
    basé sur des données de la **Banque Centrale de Mauritanie (BCM)**, du **FMI** et de la **Banque Mondiale**.
    """)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        val = st.session_state.df.loc[st.session_state.df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
        st.metric("Croissance 2024", f"{val:.1f}%", delta="↑ 45% vs 2023")
    with col2:
        val = st.session_state.df.loc[st.session_state.df["Année"] == 2024, "Inflation_pct"].iloc[0]
        st.metric("Inflation 2024", f"{val:.1f}%", delta="↓ 35% vs 2023")
    with col3:
        val = st.session_state.df.loc[st.session_state.df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
        st.metric("Recettes fiscales", f"{val:.1f}% PIB", delta="↑ 30% vs 2023")
    with col4:
        dette = st.session_state.df.loc[st.session_state.df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
        st.metric("Dette extérieure", f"{dette:.1f} Md$", delta="Stable")
    
    st.markdown("---")
    st.info("Utilisez le menu de gauche pour naviguer entre les sections.")

elif page == "📈 Croissance":
    st.subheader("📈 Croissance du PIB – cycles économiques et chocs")
    # Code de la page croissance ici (à importer depuis pages/croissance.py)
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "🔥 Inflation":
    st.subheader("🔥 Inflation – régimes macroéconomiques")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "🌍 Secteur Extérieur":
    st.subheader("🌍 Soutenabilité externe : dette vs réserves")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "🏛️ Finances Publiques":
    st.subheader("🏛️ Finances publiques")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "👥 Taux de Chômage":
    st.subheader("👥 Taux de chômage")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "💸 Envois de Fond":
    st.subheader("💸 Envois de fonds")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "📊 Dette vs Réserves":
    st.subheader("📊 Dette extérieure vs Réserves internationales")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "💹 Courbe de Phillips":
    st.subheader("💹 Courbe de Phillips")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "🥧 Pie Chart 2024":
    st.subheader("🥧 Poids des recettes fiscales – 2024")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "🔥 Heatmap":
    st.subheader("🔥 Corrélations entre indicateurs")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "📚 Stackplot":
    st.subheader("📚 Pression macroéconomique : inflation et chômage")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "📦 Boxplot par Période":
    st.subheader("📦 Distribution de la croissance du PIB par période")
    st.warning("Page en construction — à venir dans la version finale.")

elif page == "📚 Méthodologie":
    st.subheader("📚 Méthodologie et sources")
    st.markdown("""
    **Sources** :
    - Banque Centrale de Mauritanie (BCM) : 2007–2021
    - FMI (Article IV, 2023) : 2022–2024
    - Banque Mondiale : 1960–2024
    
    **Traitement** :
    - Imputation par interpolation linéaire
    - Moyenne pour variables volatiles
    - Fusion des doublons annuels
    """)
