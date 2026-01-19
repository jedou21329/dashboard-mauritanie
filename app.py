
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="📊",
    layout="wide"
)

BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"

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

df = load_and_clean_data()

st.title("🇲🇷 Dashboard Macroéconomique – Mauritanie")
st.markdown("Données : BCM, FMI, Banque Mondiale")

# 1. Croissance du PIB
st.subheader("1. Croissance du PIB – cycles économiques et chocs")
df_pib = df[df["Année"] >= 1962]
if not df_pib.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2, label="Croissance")
    ax.plot(df_pib["Année"], df_pib["Croissance_PIB_pct"].rolling(10).mean(), color=BLEU_MOYEN, linewidth=3, label="Tendance long terme")
    ax.fill_between(df_pib["Année"], df_pib["Croissance_PIB_pct"], where=df_pib["Croissance_PIB_pct"] < 0, color=BLEU_CLAIR, alpha=0.6)
    for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
        if year in df_pib["Année"].values:
            y = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
            ax.annotate(label, xy=(year, y), xytext=(year, y-6),
                        arrowprops=dict(arrowstyle="->", color=BLEU_FONCE), ha="center", fontsize=9)
    ax.axhline(0, linestyle="--", color="gray")
    ax.set_ylabel("Croissance (%)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)
else:
    st.warning("Données indisponibles.")

# 2. Inflation
st.subheader("2. Inflation – régimes macroéconomiques")
df_infl = df[df["Année"] >= 1986]
if not df_infl.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    median = df_infl["Inflation_pct"].median()
    ax.plot(df_infl["Année"], df_infl["Inflation_pct"], color=BLEU_FONCE, linewidth=2)
    ax.axhline(median, linestyle="--", color=BLEU_MOYEN, label=f"Inflation médiane ({median:.1f}%)")
    ax.fill_between(df_infl["Année"], median, df_infl["Inflation_pct"], where=df_infl["Inflation_pct"] > median, color=BLEU_CLAIR, alpha=0.6, label="Régime inflation élevée")
    ax.set_ylabel("Inflation (%)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)
else:
    st.warning("Données indisponibles.")

# 3. Dette vs Réserves
st.subheader("3. Soutenabilité externe : dette vs réserves")
df_ext = df[(df["Année"] >= 1970) & (df["Année"] <= 2021)]
df_ext = df_ext.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"])
if not df_ext.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_ext["Année"], df_ext["Dette_exterieure_USD"]/1e9, color=BLEU_FONCE, linewidth=2, label="Dette extérieure")
    ax.plot(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, color=BLEU_MOYEN, linewidth=2, label="Réserves")
    ax.fill_between(df_ext["Année"], df_ext["Reserves_internationales_USD"]/1e9, df_ext["Dette_exterieure_USD"]/1e9,
                    where=df_ext["Dette_exterieure_USD"] > df_ext["Reserves_internationales_USD"],
                    color=BLEU_CLAIR, alpha=0.6, label="Zone de vulnérabilité externe")
    ax.set_ylabel("Milliards USD")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)
else:
    st.warning("Données insuffisantes.")

st.markdown("---")
st.caption("© 2026 – Jedou Mohamed Bebacar | Master SSD, Université de Nouakchott")
