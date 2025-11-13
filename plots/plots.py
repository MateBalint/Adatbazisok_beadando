import pandas as pd
import matplotlib.pyplot as plt
import os
import sqlite3


class PlotBuilder:
    
    def build_all_daily_average_panel(self):
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
        
    def build_heatmap_daily_average_panel(self):
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
        
    def build_panel_1(self):
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

    def build_panel_1_minmax_band(self):
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
        
        def build_panel1_outliers():
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