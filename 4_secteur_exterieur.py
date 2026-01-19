
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("🌍 Soutenabilité externe : dette vs réserves")

df_ext = df.dropna(subset=["Dette_exterieure_USD", "Reserves_internationales_USD"]).copy()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Dette_exterieure_USD"]/1e9, mode='lines', name='Dette extérieure', line=dict(color='#EF4444', width=2)))
fig.add_trace(go.Scatter(x=df_ext["Année"], y=df_ext["Reserves_internationales_USD"]/1e9, mode='lines', name='Réserves', line=dict(color='#10B981', width=2)))
fig.update_layout(title="Source : Banque Mondiale", xaxis_title="Année", yaxis_title="Milliards USD", hovermode='x unified', height=500)
st.plotly_chart(fig, use_container_width=True)
