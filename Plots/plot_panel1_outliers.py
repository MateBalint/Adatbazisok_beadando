import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

DB = "project.db"
OUT = "out/panel1_outliers.png"
PANEL_ID = 1  # változtatható

os.makedirs("out", exist_ok=True)

conn = sqlite3.connect(DB)

# kis minta-idősor az adott panelhez (OK minőség)
rows = conn.execute("""
SELECT ts_utc, value
FROM measurement
WHERE panel_id=? AND quality_code='OK'
ORDER BY ts_utc
LIMIT 2000;
""", (PANEL_ID,)).fetchall()
conn.close()

if not rows:
    print("[INFO] Nincs adat a kiválasztott panelhez.")
    raise SystemExit

ts = [r[0] for r in rows]
val = [float(r[1]) for r in rows]

# alapsor
plt.figure(figsize=(10,4))
plt.plot(ts, val, linewidth=1.0, label="Értékek")

# outlierek (első 100 a reportból) – piros pont
try:
    out = pd.read_csv("out/outliers.csv")
    out_p = out[out["panel_id"] == PANEL_ID].head(100)
    if not out_p.empty:
        plt.scatter(out_p["ts_utc"], out_p["value"], s=18, marker="o", label="Outlier (TOP100)", zorder=5)
except Exception as e:
    pass

plt.title(f"Panel {PANEL_ID} – mintavétel + outlierek (TOP100)")
plt.xlabel("Idő")
plt.ylabel("Érték (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUT, dpi=200)
plt.close()
print(f"[DONE] {OUT}")
