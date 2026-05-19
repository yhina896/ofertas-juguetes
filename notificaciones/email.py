import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_email(product, discount, store_name):

    subject = f"🔥 OFERTA {discount:.2f}% - {store_name}"

    html = f"""
    <h2>🔥 OFERTA JUGUETES - {store_name}</h2>

    <p><b>🧸 {product['title']}</b></p>

    <p>🏪 Tienda: {store_name}</p>

    <p>💲 Precio: {product['price']}</p>

    <p>🏷️ Antes: {product['old_price']}</p>

    <p>🎯 Descuento: {discount:.2f}%</p>

    <p>🔗 <a href="{product['link']}">Ver producto</a></p>
    """

    params = {
        "from": f"Descuentos de Juguetes <{EMAIL_FROM}>",
        "to": [EMAIL_TO],
        "subject": subject,
        "html": html
    }

    resend.Emails.send(params)