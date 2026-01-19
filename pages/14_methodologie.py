
import streamlit as st

st.subheader("📚 Méthodologie et sources de données")

st.markdown("""
### 📋 Sources officielles
- **Banque Centrale de Mauritanie (BCM)** – Données primaires sur recettes, chômage, taux d'intérêt (2007–2021)
- **Fonds Monétaire International (FMI)** – Consultations Article IV (2022–2024)
- **Banque Mondiale** – World Development Indicators (1960–2024)

### 🔧 Traitement des données
- ✓ Imputation par interpolation linéaire pour séries continues
- ✓ Remplacement par moyenne historique pour variables volatiles
- ✓ Fusion des doublons annuels (ex: 2022–2024)
- ✓ Validation croisée avec rapports officiels
- ✓ Normalisation des unités monétaires

### 📊 Indicateurs calculés
- Tendances mobiles (moyennes glissantes sur 10 ans)
- Ratios dette/réserves pour soutenabilité externe
- Écarts à la médiane historique
- Corrélations entre indicateurs macroéconomiques

Ce dashboard a été développé dans le cadre d'un projet académique au Master SSD, Université de Nouakchott.
""")

st.caption("© 2026 – Jedou Mohamed Bebacar | Master SSD, Université de Nouakchott")
