
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = st.session_state.df

st.subheader("🔥 Corrélations (2007–2024)")
corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
corr = df[corr_vars].corr()
fig1 = go.Figure()
fig1.add_trace(go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='Blues', text=corr.values.round(2), texttemplate='%{text}'))
fig1.update_layout(title="Source : Calculs propres", height=400)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📦 Distribution par période")
df_box = df.copy()
df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])
fig2 = go.Figure()
for i, periode in enumerate(["1960-1980", "1981-2000", "2001-2024"]):
    data = df_box[df_box["Période"] == periode]["Croissance_PIB_pct"].dropna()
    color = ['#AEC7E8', '#1F77B4', '#0B3C5D'][i]
    fig2.add_trace(go.Box(y=data, name=periode, marker_color=color))
fig2.update_layout(title="Source : Banque Mondiale", yaxis_title="Croissance (%)", height=400, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)
