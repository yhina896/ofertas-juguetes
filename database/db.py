import sqlite3


def init_db():

    conn = sqlite3.connect("ofertas.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        price TEXT,

        old_price TEXT,

        link TEXT UNIQUE,

        store TEXT
    )
    """)

    conn.commit()

    conn.close()


def save_product(product):

    conn = sqlite3.connect("ofertas.db")

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO products (

            title,
            price,
            old_price,
            link,
            store

        )
        VALUES (?, ?, ?, ?, ?)
        """, (

            product.get('title'),
            product.get('price'),
            product.get('old_price'),
            product.get('link'),
            'Plaza Vea'
        ))

        conn.commit()

        print("✅ Guardado en SQLite")

        saved = True

    except sqlite3.IntegrityError:

        print("⚠️ Producto repetido")

        saved = False

    conn.close()

    return saved

