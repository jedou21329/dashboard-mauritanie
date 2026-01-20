
# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="Dashboard Macroéconomique - Mauritanie",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg",
    layout="wide"
)

# -----------------------------
# CSS + JavaScript
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #1e293b;
    }
    
    h1 {
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        letter-spacing: -1px;
        animation: slideInDown 0.8s ease-out;
    }
    
    h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        animation: fadeInUp 0.6s ease-out;
    }
    
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 48px rgba(12, 74, 110, 0.15);
        border: 1px solid #87CEEB;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: countUp 1s ease-out;
    }
    
    .stPyplot {
        background: white;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
        transition: all 0.4s ease;
        border: 1px solid #e2e8f0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .stPyplot:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
    }
    
    .header-container {
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 32px 0;
        animation: slideInLeft 0.8s ease-out;
    }
    
    .flag-img {
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transition: transform 0.3s ease;
    }
    
    .flag-img:hover {
        transform: scale(1.05) rotate(2deg);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 0;
        border-bottom: 3px solid #87CEEB;
        margin-bottom: 24px;
        animation: slideInRight 0.6s ease-out;
    }
    
    .section-icon svg {
        width: 28px;
        height: 28px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes slideInLeft { from { opacity: 0; transform: translateX(-50px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes slideInRight { from { opacity: 0; transform: translateX(50px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes countUp { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
</style>

<script>
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
            }
        });
    });
    document.querySelectorAll('.stPyplot').forEach(el => observer.observe(el));
</script>
""", unsafe_allow_html=True)

# -----------------------------
# Chargement des données
# -----------------------------
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("macro_mauritanie_complet_1960_2024.csv")
    df["Année"] = df["Année"].astype(int)
    df = df.groupby("Année", as_index=False).first()
    df = df.sort_values("Année").reset_index(drop=True)
    
    df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"] = df.loc[df["Année"] >= 1962, "Croissance_PIB_pct"].interpolate()
    df.loc[df["Année"] >= 1986, "Inflation_pct"] = df.loc[df["Année"] >= 1986, "Inflation_pct"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2024), "Recettes_fiscales_pct_PIB"].interpolate()
    df.loc[df["Année"] >= 1975, "Envois_de_fonds_pct_PIB"] = df.loc[df["Année"] >= 1975, "Envois_de_fonds_pct_PIB"].interpolate(limit=4).fillna(df["Envois_de_fonds_pct_PIB"].mean())
    df.loc[df["Année"] >= 1970, "Dette_exterieure_USD"] = df.loc[df["Année"] >= 1970, "Dette_exterieure_USD"].interpolate()
    df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"] = df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"].fillna(df.loc[df["Année"] >= 1961, "Solde_commercial_pct_PIB"].mean())
    df.loc[(df["Année"] >= 1963) & (df["Année"] <= 2021), "Reserves_internationales_USD"] = df.loc[(df["Année"] >= 1963) & (df["Année"] <= 2021), "Reserves_internationales_USD"].interpolate()
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].fillna(df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2021), "Taux_chomage_pct"].mean())
    df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2017), "Taux_interet_pct"] = df.loc[(df["Année"] >= 2007) & (df["Année"] <= 2017), "Taux_interet_pct"].fillna(17.0)
    
    return df

df = load_and_clean_data()

# -----------------------------
# Palette
# -----------------------------
BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"
BLEU_TRES_CLAIR = "#E6F0FA"

plt.rcParams.update({
    "axes.edgecolor": BLEU_FONCE,
    "axes.labelcolor": BLEU_FONCE,
    "xtick.color": BLEU_FONCE,
    "ytick.color": BLEU_FONCE,
    "text.color": BLEU_FONCE,
    "font.size": 11,
    "figure.dpi": 150
})

# -----------------------------
# En-tête
# -----------------------------
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Mauritania.svg", width=100)
with col2:
    st.title("Dashboard Macroéconomique - République Islamique de Mauritanie")
    st.markdown("""
    <p style="font-size: 18px; color: #64748b; margin-top: -15px; font-weight: 500;">
    Suivi en temps réel des indicateurs économiques • Banque Centrale • FMI • Banque Mondiale
    </p>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# KPIs
# -----------------------------
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M3 13H5V19H3V13ZM7 9H9V19H7V9ZM11 7H13V19H11V7ZM15 11H17V19H15V11ZM19 5H21V19H19V5Z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Indicateurs clés 2024</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    val = df.loc[df["Année"] == 2024, "Croissance_PIB_pct"].iloc[0]
    st.metric("Croissance PIB", f"{val:.1f}%", delta="+1.9 pts vs 2023")
with col2:
    val = df.loc[df["Année"] == 2024, "Inflation_pct"].iloc[0]
    st.metric("Inflation", f"{val:.1f}%", delta="-1.4 pts vs 2023")
with col3:
    val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].iloc[0]
    st.metric("Recettes fiscales", f"{val:.1f}% PIB", delta="+3.8 pts vs 2023")
with col4:
    dette = df.loc[df["Année"] == 2024, "Dette_exterieure_USD"].iloc[0] / 1e9
    st.metric("Dette extérieure", f"{dette:.1f} Md$", delta="Stable")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Visualisations
# -----------------------------

# 1. Croissance du PIB
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M3 13H5V19H3V13ZM7 9H9V19H7V9ZM11 7H13V19H11V7ZM15 11H17V19H15V11ZM19 5H21V19H19V5Z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Croissance du PIB - cycles économiques et chocs</h2>
</div>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(df["Année"], df["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2, label="Croissance")
ax.plot(df["Année"], df["Croissance_PIB_pct"].rolling(10).mean(), color=BLEU_MOYEN, linewidth=3, label="Tendance long terme")
ax.fill_between(df["Année"], df["Croissance_PIB_pct"], where=df["Croissance_PIB_pct"] < 0, color=BLEU_CLAIR, alpha=0.6)
for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
    if year in df["Année"].values:
        y = df.loc[df["Année"] == year, "Croissance_PIB_pct"].values[0]
        ax.annotate(label, xy=(year, y), xytext=(year, y-6),
                    arrowprops=dict(arrowstyle="->", color=BLEU_FONCE), ha="center", fontsize=9)
ax.axhline(0, linestyle="--", color="gray")
ax.set_title("Source : BCM, FMI, Banque Mondiale", fontsize=12)
ax.set_ylabel("%")
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close()

# 2. Inflation
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Inflation - régimes macroéconomiques</h2>
</div>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(14, 4))
median = df["Inflation_pct"].median()
ax.plot(df["Année"], df["Inflation_pct"], color=BLEU_FONCE, linewidth=2)
ax.axhline(median, linestyle="--", color=BLEU_MOYEN, label=f"Inflation médiane ({median:.1f}%)")
ax.fill_between(df["Année"], median, df["Inflation_pct"], where=df["Inflation_pct"] > median, color=BLEU_CLAIR, alpha=0.6, label="Régime inflation élevée")
ax.set_title("Source : BCM, FMI", fontsize=12)
ax.set_ylabel("%")
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close()

# 3. Dette vs Réserves
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Soutenabilité externe : dette vs réserves</h2>
</div>
""", unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df["Année"], df["Dette_exterieure_USD"]/1e9, color=BLEU_FONCE, linewidth=2, label="Dette extérieure")
ax.plot(df["Année"], df["Reserves_internationales_USD"]/1e9, color=BLEU_MOYEN, linewidth=2, label="Réserves")
ax.fill_between(df["Année"], df["Reserves_internationales_USD"]/1e9, df["Dette_exterieure_USD"]/1e9,
                where=df["Dette_exterieure_USD"] > df["Reserves_internationales_USD"],
                color=BLEU_CLAIR, alpha=0.6, label="Zone de vulnérabilité externe")
ax.set_title("Source : Banque Mondiale", fontsize=12)
ax.set_ylabel("Milliards USD")
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close()

# 4. Croissance vs Chômage
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Croissance économique et chômage (2007-2021)</h2>
</div>
""", unsafe_allow_html=True)

df_cc = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Croissance_PIB_pct", "Taux_chomage_pct"])
x = np.arange(len(df_cc))
w = 0.4
fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(x - w/2, df_cc["Croissance_PIB_pct"], w, label="Croissance PIB", color=BLEU_MOYEN)
ax.bar(x + w/2, df_cc["Taux_chomage_pct"], w, label="Chômage", color=BLEU_CLAIR)
for i in range(len(df_cc)):
    ax.text(i - w/2, df_cc["Croissance_PIB_pct"].iloc[i] + 0.3, f"{df_cc['Croissance_PIB_pct'].iloc[i]:.1f}%", ha="center", fontsize=8)
    ax.text(i + w/2, df_cc["Taux_chomage_pct"].iloc[i] + 0.3, f"{df_cc['Taux_chomage_pct'].iloc[i]:.1f}%", ha="center", fontsize=8)
ax.set_xticks(x)
ax.set_xticklabels(df_cc["Année"], rotation=45)
ax.set_ylabel("%")
ax.set_title("Source : BCM", fontsize=12)
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
plt.close()

# 5. Courbe de Phillips
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Courbe de Phillips - Mauritanie (2007-2021)</h2>
</div>
""", unsafe_allow_html=True)

df_ph = df[(df["Année"] >= 2007) & (df["Année"] <= 2021)].dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
fig, ax = plt.subplots(figsize=(8, 6))
sc = ax.scatter(df_ph["Taux_chomage_pct"], df_ph["Inflation_pct"], c=df_ph["Année"], cmap="Blues", s=90, edgecolor="black")
plt.colorbar(sc, ax=ax, label="Année")
ax.set_xlabel("Chômage (%)")
ax.set_ylabel("Inflation (%)")
ax.set_title("Source : BCM", fontsize=12)
ax.grid(alpha=0.3)
st.pyplot(fig)
plt.close()

# 6. Pie chart
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Poids des recettes fiscales - 2024</h2>
</div>
""", unsafe_allow_html=True)

val = df.loc[df["Année"] == 2024, "Recettes_fiscales_pct_PIB"].values[0]
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie([val, 100-val], labels=["Recettes fiscales", "Autres"], colors=[BLEU_MOYEN, BLEU_TRES_CLAIR],
       autopct="%1.1f%%", startangle=90, wedgeprops=dict(edgecolor="white"))
ax.set_title("Source : FMI (2023)", fontsize=12)
st.pyplot(fig)
plt.close()

# 7. Heatmap
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Corrélations entre indicateurs macroéconomiques (2007-2024)</h2>
</div>
""", unsafe_allow_html=True)

corr_vars = ["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct", "Recettes_fiscales_pct_PIB"]
corr = df[corr_vars].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.6, linecolor="white", cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title("Source : Calculs propres", fontsize=12)
st.pyplot(fig)
plt.close()

# 8. Stackplot
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 14H7v-2h10v2zm0-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Pression macroéconomique : inflation et chômage</h2>
</div>
""", unsafe_allow_html=True)

