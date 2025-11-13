import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Beállítások ---
CSV_PATH = "out/daily_avg.csv"
OUT_IMG = "out/panel1_daily_avg.png"

# --- Ellenőrzés ---
if not os.path.exists(CSV_PATH):
    print(f"[HIBA] A fájl nem található: {CSV_PATH}")
    print("Futtasd előbb a report.py-t!")
    exit(1)

# --- Adatok beolvasása ---
df = pd.read_csv(CSV_PATH)

# Csak a 'Panel hőfok 1' adatait tartjuk meg
df_panel = df[df["name"] == "Panel hőfok 1"]

if df_panel.empty:
    print("[HIBA] Nincs adat a 'Panel hőfok 1'-hez!")
    exit(1)

# --- Grafikon létrehozása ---
plt.figure(figsize=(8,4))
plt.plot(df_panel["day"], df_panel["avg"], marker='o', linestyle='-', linewidth=1.5)
plt.title("Panel 1 napi átlaghőmérséklet")
plt.xlabel("Dátum")
plt.ylabel("Átlaghőmérséklet (°C)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()

# --- Mentés ---
plt.savefig(OUT_IMG, dpi=200)
plt.close()

print(f"[DONE] Grafikon mentve ide: {OUT_IMG}")
