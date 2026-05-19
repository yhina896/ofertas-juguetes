from scrapers.plaza_vea import scrape_plaza_vea
from scrapers.metro import scrape_metro
from scrapers.falabella import scrape_falabella

from notificaciones.telegram_bot import send_telegram
from notificaciones.email import send_email
from database.db import init_db, save_product

import re


def clean_price(price_text):
    try:
        if not price_text:
            return None

        number = re.sub(r'[^0-9.]', '', str(price_text))

        if number == "":
            return None

        return float(number)

    except:
        return None


def process_store(products, store_name):

    print(f"\n🏬 Procesando {store_name} => {len(products)} productos")

    for product in products:

        current_price = clean_price(product.get('price', ''))
        old_price = clean_price(product.get('old_price', ''))

        if current_price is None or old_price is None:
            continue

        if old_price <= 0:
            continue

        discount = ((old_price - current_price) / old_price) * 100

        print(f"🟢 {product.get('title')} => {discount:.2f}%")

        if discount <= 10 or discount > 95:
            continue

        # IMPORTANTE: agregar tienda al producto
        product["store"] = store_name

        # -------------------------
        # SIEMPRE ENVIAR TELEGRAM
        # -------------------------
        msg = f"""
🔥 OFERTA JUGUETES - {store_name}

🧸 {product.get('title')}

💲 Precio: {product.get('price')}

🏷️ Antes: {product.get('old_price')}

🎯 Descuento: {discount:.2f}%

🔗 {product.get('link')}
"""

        print("📲 ENVIANDO TELEGRAM...")
        send_telegram(msg)

        print("📧 ENVIANDO EMAIL...")
        send_email(product, discount, store_name)

        # -------------------------
        # SOLO GUARDAR SI ES NUEVO
        # -------------------------
        is_new = save_product(product)

        if is_new:
            print("🆕 Producto nuevo guardado")
        else:
            print("🔁 Producto ya existía")


# -------------------------
# MAIN
# -------------------------

init_db()

process_store(scrape_plaza_vea(), "Plaza Vea")
process_store(scrape_metro(), "Metro")
process_store(scrape_falabella(), "Falabella")