df_area = df.dropna(subset=["Inflation_pct", "Taux_chomage_pct"])
fig, ax = plt.subplots(figsize=(13, 4))
ax.stackplot(df_area["Année"], df_area["Inflation_pct"], df_area["Taux_chomage_pct"],
             labels=["Inflation", "Chômage"], colors=[BLEU_CLAIR, BLEU_MOYEN], alpha=0.85)
ax.set_title("Source : BCM, FMI", fontsize=12)
ax.set_ylabel("%")
ax.legend(loc="upper left")
st.pyplot(fig)
plt.close()

# 9. Boxplot
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 14H7v-2h10v2zm0-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Distribution de la croissance du PIB par période</h2>
</div>
""", unsafe_allow_html=True)

df_box = df.copy()
df_box["Période"] = pd.cut(df_box["Année"], bins=[1960, 1980, 2000, 2024], labels=["1960-1980", "1981-2000", "2001-2024"])
fig, ax = plt.subplots(figsize=(14, 5))
sns.boxplot(data=df_box, x="Période", y="Croissance_PIB_pct", palette=[BLEU_CLAIR, BLEU_MOYEN, BLEU_FONCE], ax=ax)
ax.set_title("Source : Banque Mondiale", fontsize=12)
ax.set_ylabel("%")
st.pyplot(fig)
plt.close()

# 10. Moyennes par décennie
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 14H7v-2h10v2zm0-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Indicateurs macroéconomiques - moyennes par décennie (depuis 2000)</h2>
</div>
""", unsafe_allow_html=True)

