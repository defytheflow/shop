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
                slug VARCHAR(64) NOT NULL UNIQUE,
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

db = DB()
