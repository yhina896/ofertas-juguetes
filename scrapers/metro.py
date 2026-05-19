from playwright.sync_api import sync_playwright
import re

def scrape_metro():

    products = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        page = browser.new_page()

        page.goto(
            "https://www.metro.pe/la-jugueteria",
            timeout=60000
        )

        page.wait_for_timeout(8000)

        # scroll para cargar productos
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(5000)

        # detectar cards (Metro usa muchos divs, buscamos links con productos)
        cards = page.locator("a")

        count = cards.count()

        links_seen = set()

        for i in range(count):

            try:
                card = cards.nth(i)

                href = card.get_attribute("href")

                if not href:
                    continue

                if "/p/" not in href:
                    continue

                if href.startswith("/"):
                    href = "https://www.metro.pe" + href

                if href in links_seen:
                    continue

                links_seen.add(href)

                text = card.inner_text()

                if not text or len(text) < 10:
                    continue

                # precios
                prices = re.findall(r'S/\s?\d+[.,]?\d*', text)

                numeric_prices = []

                for ptxt in prices:
                    try:
                        val = float(re.sub(r'[^0-9.]', '', ptxt))
                        numeric_prices.append(val)
                    except:
                        pass

                if len(numeric_prices) == 0:
                    continue

                numeric_prices.sort()

                price = f"S/ {numeric_prices[0]:.2f}"
                old_price = f"S/ {numeric_prices[-1]:.2f}" if len(numeric_prices) > 1 else price

                # título (heurística simple)
                lines = text.split("\n")
                title = next((l.strip() for l in lines if len(l.strip()) > 8 and "S/" not in l), None)

                if not title:
                    continue

                # filtro juguetes
                keywords = [
                    "lego", "barbie", "hot wheels", "nerf",
                    "muñeca", "juguete", "peluche", "hasbro",
                    "fisher", "disney", "carro"
                ]

                if not any(k in title.lower() for k in keywords):
                    continue

                product = {
                    "title": title,
                    "price": price,
                    "old_price": old_price,
                    "link": href
                }

                products.append(product)

            except:
                continue

        browser.close()

    return products