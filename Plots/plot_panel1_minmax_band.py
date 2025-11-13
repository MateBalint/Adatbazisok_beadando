import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_MINMAX = "out/daily_minmax.csv"
CSV_AVG    = "out/daily_avg.csv"
OUT        = "out/panel1_minmax_band.png"
PANEL_NAME = "Panel hőfok 1"

os.makedirs("out", exist_ok=True)

df_minmax = pd.read_csv(CSV_MINMAX)
df_avg    = pd.read_csv(CSV_AVG)

m1 = df_minmax[df_minmax["name"] == PANEL_NAME].sort_values("day")
a1 = df_avg[df_avg["name"] == PANEL_NAME].sort_values("day")

plt.figure(figsize=(9,4))
plt.fill_between(m1["day"], m1["min_value"], m1["max_value"], alpha=0.25, label="Min–Max sáv")
plt.plot(a1["day"], a1["avg"], marker="o", linewidth=1.2, label="Napi átlag")
plt.title(f"{PANEL_NAME} – napi min/átlag/max")
plt.xlabel("Dátum")
plt.ylabel("Hőmérséklet (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUT, dpi=200)
plt.close()
print(f"[DONE] {OUT}")
