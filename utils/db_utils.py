import sqlite3
import pandas as pd

class DatabaseUtils:
    DB_PATH = ""
    SQL_SCRIPT_PATH = ""
    ADAGOK_PATH = ""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def setup_database(self):
        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            
            with open(self.SQL_SCRIPT_PATH, "r", encoding="utf-8") as f:
                sql = f.read()
                
            cursor.executescript(sql)
            conn.commit()
    
    def seed_data(self, chunks, table_name):
        """
        Seeds the given data to the given table.
        :param chunks: data to seed.
        :param table_name: Name of the table to seed that data to.
        """
        connection = sqlite3.connect(self.file_path)
    
        try:
            for i, chunk in enumerate(chunks):
                if_exists = 'replace' if i == 0 else 'append'
                chunk.to_sql(table_name, connection, if_exists=if_exists, index=False)
    
            connection.commit()
    
        except Exception as e:
            print(f"Error seeding database: {e}")
    
        finally:
            connection.close()
    
    
    def execute_query(self, query: str):
        """
        This method runs the given sql query.
        :param query: Query to run.
        :return: The data if the query ran successfully, None otherwise.
        """
        connection = sqlite3.connect(self.file_path)
    
        try:
            result = pd.read_sql_query(query, connection)
    
            return result
    
        except Exception as e:
            print(f"Error happened during query execution: {e}")
            return None
    
        finally:
            connection.close()