import os

os.environ["TELEGRAM_TOKEN"] = "8899955127:AAHBLtiN-L2-LZloAPt1ixh62jU4T6BzIx4"
os.environ["TELEGRAM_CHAT_ID"] = "-1003976574119"

from notificaciones.telegram_bot import send_telegram

send_telegram("Prueba desde Python")

#1001467