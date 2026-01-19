import matplotlib.pyplot as plt
import numpy as np

BLEU_FONCE = "#0B3C5D"
BLEU_MOYEN = "#1F77B4"
BLEU_CLAIR = "#AEC7E8"

plt.figure(figsize=(14, 4))
plt.plot(df["Année"], df["Croissance_PIB_pct"], color=BLEU_FONCE, linewidth=2, label="Croissance")
plt.plot(df["Année"], df["Croissance_PIB_pct"].rolling(10).mean(), color=BLEU_MOYEN, linewidth=3, label="Tendance long terme")
plt.fill_between(df["Année"], df["Croissance_PIB_pct"], where=df["Croissance_PIB_pct"] < 0, color=BLEU_CLAIR, alpha=0.6)
for year, label in zip([1975, 2009, 2020], ["Choc pétrolier", "Crise financière", "COVID-19"]):
    if year in df["Année"].values:
        y = df.loc[df["Année"] == year, "Croissance_PIB_pct"].values[0]
        plt.annotate(label, xy=(year, y), xytext=(year, y-6),
                     arrowprops=dict(arrowstyle="->", color=BLEU_FONCE), ha="center", fontsize=9)
plt.axhline(0, linestyle="--", color="gray")
plt.title("Croissance du PIB – cycles économiques et chocs\nSource : BCM, FMI, Banque Mondiale", weight="bold")
plt.ylabel("%")
plt.legend()
plt.grid(axis="y", alpha=0.3)
st.pyplot(plt)
plt.close()
