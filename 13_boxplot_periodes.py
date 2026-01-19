
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("📦 Distribution de la croissance du PIB par période")

df_box = df.copy()
df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])
fig = go.Figure()
for i, periode in enumerate(["1960-1980", "1981-2000", "2001-2024"]):
    data = df_box[df_box["Période"] == periode]["Croissance_PIB_pct"].dropna()
    color = ['#AEC7E8', '#1F77B4', '#0B3C5D'][i]
    fig.add_trace(go.Box(y=data, name=periode, marker_color=color, boxmean='sd'))
fig.update_layout(title="Source : Banque Mondiale", yaxis_title="Croissance (%)", height=500, showlegend=False)
st.plotly_chart(fig, use_container_width=True)
