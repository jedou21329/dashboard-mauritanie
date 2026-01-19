
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("👥 Taux de chômage (2007–2021)")

df_chom = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Taux_chomage_pct"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_chom["Année"], y=df_chom["Taux_chomage_pct"], mode='lines+markers', name='Taux de chômage', line=dict(color='#0B3C5D', width=2), marker=dict(size=8)))
fig.update_layout(title="Source : BCM", xaxis_title="Année", yaxis_title="Taux de chômage (%)", hovermode='x unified', height=500)
st.plotly_chart(fig, use_container_width=True)
