
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df
st.subheader("💹 Courbe de Phillips – Mauritanie (2007–2021)")

df_ph = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_ph["Taux_chomage_pct"], y=df_ph["Inflation_pct"], mode='markers', marker=dict(size=12, color=df_ph["Année"], colorscale='Blues', showscale=True, colorbar=dict(title="Année"), line=dict(width=1, color='black')), text=df_ph["Année"]))
fig.update_layout(title="Source : BCM", xaxis_title="Chômage (%)", yaxis_title="Inflation (%)", height=500)
st.plotly_chart(fig, use_container_width=True)
