
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("📊 Dette extérieure vs Réserves")
df_dr = df.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_dr["Année"], y=df_dr["Dette_exterieure_USD"]/1e9, mode='lines', name='Dette', line=dict(color='#EF4444')))
fig1.add_trace(go.Scatter(x=df_dr["Année"], y=df_dr["Reserves_internationales_USD"]/1e9, mode='lines', name='Réserves', line=dict(color='#10B981')))
fig1.update_layout(title="Source : Banque Mondiale", xaxis_title="Année", yaxis_title="Md$", height=400)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("💹 Courbe de Phillips (2007–2021)")
df_ph = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_ph["Taux_chomage_pct"], y=df_ph["Inflation_pct"], mode='markers', marker=dict(size=12, color=df_ph["Année"], colorscale='Blues', showscale=True)))
fig2.update_layout(title="Source : BCM", xaxis_title="Chômage (%)", yaxis_title="Inflation (%)", height=400)
st.plotly_chart(fig2, use_container_width=True)
