
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df
st.subheader("🥧 Poids des recettes fiscales – 2024")

val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
fig = go.Figure()
fig.add_trace(go.Pie(labels=['Recettes fiscales', 'Autres'], values=[val, 100-val], marker=dict(colors=['#1F77B4', '#AEC7E8']), textinfo='label+percent'))
fig.update_layout(title="Source : FMI (2023)", height=500)
st.plotly_chart(fig, use_container_width=True)
