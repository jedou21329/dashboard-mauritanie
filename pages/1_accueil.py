
import streamlit as st
import pandas as pd

df = st.session_state.df

st.subheader("🏠 Accueil")

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
Bienvenue sur le dashboard macroéconomique de la Mauritanie. Ce tableau de bord présente l’évolution des principaux indicateurs économiques, 
basé sur des données de la **Banque Centrale de Mauritanie (BCM)**, du **FMI** et de la **Banque Mondiale**.

### Sections disponibles :
- 📈 Croissance économique
- 🔥 Inflation
- 🌍 Secteur extérieur
- 🏛️ Finances publiques
- 👥 Marché du travail
- 💸 Envois de fonds
- 📊 Corrélations et régimes macroéconomiques

Utilisez le menu de navigation pour explorer les différentes dimensions de l’économie mauritanienne.
""")
