
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df
st.subheader("🔥 Corrélations entre indicateurs macroéconomiques (2007–2024)")

corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
corr = df[corr_vars].corr()
fig = go.Figure()
fig.add_trace(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='Blues', text=corr.values.round(2), texttemplate='%{text}', textfont={"size": 12}))
fig.update_layout(title="Source : Calculs propres", height=500, xaxis=dict(side='bottom'), yaxis=dict(side='left'))
st.plotly_chart(fig, use_container_width=True)
