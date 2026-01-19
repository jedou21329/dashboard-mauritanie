
import streamlit as st

st.subheader("📚 Méthodologie et sources")

st.markdown("""
### Sources officielles
- **BCM** : Recettes, chômage, taux d'intérêt (2007–2021)
- **FMI** : Données 2022–2024
- **Banque Mondiale** : Séries longues (1960–2024)

### Traitement
- Imputation par interpolation linéaire
- Moyenne pour variables volatiles
- Fusion des doublons annuels

© 2026 – Jedou Mohamed Bebacar | Master SSD, Université de Nouakchott
""")
