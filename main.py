from scrapers.plaza_vea import scrape_plaza_vea

from notificaciones.telegram_bot import send_telegram

from database.db import (
    init_db,
    save_product
)

import re


def clean_price(price_text):

    try:

        number = re.sub(
            r'[^0-9.]',
            '',
            price_text
        )

        return float(number)

    except:

        return None


# crear DB
init_db()

# scrapear productos
products = scrape_plaza_vea()

print(f"✅ TOTAL PRODUCTOS: {len(products)}")

for product in products:

    current_price = clean_price(
        product.get('price', '')
    )

    old_price = clean_price(
        product.get('old_price', '')
    )

    # validar precios
    if not current_price or not old_price:

        print("⚠️ Producto sin precios válidos")
        continue

    # evitar división inválida
    if old_price <= 0:
        continue

    # calcular descuento
    discount = (
        (old_price - current_price)
        / old_price
    ) * 100

    print(
        f"🟢 {product.get('title')} "
        f"=> {discount:.2f}%"
    )

    # mínimo 20%
    if discount <= 20:

        print("❌ Menor a 15%")
        continue

    # evitar descuentos absurdos
    if discount > 95:

        print("❌ Descuento inválido")
        continue

    # guardar producto
    saved = save_product(product)

    # solo enviar nuevos
    if saved:

        msg = f"""
🔥 OFERTA JUGUETE

🧸 {product.get('title')}

💲 Precio: {product.get('price')}

🏷️ Antes: {product.get('old_price')}

🎯 Descuento: {discount:.2f}%

🔗 {product.get('link')}
"""

        print(msg)

        send_telegram(msg)