df_2000 = df[df["Année"] >= 2000].copy()
df_2000["Décennie"] = (df_2000["Année"] // 10) * 10
dec = df_2000.groupby("Décennie")[["Croissance_PIB_pct", "Inflation_pct", "Taux_chomage_pct"]].mean()
ax = dec.plot(kind="bar", figsize=(14, 5), color=[BLEU_FONCE, BLEU_MOYEN, BLEU_CLAIR])
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", label_type="edge", fontsize=12)
ax.set_title("Source : Calculs propres", fontsize=12)
ax.set_ylabel("Pourcentage (%)")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Indicateurs")
ax.grid(axis="y", alpha=0.25)
st.pyplot(ax.figure)
plt.close()

# 11. Volatilité
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 14H7v-2h10v2zm0-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Croissance du PIB - volatilité et incertitude</h2>
</div>
""", unsafe_allow_html=True)

roll = df["Croissance_PIB_pct"].rolling(10)
fig, ax = plt.subplots(figsize=(13, 4))
ax.plot(df["Année"], roll.mean(), color=BLEU_FONCE, linewidth=2.5, label="Moyenne mobile (10 ans)")
ax.fill_between(df["Année"], roll.mean() - roll.std(), roll.mean() + roll.std(),
                color=BLEU_CLAIR, alpha=0.6, label="± 1 écart-type")
ax.set_title("Source : Banque Mondiale", fontsize=12)
ax.set_ylabel("%")
ax.legend()
st.pyplot(fig)
plt.close()

# 12. Régimes macro
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 14H7v-2h10v2zm0-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Régimes macroéconomiques (Inflation vs Croissance)</h2>
</div>
""", unsafe_allow_html=True)

