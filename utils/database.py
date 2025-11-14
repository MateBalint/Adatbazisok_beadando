import sqlite3

from constants.file_paths import DB_PATH, SQL_SCHEMA
from utils.loader import DataLoader

class Database:
    def run_sql_schema_script(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            with open(SQL_SCHEMA, encoding="utf-8") as f:
                sql_script = f.read()

            cursor.executescript(sql_script)
            conn.commit()

        data_loader = DataLoader()
        data_loader.load()