import sqlite3
import os

class DeliveryDatabase:
    def __init__(self, db_name="delivery.db"):
        # Файл лежит в db/, значит корень проекта — это родительская папка
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Папка, где лежит этот скрипт (то есть папка db)
        db_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Полный путь к файлу БД внутри папки db
        self.db_path = os.path.join(db_dir, db_name)
        
        # Подключаемся к файлу БД
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS deliveries (
                weight REAL,
                distance INTEGER,
                package_type TEXT,
                is_express INTEGER,
                cost INTEGER,
                delivery_date TEXT,
                error_message TEXT,
                PRIMARY KEY (weight, distance, package_type, is_express)
            )
        ''')
        self.conn.commit()

    def add_record(self, weight, distance, package_type, is_express, cost, delivery_date, error_message=""):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO deliveries 
                (weight, distance, package_type, is_express, cost, delivery_date, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (weight, distance, package_type, int(is_express), cost, delivery_date, error_message))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка БД при добавлении: {e}")

    def get_record(self, weight, distance, package_type, is_express):
        self.cursor.execute('''
            SELECT cost, delivery_date, error_message FROM deliveries
            WHERE weight = ? AND distance = ? AND package_type = ? AND is_express = ?
        ''', (weight, distance, package_type, int(is_express)))
        return self.cursor.fetchone()

    def delete_record(self, weight, distance, package_type, is_express):
        self.cursor.execute('''
            DELETE FROM deliveries
            WHERE weight = ? AND distance = ? AND package_type = ? AND is_express = ?
        ''', (weight, distance, package_type, int(is_express)))
        self.conn.commit()

    def close(self):
        self.conn.close()