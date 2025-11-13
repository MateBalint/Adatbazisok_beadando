import sqlite3
import pandas as pd
from datetime import datetime
import re

class FormatUtils:
    # Mojibake-barát aliasok az Adagok.csv-hez
    C_ID    = ["Adagszám","ADAGSZÁM","ADAGSZAM","ADAGSZµM","ADAGSZ\u00C1M"]
    C_SD    = ["Kezdet_DÁTUM","Kezdet_DATUM","Kezdet_D\u00C1TUM","Kezdet_DµTUM"]
    C_ST    = ["Kezdet_IDŐ","Kezdet_IDO","Kezdet_ID\u0150","Kezdet_IDŠ"]
    C_ED    = ["Vége_DÁTUM","Vege_DATUM","V\u00E9ge_D\u00C1TUM","V‚ge_DµTUM"]
    C_ET    = ["Vége_IDŐ","Vege_IDO","V\u00E9ge_ID\u0150","V‚ge_IDŠ"]
    C_INTRA = ["ADAGKÖZI IDŐ","ADAGKOZI IDO","ADAGK\u00D6ZI ID\u0150","ADAGK\u2122ZI ID\u0160"]
    C_DUR   = ["ADAGIDŐ","ADAGIDO","ADAGID\u0150","ADAGIDŠ"]
    
    # Bővített kulcsszavak a Hűtőpanelek.csv oszlopainak felismeréséhez
    TIME_KEYS  = ["time", "idő", "ido", "timestamp"]
    VALUE_KEYS = ["valuey", "value", "érték", "ertek", "yvalue", "y-value"]

    def to_iso(date_str, time_str):
        """Dátum + idő -> ISO (YYYY-MM-DDTHH:MM:SS)"""
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y.%m.%d %H:%M:%S")
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception:
            return None
    
    def parse_ts_any(s: str):
        s = str(s).strip()
        fmts = [
            "%Y.%m.%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d.%m.%Y %H:%M:%S",
            "%Y.%m.%dT%H:%M:%S",
        ]
        for f in fmts:
            try:
                return datetime.strptime(s, f).strftime("%Y-%m-%dT%H:%M:%S")
            except Exception:
                pass
        return None
    
    def to_int_or_none(x):
        if pd.isna(x): return None
        try:
            return int(x)
        except Exception:
            s = str(x).replace(",", ".")
            try:
                return int(float(s))
            except Exception:
                return None
    
    def to_float_or_none(x):
        if pd.isna(x): return None
        try:
            return float(str(x).replace(",", ".").strip())
        except Exception:
            return None
    
    def run_sql(conn, sql, rows=None):
        cur = conn.cursor()
        if rows is None:
            cur.execute(sql)
        elif len(rows) > 0:
            cur.executemany(sql, rows)
        conn.commit()
    
    def pick(cols, candidates):
        for c in candidates:
            if c in cols:
                return c
        return None
    
    
    def main():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        print("[OK] Kapcsolódva az adatbázishoz.")
    
        # 1) Panelek seed + default min/max ha nincs beállítva
        panels = [(i, f"Panel hőfok {i}", "°C") for i in range(1, 16)]
        run_sql(conn, "INSERT OR IGNORE INTO panel(id,name,unit) VALUES (?,?,?)", panels)
        run_sql(conn, "UPDATE panel SET min_valid=-60 WHERE min_valid IS NULL;")
        run_sql(conn, "UPDATE panel SET max_valid=200 WHERE max_valid IS NULL;")
        print(f"[OK] {len(panels)} panel feltöltve (min/max beállítva, ha hiányzott).")
    
        # 2) Adagok (batch)
        df_adag = pd.read_csv(ADAGOK_PATH, sep=";", encoding="cp1250")
        cols = df_adag.columns
        col_id    = pick(cols, C_ID)
        col_sd    = pick(cols, C_SD)
        col_st    = pick(cols, C_ST)
        col_ed    = pick(cols, C_ED)
        col_et    = pick(cols, C_ET)
        col_intra = pick(cols, C_INTRA)
        col_dur   = pick(cols, C_DUR)
    
        if not all([col_id, col_sd, col_st, col_ed, col_et]):
            print("[HIBA] Az Adagok.csv kötelező oszlopait nem találtam!")
            print("Meglevő fejlécek:", list(cols))
            conn.close()
            return
    
        batch_rows = []
        for _, r in df_adag.iterrows():
            adagszam = to_int_or_none(r[col_id])
            start_ts = to_iso(r[col_sd], r[col_st])
            end_ts   = to_iso(r[col_ed], r[col_et])
            dur      = to_int_or_none(r[col_dur]) if col_dur else None
            intra    = to_int_or_none(r[col_intra]) if col_intra else None
            if adagszam is None or not start_ts or not end_ts:
                continue
            batch_rows.append((adagszam, start_ts, end_ts, dur, intra))
    
        print(f"[INFO] Adagok parsed sorok: {len(batch_rows)}")
        run_sql(conn,
                "INSERT OR REPLACE INTO batch(id,start_ts,end_ts,duration_s,intra_duration_s) VALUES (?,?,?,?,?)",
                batch_rows
                )
        print(f"[OK] {len(batch_rows)} adag feltöltve.")
    
        # 3) Hűtőpanelek (measurement) — autodetekt + panel min/max szűrés
        df = pd.read_csv(PANELEK_PATH, sep=";", encoding="utf-8-sig")
    
        # Gyűjtsük a (panel_id, time_col, value_col) párokat
        def is_time_col(colname: str) -> bool:
            low = str(colname).lower()
            return any(k in low for k in TIME_KEYS)
    
        def is_value_col_for_pid(colname: str, pid: int) -> bool:
            text = str(colname)
            low  = text.lower()
            return (str(pid) in text) and any(k in low for k in VALUE_KEYS) and not is_time_col(text)
    
        time_cols = [c for c in df.columns if is_time_col(c)]
    
        pairs = []
        def extract_panel_id(text):
            m = re.search(r'(\d+)', str(text))
            return int(m.group(1)) if m else None
    
        for tcol in time_cols:
            pid = extract_panel_id(tcol)
            if pid is None:
                continue
            candidates = [c for c in df.columns if is_value_col_for_pid(c, pid)]
            if candidates:
                vcol = candidates[0]
                pairs.append((pid, tcol, vcol))
    
        if DEBUG:
            print("[DEBUG] Felismert (panel_id, time_col, value_col) párok:")
            for pid, tcol, vcol in sorted(pairs):
                n = df[[tcol, vcol]].dropna().shape[0]
                print(f"  panel {pid:2d}: time='{tcol}'  value='{vcol}'  (nem üres sorok: {n})")
            present = {pid for pid, *_ in pairs}
            missing = [pid for pid in range(1, 16) if pid not in present]
            if missing:
                print("[FIGYELEM] Nem találtam oszloppárt ezekhez a panelekhez:", missing)
    
        if not pairs:
            print("[HIBA] Nem találtam Time/Value párokat a Hűtőpanelek (Hutopanelek).csv-ben!")
            print("Meglevő fejlécek (mintaként az első 10):", list(df.columns)[:10])
            conn.close()
            return
    
        # Panel min/max beolvasása a DB-ből
        panel_limits = {row[0]: (row[1], row[2])
                        for row in conn.execute("SELECT id, min_valid, max_valid FROM panel").fetchall()}
    
        meas_rows = []
        skipped_out_of_range = 0
        for pid, tcol, vcol in pairs:
            minv, maxv = panel_limits.get(pid, (None, None))
            for t, v in zip(df[tcol], df[vcol]):
                if pd.isna(t) or pd.isna(v):
                    continue
                ts = parse_ts_any(t)
                val = to_float_or_none(v)
                if ts is None or val is None:
                    continue
                # panel-specifikus tartomány szűrés, hogy a trigger ne dobjon hibát
                if (minv is not None and val < minv) or (maxv is not None and val > maxv):
                    skipped_out_of_range += 1
                    continue
                meas_rows.append((pid, ts, val))
    
        run_sql(conn, "INSERT OR IGNORE INTO measurement(panel_id,ts_utc,value) VALUES (?,?,?)", meas_rows)
        print(f"[OK] {len(meas_rows)} mérés feltöltve. (kihagyva tartományon kívül: {skipped_out_of_range})")
    
        # 4) Ellenőrzés
        c1 = conn.execute("SELECT COUNT(*) FROM batch;").fetchone()[0]
        c2 = conn.execute("SELECT COUNT(*) FROM measurement;").fetchone()[0]
        print(f"[INFO] Összes adag: {c1}, összes mérés: {c2}")
    
        # --- Biztonsági mentés a betöltés után ---
        import shutil, os
        from datetime import datetime
        os.makedirs("backup", exist_ok=True)
        backup_path = f"backup/project_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy(DB_PATH, backup_path)
        print(f"[INFO] Biztonsági mentés készült: {backup_path}")
    
        conn.close()
        print("[DONE] Betöltés befejezve.")