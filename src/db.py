import os
import sqlite3


class DB:

    def __init__(self, db_name):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               db_name)
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(128) NOT NULL UNIQUE,
                price DOUBLE PRECISION NOT NULL,
                image TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def create_product(self, name, price, image, description=''):
        self.cursor.execute("""
            INSERT INTO products (name, price, image, description) VALUES (
                ?, ?, ?, ?
            )
        """, (name, price, image, description))
        self.connection.commit()

    def get_product(self, pk=None):
        if pk is None:
            raise ValueError('pk is required')

        rows = self.cursor.execute("""
            SELECT id, name, price, image, description FROM products
            WHERE id = ?
        """, (pk,)).fetchall()
        self.connection.commit()

        return rows[0]

    def get_products(self):
        rows = self.cursor.execute("""
            SELECT id, name, price, image, description FROM products
        """).fetchall()
        self.connection.commit()

        return rows


db = DB("shop.db")
