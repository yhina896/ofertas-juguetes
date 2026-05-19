from scrapers.plaza_vea import scrape_plaza_vea
from notificaciones.telegram_bot import send_telegram
from database.db import init_db, save_product

import re


def clean_price(price_text):
    try:
        number = re.sub(r'[^0-9.]', '', price_text)
        return float(number)
    except:
        return None


init_db()

products = scrape_plaza_vea()

print(f"✅ TOTAL PRODUCTOS: {len(products)}")


for product in products:

    current_price = clean_price(product.get('price', ''))
    old_price = clean_price(product.get('old_price', ''))

    if not current_price or not old_price:
        print("⚠️ Producto sin precios válidos")
        continue

    if old_price <= 0:
        continue

    discount = ((old_price - current_price) / old_price) * 100

    print(f"🟢 {product.get('title')} => {discount:.2f}%")

    if discount <= 20:
        continue

    if discount > 95:
        continue


    # -------------------------
    # SIEMPRE ENVIAR TELEGRAM
    # -------------------------
    msg = f"""
🔥 OFERTA JUGUETE

🧸 {product.get('title')}

💲 Precio: {product.get('price')}

🏷️ Antes: {product.get('old_price')}

🎯 Descuento: {discount:.2f}%

🔗 {product.get('link')}
"""

    print("📲 ENVIANDO TELEGRAM...")
    send_telegram(msg)


    # -------------------------
    # SOLO GUARDAR SI ES NUEVO
    # -------------------------
    is_new = save_product(product)

    if is_new:
        print("🆕 Producto nuevo guardado")
    else:
        print("🔁 Producto ya existía (no se guarda duplicado)")