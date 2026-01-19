
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("🔥 Inflation – régimes macroéconomiques")

df_infl = df[df["Année"] >= 1986].copy()
median = df_infl["Inflation_pct"].median()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_infl["Année"], y=df_infl["Inflation_pct"], mode='lines', name='Inflation', line=dict(color='#0B3C5D', width=2)))
fig.add_hline(y=median, line_dash="dash", line_color="#1F77B4", line_width=2, annotation_text=f"Médiane ({median:.1f}%)", annotation_position="right")
fig.update_layout(title="Source : BCM, FMI", xaxis_title="Année", yaxis_title="Inflation (%)", hovermode='x unified', height=500)
st.plotly_chart(fig, use_container_width=True)
