import os
import sqlite3

DB_PATH = "project.db"
OUT_DIR = "out"

REPORTS = {
    # 1) Utolsó érték panelenként
    "last_values.csv": """
        SELECT p.id, p.name, m.ts_utc, m.value
        FROM panel p
        JOIN measurement m ON m.panel_id=p.id
        WHERE m.ts_utc=(SELECT MAX(ts_utc) FROM measurement WHERE panel_id=p.id)
        ORDER BY p.id;
    """,

    # 2) Napi átlag panelenként
    "daily_avg.csv": """
        SELECT p.name, DATE(m.ts_utc) AS day, AVG(m.value) AS avg
        FROM measurement m
        JOIN panel p ON p.id=m.panel_id
        WHERE m.quality_code='OK'
        GROUP BY p.name, DATE(m.ts_utc)
        ORDER BY day, p.name;
    """,

    # 3) Batch-átlag panelenként
    "batch_avg.csv": """
        SELECT b.id AS batch_id, p.name, AVG(m.value) AS avg
        FROM v_measurement_in_batch m
        JOIN panel p ON p.id=m.panel_id
        JOIN batch b ON b.id=m.batch_id
        WHERE m.quality_code='OK'
        GROUP BY b.id, p.name
        ORDER BY b.id, p.name;
    """,

    # 4) Outlierek 3σ szabállyal
    "outliers.csv": """
        WITH stats AS (
          SELECT
            panel_id,
            COUNT(*) AS n,
            AVG(value) AS av,
            (SUM(value*value) - (SUM(value)*SUM(value))/COUNT(*)) / COUNT(*) AS var
          FROM measurement
          WHERE quality_code='OK'
          GROUP BY panel_id
        )
        SELECT m.panel_id, m.ts_utc, m.value
        FROM measurement m
        JOIN stats s USING(panel_id)
        WHERE m.quality_code='OK'
          AND s.var IS NOT NULL
          AND ABS(m.value - s.av) > 3*sqrt(s.var)
        LIMIT 100;
    """,

    # 5) ÚJ: napi minimum–maximum panelenként  ✅
    "daily_minmax.csv": """
        SELECT 
            p.name,
            substr(m.ts_utc, 1, 10) AS day,
            MIN(m.value) AS min_value,
            MAX(m.value) AS max_value
        FROM measurement m
        JOIN panel p ON p.id = m.panel_id
        WHERE m.quality_code='OK'
        GROUP BY p.name, day
        ORDER BY day, p.name;
    """
}

def save_query(conn, out_path: str, sql: str) -> int:
    cur = conn.cursor()
    rows = cur.execute(sql).fetchall()
    cols = [d[0] for d in cur.description]

    # biztos, ami biztos: kimeneti mappa
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # egyszerű CSV fejléc + sorok; értékeket str() konvertáljuk
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join("" if x is None else str(x) for x in r) + "\n")
    return len(rows)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    for filename, sql in REPORTS.items():
        print(f"[INFO] Generálás: {filename} ...")
        out_path = os.path.join(OUT_DIR, filename)
        n = save_query(conn, out_path, sql)
        print(f"   → {n} sor elmentve: {out_path}")

    conn.close()
    print("\n[DONE] Minden riport sikeresen elkészült az 'out/' mappába.")

if __name__ == "__main__":
    main()
