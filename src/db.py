import os

import psycopg2
from dotenv import load_dotenv

load_dotenv() 


class DB:

    def __init__(self):
        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS shops(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) NOT NULL UNIQUE,
                image VARCHAR(256) NOT NULL DEFAULT ''
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories(
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) NOT NULL UNIQUE,
                image VARCHAR(256) NOT NULL DEFAULT ''
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id SERIAL PRIMARY KEY,
                name VARCHAR(128) NOT NULL UNIQUE,
                price NUMERIC(10,2) NOT NULL,
                image VARCHAR(256) NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                shop_id INT REFERENCES shops(id) ON DELETE CASCADE
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_category(
                product_id INT REFERENCES products(id) ON DELETE CASCADE,
                category_id INT REFERENCES categories(id) ON DELETE CASCADE,
                CONSTRAINT product_category_pk PRIMARY KEY (product_id, category_id)
            )
        """)

        self.conn.commit()

    def create_shop(self, name, image=''):
        self.cursor.execute("""
            INSERT INTO shops (name, image) VALUES (
                %s, %s
            ) RETURNING *
        """, (name, image))
        row = self.cursor.fetchone()
        self.conn.commit()
        return row

    def create_product(self, name, price, shop_id, image='', description=''):
        self.cursor.execute("""
            INSERT INTO products (name, price, shop_id, image, description) VALUES (
                %s, %s, %s, %s, %s
            ) RETURNING *
        """, (name, price, shop_id, image, description))
        row = self.cursor.fetchone()
        self.conn.commit()
        return row

    def get_product(self, pk):
        self.cursor.execute("""
            SELECT * FROM products
            INNER JOIN shops ON shops.id = products.shop_id
            WHERE products.id = %s
        """, (pk,))
        row = self.cursor.fetchone()
        self.conn.commit()
        return row

    def get_products(self):
        self.cursor.execute("""
            SELECT *
            FROM products INNER JOIN shops ON shops.id = products.shop_id
        """)
        rows = self.cursor.fetchall()
        self.conn.commit()
        return rows


db = DB()
