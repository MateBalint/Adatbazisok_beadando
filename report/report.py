import os
import sqlite3

class ReportGenerator:
    DB_PATH = "project.db"
    OUT_DIR = "../output"

    REPORTS = {
        "last_values.csv": """
                           SELECT p.id, p.name, m.ts_utc, m.value
                           FROM panel p
                                    JOIN measurement m ON m.panel_id = p.id
                           WHERE m.ts_utc = (SELECT MAX(ts_utc) FROM measurement WHERE panel_id = p.id)
                           ORDER BY p.id;
                           """,
        "daily_avg.csv": """
                         SELECT p.name, DATE (m.ts_utc) AS day, AVG (m.value) AS avg
                         FROM measurement m
                             JOIN panel p
                         ON p.id=m.panel_id
                         WHERE m.quality_code='OK'
                         GROUP BY p.name, DATE (m.ts_utc)
                         ORDER BY day, p.name;
                         """,
        "batch_avg.csv": """
                         SELECT b.id AS batch_id, p.name, AVG(m.value) AS avg
                         FROM v_measurement_in_batch m
                             JOIN panel p
                         ON p.id=m.panel_id
                             JOIN batch b ON b.id=m.batch_id
                         WHERE m.quality_code='OK'
                         GROUP BY b.id, p.name
                         ORDER BY b.id, p.name;
                         """,
        "outliers.csv": """
                        WITH stats AS (SELECT panel_id,
                                              COUNT(*)                                                               AS n,
                                              AVG(value)                                                             AS av,
                                              (SUM(value * value) - (SUM(value) * SUM(value)) / COUNT(*)) /
                                              COUNT(*)                                                               AS var
                                       FROM measurement
                                       WHERE quality_code = 'OK'
                                       GROUP BY panel_id)
                        SELECT m.panel_id, m.ts_utc, m.value
                        FROM measurement m
                                 JOIN stats s USING (panel_id)
                        WHERE m.quality_code = 'OK'
                          AND s.var IS NOT NULL
                          AND ABS(m.value - s.av) > 3 * sqrt(s.var) LIMIT 100;
                        """,
        "daily_minmax.csv": """
                            SELECT p.name,
                                   substr(m.ts_utc, 1, 10) AS day,
                MIN(m.value) AS min_value,
                MAX(m.value) AS max_value
                            FROM measurement m
                                JOIN panel p
                            ON p.id = m.panel_id
                            WHERE m.quality_code='OK'
                            GROUP BY p.name, day
                            ORDER BY day, p.name;
                            """
    }

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        os.makedirs(self.OUT_DIR, exist_ok=True)

    def save_query(self, out_path: str, sql: str) -> int:
        cur = self.conn.cursor()
        rows = cur.execute(sql).fetchall()
        cols = [d[0] for d in cur.description]
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(",".join(cols) + "\n")
            for r in rows:
                f.write(",".join("" if x is None else str(x) for x in r) + "\n")
        return len(rows)

    def generate_reports(self):
        for filename, sql in self.REPORTS.items():
            print(f"[INFO] Generálás: {filename} ...")
            out_path = os.path.join(self.OUT_DIR, filename)
            n = self.save_query(out_path, sql)
            print(f"   → {n} sor elmentve: {out_path}")
        self.conn.close()
        print("\n[DONE] Minden riport sikeresen elkészült az 'out/' mappába.")