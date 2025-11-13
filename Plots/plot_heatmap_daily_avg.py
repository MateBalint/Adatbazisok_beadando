import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

CSV = "out/daily_avg.csv"
OUT = "out/heatmap_daily_avg.png"

os.makedirs("out", exist_ok=True)
df = pd.read_csv(CSV)

pivot = df.pivot(index="name", columns="day", values="avg")
# rendezés: panel név szerinti
pivot = pivot.sort_index()

plt.figure(figsize=(12,4.5))
im = plt.imshow(pivot.values, aspect="auto")
plt.title("Napi átlaghőmérséklet – hőtérkép")
plt.xlabel("Dátum")
plt.ylabel("Panel")
plt.yticks(ticks=range(len(pivot.index)), labels=pivot.index, fontsize=8)
plt.xticks(ticks=range(len(pivot.columns)), labels=pivot.columns, rotation=45, fontsize=7)
plt.colorbar(im, label="Átlag (°C)")
plt.tight_layout()
plt.savefig(OUT, dpi=220)
plt.close()
print(f"[DONE] {OUT}")
