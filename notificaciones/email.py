import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def send_email(product, discount):

    subject = f"🔥 Oferta {discount:.2f}% - {product['title']}"

    html = f"""
    <h2>🔥 OFERTA JUGUETE</h2>

    <p><b>🧸 {product['title']}</b></p>

    <p>💲 Precio: {product['price']}</p>

    <p>🏷️ Antes: {product['old_price']}</p>

    <p>🎯 Descuento: {discount:.2f}%</p>

    <p>🔗 <a href="{product['link']}">Ver producto</a></p>
    """

    params = {
        "from": EMAIL_FROM,
        "to": [EMAIL_TO],
        "subject": subject,
        "html": html
    }

    resend.Emails.send(params)