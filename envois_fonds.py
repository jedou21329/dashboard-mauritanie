
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df
st.subheader("💸 Envois de fonds des migrants (% PIB, 1975–2024)")

df_rem = df[df["Année"] >= 1975].dropna(subset=["Envois_de_fonds_pct_PIB"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_rem["Année"], y=df_rem["Envois_de_fonds_pct_PIB"], mode='lines+markers', name='Envois de fonds', line=dict(color='#1F77B4', width=2), marker=dict(size=6)))
fig.update_layout(title="Source : Banque Mondiale", xaxis_title="Année", yaxis_title="Envois de fonds (% PIB)", hovermode='x unified', height=500)
st.plotly_chart(fig, use_container_width=True)