df_2000 = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Croissance_PIB_pct"])
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(df_2000["Inflation_pct"], df_2000["Croissance_PIB_pct"], c=df_2000["Année"], cmap="Blues", s=80, edgecolor="black", alpha=0.9)
plt.colorbar(ax.collections[0], ax=ax, label="Année")
ax.axhline(0, color="gray", linestyle="--")
ax.axvline(df_2000["Inflation_pct"].median(), linestyle="--", color="gray")
ax.set_title("Source : Calculs propres", fontsize=12)
ax.set_xlabel("Inflation (%)")
ax.set_ylabel("Croissance (%)")
st.pyplot(fig)
plt.close()

# 13. Trajectoire 3D
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Trajectoire macroéconomique 3D (depuis 2000)</h2>
</div>
""", unsafe_allow_html=True)

df_3d = df[df["Année"] >= 2000].dropna(subset=["Inflation_pct", "Taux_chomage_pct", "Croissance_PIB_pct"])
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
sc = ax.scatter(df_3d["Inflation_pct"], df_3d["Taux_chomage_pct"], df_3d["Croissance_PIB_pct"],
                c=df_3d["Année"], cmap="Blues", s=70, edgecolor="black", alpha=0.9)
ax.plot(df_3d["Inflation_pct"], df_3d["Taux_chomage_pct"], df_3d["Croissance_PIB_pct"], color=BLEU_FONCE, alpha=0.6)
ax.set_xlabel("Inflation (%)"); ax.set_ylabel("Chômage (%)"); ax.set_zlabel("Croissance (%)")
ax.set_title("Source : Calculs propres", fontsize=12)
fig.colorbar(sc, ax=ax, label="Année")
st.pyplot(fig)
plt.close()

# 14. Recettes fiscales 3D
st.markdown(f"""
<div class="section-header">
    <span class="section-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0B3C5D">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/>
        </svg>
    </span>
    <h2 style="margin:0;">Recettes fiscales - Vue 3D (2007-2024)</h2>
</div>
""", unsafe_allow_html=True)

df3d_bar = df[(df["Année"] >= 2007) & (df["Année"] <= 2024)].dropna(subset=["Recettes_fiscales_pct_PIB"])
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection="3d")
x = np.arange(len(df3d_bar)); y = np.zeros(len(x)); z = df3d_bar["Recettes_fiscales_pct_PIB"]
ax.bar3d(x, y, np.zeros_like(z), 0.6, 0.6, z, color=BLEU_MOYEN, alpha=0.9)
ax.set_xticks(x); ax.set_xticklabels(df3d_bar["Année"], rotation=45)
ax.set_zlabel("% du PIB")
ax.set_title("Source : FMI", fontsize=12)
st.pyplot(fig)
plt.close()

# -----------------------------
# Méthodologie
# -----------------------------
with st.expander("Méthodologie et sources de données"):
    st.markdown("""
    <div style="background: #f0f9ff; padding: 20px; border-radius: 12px; border-left: 4px solid #87CEEB;">
    <h4 style="color: #0c4a6e; margin-top: 0;">Sources officielles</h4>
    <ul>
        <li><b>Banque Centrale de Mauritanie (BCM)</b> - Données primaires sur recettes, chômage, taux d'intérêt (2007-2021)</li>
        <li><b>Fonds Monétaire International (FMI)</b> - Consultations Article IV (2022-2024)</li>
        <li><b>Banque Mondiale</b> - World Development Indicators (1960-2024)</li>
    </ul>
    
    <h4 style="color: #0c4a6e;">Traitement des données</h4>
    <ul>
        <li>Imputation par interpolation linéaire pour séries continues</li>
        <li>Remplacement par moyenne historique pour variables volatiles</li>
        <li>Fusion des doublons annuels (ex: 2022-2024)</li>
        <li>Validation croisée avec rapports officiels</li>
    </ul>
    </div>
    """)

st.caption("© 2026 - Projet académique | Jedou Mohamed Bebacar | Master SSD, Université de Nouakchott")

