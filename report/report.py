import os
import sqlite3

from constants.file_paths import DB_PATH, OUTPUT_FOLDER_PATH
from constants.sql_queries import REPORTS

class ReportGenerator:
    def save_query(self, out_path: str, sql: str) -> int:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            rows = cur.execute(sql).fetchall()
            cols = [d[0] for d in cur.description]
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(",".join(cols) + "\n")
                for r in rows:
                    f.write(",".join("" if x is None else str(x) for x in r) + "\n")
            return len(rows)
    
    def generate_reports(self):
        for filename, sql in REPORTS.items():
            print(f"[INFO] Generálás: {filename} ...")
            out_path = os.path.join(OUTPUT_FOLDER_PATH, filename)
            n = self.save_query(out_path, sql)
            print(f"   → {n} sor elmentve: {out_path}")
        print("\n[DONE] Minden riport sikeresen elkészült az 'output' mappába.")