
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide"
)

@st.cache_data
def load_and_clean_data():
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
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Recettes_millions_MR"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Recettes_millions_MR"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].fillna(df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].mean())
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2017), "Taux_interet_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2017), "Taux_interet_pct"].fillna(17.0)
    
    return df

if 'df' not in st.session_state:
    st.session_state.df = load_and_clean_data()

col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=80)
with col2:
    st.title("Dashboard Macroéconomique – République Islamique de Mauritanie")
    st.markdown("Suivi des indicateurs clés — Banque Centrale, FMI, Banque Mondiale")

st.markdown("---")

df = st.session_state.df
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

st.markdown("""
Bienvenue sur le dashboard macroéconomique de la Mauritanie.  
Utilisez le **menu de gauche** pour explorer les différentes dimensions de l’économie.
""")
