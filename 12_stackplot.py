
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("📚 Pression macroéconomique : inflation et chômage")

df_area = df.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_area["Année"], y=df_area["Inflation_pct"], mode='lines', name='Inflation', line=dict(width=0), fillcolor='#AEC7E8', fill='tonexty', stackgroup='one'))
fig.add_trace(go.Scatter(x=df_area["Année"], y=df_area["Taux_chomage_pct"], mode='lines', name='Chômage', line=dict(width=0), fillcolor='#1F77B4', fill='tonexty', stackgroup='one'))
fig.update_layout(title="Source : BCM, FMI", xaxis_title="Année", yaxis_title="%", height=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
st.plotly_chart(fig, use_container_width=True)
