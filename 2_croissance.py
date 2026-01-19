
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("📈 Croissance du PIB – cycles économiques et chocs")

df_pib = df[df["Année"] >= 1962].copy()
df_pib['Tendance'] = df_pib['Croissance_PIB_pct'].rolling(10, min_periods=1).mean()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_pib["Année"],
    y=df_pib["Croissance_PIB_pct"],
    mode='lines',
    name='Croissance',
    line=dict(color='#0B3C5D', width=2),
    hovertemplate='<b>%{x}</b><br>Croissance: %{y:.1f}%<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=df_pib["Année"],
    y=df_pib['Tendance'],
    mode='lines',
    name='Tendance (10 ans)',
    line=dict(color='#1F77B4', width=2),
    hovertemplate='<b>%{x}</b><br>Tendance: %{y:.1f}%<extra></extra>'
))

for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "Pandémie"]):
    if year in df_pib["Année"].values:
        y_val = df_pib.loc[df_pib["Année"] == year, "Croissance_PIB_pct"].values[0]
        fig.add_annotation(x=year, y=y_val, text=label, showarrow=True, arrowhead=2, arrowcolor='#0B3C5D', ax=0, ay=-40)

fig.update_layout(title="Source : BCM, FMI, Banque Mondiale", xaxis_title="Année", yaxis_title="Croissance (%)", hovermode='x unified', height=500)
st.plotly_chart(fig, use_container_width=True)
