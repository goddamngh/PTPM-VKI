import sqlite3
import os

class TriangleDatabase:
    def __init__(self, db_name="triangle.db"):
        if db_name == ":memory:" or os.path.isabs(db_name):
            self.db_path = db_name
        else:
            db_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(db_dir, db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS triangles (
                side_a REAL,
                side_b REAL,
                side_c REAL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        ''')
        self.conn.commit()

    def add_record(self, side_a, side_b, side_c, triangle_type, error_message=""):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO triangles 
                (side_a, side_b, side_c, triangle_type, error_message)
                VALUES (?, ?, ?, ?, ?)
            ''', (side_a, side_b, side_c, triangle_type, error_message))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка БД при добавлении: {e}")

    def get_record(self, side_a, side_b, side_c):
        self.cursor.execute('''
            SELECT triangle_type, error_message FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        ''', (side_a, side_b, side_c))
        return self.cursor.fetchone()

    def delete_record(self, side_a, side_b, side_c):
        self.cursor.execute('''
            DELETE FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        ''', (side_a, side_b, side_c))
        self.conn.commit()

    def close(self):
        self.conn.close()