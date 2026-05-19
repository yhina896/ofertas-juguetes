import requests

TOKEN = "8899955127:AAHBLtiN-L2-LZloAPt1ixh62jU4T6BzIx4"
CHAT_ID = "5450728827"

def send_telegram(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })