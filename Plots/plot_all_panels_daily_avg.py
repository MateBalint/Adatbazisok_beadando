import pandas as pd
import matplotlib.pyplot as plt
import os

CSV = "out/daily_avg.csv"
OUT = "out/all_panels_daily_avg.png"

os.makedirs("out", exist_ok=True)
df = pd.read_csv(CSV)

plt.figure(figsize=(10,5))
for name, g in df.groupby("name"):
    plt.plot(g["day"], g["avg"], label=name, linewidth=1)

plt.title("Összes panel – napi átlaghőmérséklet")
plt.xlabel("Dátum")
plt.ylabel("Átlag (°C)")
plt.xticks(rotation=45)
plt.legend(ncol=3, fontsize=8)
plt.tight_layout()
plt.savefig(OUT, dpi=200)
plt.close()
print(f"[DONE] {OUT}")
