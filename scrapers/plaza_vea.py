from playwright.sync_api import sync_playwright
import re


def scrape_plaza_vea():

    products = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        page = browser.new_page()

        page.goto(
            "https://www.plazavea.com.pe/juguetes",
            timeout=60000
        )

        page.wait_for_timeout(10000)

        # cerrar cookies
        try:

            page.evaluate("""
                const btn = document.querySelector(
                    '.cookies-consent-banner__button'
                );

                if(btn){
                    btn.click();
                }
            """)

            print("✅ Cookies cerradas")

        except:
            print("⚠️ No se pudo cerrar cookies")

        # scroll
        page.evaluate("""
            window.scrollTo(0, document.body.scrollHeight)
        """)

        page.wait_for_timeout(8000)

        # obtener todos los divs/cards
        cards = page.locator("div")

        count = cards.count()

        print("TOTAL DIVS:", count)

        links_seen = set()

        for i in range(count):

            try:

                card = cards.nth(i)

                full_text = card.inner_text()

                # debe contener precio
                if "S/" not in full_text:
                    continue

                # obtener links
                links = card.locator("a")

                if links.count() == 0:
                    continue

                href = links.first.get_attribute("href")

                if not href:
                    continue

                # completar dominio
                if href.startswith("/"):

                    href = f"https://www.plazavea.com.pe{href}"

                # evitar duplicados
                if href in links_seen:
                    continue

                links_seen.add(href)

                # detectar precios
                prices = re.findall(
                    r'S/\s?\d+[.,]?\d*',
                    full_text
                )

                if len(prices) == 0:
                    continue

                # convertir precios a float
                numeric_prices = []

                for p in prices:

                    try:

                        value = float(
                            re.sub(r'[^0-9.]', '', p)
                        )

                        numeric_prices.append(value)

                    except:
                        pass

                # ordenar precios
                numeric_prices = sorted(numeric_prices)

                # validar
                if len(numeric_prices) == 0:
                    continue

                # menor precio = actual
                price = f"S/ {numeric_prices[0]:.2f}"

                # mayor precio = anterior
                old_price = "No disponible"

                if len(numeric_prices) >= 2:

                    old_price = f"S/ {numeric_prices[-1]:.2f}"

                # detectar título
                lines = full_text.split("\n")

                title = ""

                for line in lines:

                    line = line.strip()

                    if (
                        len(line) > 5
                        and "S/" not in line
                    ):

                        title = line
                        break

                if not title:
                    continue

                # blacklist
                blacklist = [
                    "ropa",
                    "pijama",
                    "interior",
                    "cookies",
                    "cuenta",
                    "perfil",
                    "preguntas",
                    "politica",
                    "despacho",
                    "cambios",
                    "devoluciones"
                ]

                title_lower = title.lower()

                if any(word in title_lower for word in blacklist):
                    continue

                # keywords juguetes
                keywords = [
                    "lego",
                    "barbie",
                    "hot wheels",
                    "peppa",
                    "play doh",
                    "fisher",
                    "hasbro",
                    "nerf",
                    "muñeca",
                    "juguete",
                    "peluche",
                    "rompecabezas",
                    "pistola",
                    "carro",
                    "disney"
                ]

                if not any(word in title_lower for word in keywords):
                    continue

                product = {
                    "title": title,
                    "price": price,
                    "old_price": old_price,
                    "link": href
                }

                print(product)

                products.append(product)

            except Exception as e:

                print("ERROR:", e)

        browser.close()

    return products