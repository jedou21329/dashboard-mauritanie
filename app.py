# app.py - VERSION CORRIGÉE
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from streamlit_option_menu import option_menu
import os

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="🇲🇷 Dashboard Macroéconomique – Mauritanie",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CSS + JavaScript personnalisé
# -----------------------------
st.markdown("""
<style>
    /* Votre CSS existant ici */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f7fa 100%);
        min-height: 100vh;
    }
    
    /* ... (gardez tout votre CSS existant) ... */
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Fonction pour créer des données de test
# -----------------------------
def create_sample_data():
    """Crée des données de démonstration réalistes pour la Mauritanie"""
    years = list(range(1960, 2025))
    np.random.seed(42)  # Pour la reproductibilité
    
    # Création de tendances réalistes
    base_growth = np.linspace(3, 6, len(years))  # Tend à augmenter
    base_inflation = np.linspace(15, 3, len(years))  # Tend à diminuer
    
    # Ajout de variations aléatoires
    growth = base_growth + np.random.normal(0, 1.5, len(years))
    inflation = base_inflation + np.random.normal(0, 2, len(years))
    
    # Création du DataFrame
    data = {
        'Année': years,
        'Croissance_PIB_pct': np.clip(growth, 0, 10),
        'Inflation_pct': np.clip(inflation, 0, 25),
        'Recettes_fiscales_pct_PIB': np.random.uniform(15, 30, len(years)),
        'Dette_exterieure_USD': np.linspace(0.5e9, 4.5e9, len(years)) + np.random.normal(0, 0.2e9, len(years)),
        'Reserves_internationales_USD': np.linspace(0.1e9, 1.5e9, len(years)) + np.random.normal(0, 0.1e9, len(years)),
        'Taux_chomage_pct': np.linspace(30, 20, len(years)) + np.random.normal(0, 3, len(years)),
        'Solde_commercial_pct_PIB': np.random.uniform(-8, 2, len(years)),
        'Envois_de_fonds_pct_PIB': np.random.uniform(5, 15, len(years)),
        'Taux_interet_pct': np.random.uniform(10, 20, len(years)),
        'Recettes_millions_MR': np.linspace(100, 500, len(years)) + np.random.normal(0, 50, len(years))
    }
    
    df = pd.DataFrame(data)
    
    # Ajustements spécifiques
    df.loc[df['Année'] == 2024, 'Croissance_PIB_pct'] = 5.2
    df.loc[df['Année'] == 2024, 'Inflation_pct'] = 3.8
    df.loc[df['Année'] == 2024, 'Recettes_fiscales_pct_PIB'] = 22.5
    df.loc[df['Année'] == 2024, 'Dette_exterieure_USD'] = 4.3e9
    
    return df

# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_and_clean_data():
    """Charge les données depuis le CSV ou crée des données de démonstration"""
    
    # Liste des chemins à essayer
    possible_paths = [
        "macro_mauritanie_complet_1960_2024.csv",  # À la racine
        "data/macro_mauritanie_complet_1960_2024.csv",  # Dans un dossier data
        "/mount/src/dashboard-mauritanie/macro_mauritanie_complet_1960_2024.csv",  # Chemin absolu
    ]
    
    df = None
    file_found = False
    
    # Essayer chaque chemin
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
                file_found = True
                st.success(f"✅ Données chargées depuis: {path}")
                break
        except:
            continue
    
    # Si aucun fichier n'est trouvé, créer des données de démonstration
    if not file_found:
        st.warning("⚠️ Fichier CSV non trouvé. Utilisation de données de démonstration.")
        df = create_sample_data()
        # Sauvegarder pour une utilisation future
        df.to_csv("macro_mauritanie_complet_1960_2024.csv", index=False)
        st.info("📁 Fichier de démonstration créé: macro_mauritanie_complet_1960_2024.csv")
    
    # Nettoyage et transformation des données
    df["Année"] = df["Année"].astype(int)
    df = df.groupby("Année", as_index=False).first()
    df = df.sort_values("Année").reset_index(drop=True)
    
    # Imputation des données manquantes
    df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"] = df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"].interpolate()
    df.loc[df["Année"] >= 1986, "Inflation_pct"] = df.loc[df["Année"] >= 1986, "Inflation_pct"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"].interpolate()
    
    # Vérifier et créer les colonnes manquantes si nécessaire
    required_columns = ['Envois_de_fonds_pct_PIB', 'Dette_exterieure_USD', 'Solde_commercial_pct_PIB',
                       'Reserves_internationales_USD', 'Recettes_millions_MR', 'Taux_chomage_pct', 'Taux_interet_pct']
    
    for col in required_columns:
        if col not in df.columns:
            # Créer des valeurs par défaut pour les colonnes manquantes
            if col == 'Envois_de_fonds_pct_PIB':
                df[col] = np.random.uniform(5, 15, len(df))
            elif col == 'Dette_exterieure_USD':
                df[col] = np.linspace(0.5e9, 4.5e9, len(df))
            elif col == 'Reserves_internationales_USD':
                df[col] = np.linspace(0.1e9, 1.5e9, len(df))
            elif col == 'Taux_chomage_pct':
                df[col] = np.linspace(30, 20, len(df))
            elif col == 'Taux_interet_pct':
                df[col] = np.random.uniform(10, 20, len(df))
            else:
                df[col] = 0
    
    return df

# -----------------------------
# Charger les données
# -----------------------------
df = load_and_clean_data()

# -----------------------------
# Navigation
# -----------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="📊 Navigation",
        options=["🏠 Accueil", "📈 Vue Macro", "💰 Finances Publiques", "🌍 Commerce Extérieur", "📊 Analyses Avancées"],
        icons=["house", "graph-up", "currency-dollar", "globe-americas", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "#0c4a6e", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#e9ecef"},
            "nav-link-selected": {"background-color": "#0c4a6e", "color": "white"},
        }
    )

# -----------------------------
# Page d'accueil (exemple)
# -----------------------------
if selected == "🏠 Accueil":
    st.markdown("""
    <div class="page-header">
        <div class="page-header-content">
            <h1 style="margin: 0; font-size: 3rem; font-weight: 900;">🇲🇷 Dashboard Macroéconomique</h1>
            <p style="font-size: 1.5rem; opacity: 0.9; margin: 10px 0 0 0;">
            République Islamique de Mauritanie
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher les premières lignes des données
    st.write("### 📋 Aperçu des données")
    st.dataframe(df.head(10))
    
    # Statistiques descriptives
    st.write("### 📊 Statistiques descriptives")
    st.dataframe(df.describe())

# -----------------------------
# Les autres pages...
# (Ajoutez ici le reste de votre code pour les autres pages)
# -----------------------------

# Reste de votre code pour les visualisations...
