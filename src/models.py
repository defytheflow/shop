from dataclasses import dataclass

from db import db


@dataclass
class Shop:
    id: int
    name: str
    slug: str
    image: str

    @classmethod
    def create(cls, name, slug, image=''):
        db.cursor.execute("""
            INSERT INTO shops (name, slug, image) VALUES (
                %s, %s, %s
            ) RETURNING *
        """, (name, slug, image))
        row = db.cursor.fetchone()
        db.conn.commit()
        return cls(*row)

    @classmethod
    def get(cls, pk=None, slug=None):
        if pk is not None:
            db.cursor.execute("""
                SELECT * FROM shops WHERE shops.id = %s
            """, (pk,))
        elif slug is not None:
            db.cursor.execute("""
                SELECT * FROM shops WHERE shops.slug = %s
            """, (slug,))
        else:
            raise ValueError('Either pk or slug is required.')

        row = db.cursor.fetchone()
        db.conn.commit()

        return None if row is None else cls(*row)

    @classmethod
    def all(cls):
        db.cursor.execute("""
            SELECT * FROM shops
        """)
        rows = db.cursor.fetchall()
        db.conn.commit()
        shops = [cls(*row) for row in rows]
        return shops

    @property
    def products(self):
        db.cursor.execute("""
            SELECT * FROM products
            INNER JOIN shops ON shops.id = products.shop_id
            WHERE shop_id = %s
        """, (self.id, ))
        rows = db.cursor.fetchall()
        db.conn.commit()
        products = [Product(*row[:5], self.__class__(*row[6:])) for row
                    in rows]
        return products

    @property
    def reviews(self):
        db.cursor.execute("""
            SELECT * FROM shop_reviews
            WHERE shop_id = %s
        """, (self.id, ))
        rows = db.cursor.fetchall()
        db.conn.commit()
        reviews = [ShopReview(*row[:-1], self) for row in rows]
        return reviews

    def get_absolute_url(self):
        return f'/shops/{self.slug}'


@dataclass
class ShopReview:
    id: int
    username: str
    text: str
    shop: Shop

    @classmethod
    def create(cls, username, text, shop_id):
        db.cursor.execute("""
            INSERT INTO shop_reviews (
                username, text, shop_id) VALUES (
                %s, %s, %s
            ) RETURNING *
        """, (username, text, shop_id))
        row = db.cursor.fetchone()
        db.conn.commit()
        return cls(*row)


@dataclass
class Category:
    id: int
    name: str
    image: str


@dataclass
class Product:
    id: int
    name: str
    price: float
    image: str
    description: str
    shop: Shop

    @classmethod
    def create(cls, name, price, shop_id, image='', description=''):
        db.cursor.execute("""
            INSERT INTO products (
                name, price, shop_id, image, description) VALUES (
                %s, %s, %s, %s, %s
            ) RETURNING *
        """, (name, price, shop_id, image, description))
        row = db.cursor.fetchone()
        db.conn.commit()
        return cls(*row)

    @classmethod
    def get(cls, pk):
        db.cursor.execute("""
            SELECT * FROM products
            INNER JOIN shops ON shops.id = products.shop_id
            WHERE products.id = %s
        """, (pk,))
        row = db.cursor.fetchone()
        db.conn.commit()
        return None if row is None else cls(*row[:5], Shop(*row[6:]))

    @classmethod
    def all(cls):
        db.cursor.execute("""
            SELECT * FROM products
            INNER JOIN shops ON shops.id = products.shop_id
        """)
        rows = db.cursor.fetchall()
        db.conn.commit()
        products = [cls(*row[:5], Shop(*row[6:])) for row in rows]
        return products

    def get_absolute_url(self):
        return f'/products/{self.id}'
