
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("🏛️ Finances publiques (2007–2024)")

df_fp = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
fig = go.Figure()
fig.add_trace(go.Bar(x=df_fp["Année"], y=df_fp["Recettes_fiscales_pct_PIB"], name='Recettes fiscales (% PIB)', marker_color='#1F77B4'))
fig.update_layout(title="Source : FMI (2023)", xaxis_title="Année", yaxis_title="% du PIB", height=500)
st.plotly_chart(fig, use_container_width=True)
