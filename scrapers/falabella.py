from playwright.sync_api import sync_playwright
import re

def scrape_falabella():

    products = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        page = browser.new_page()

        page.goto(
            "https://www.falabella.com.pe/falabella-pe/category/CATG34943/Jugueteria",
            timeout=60000
        )

        page.wait_for_timeout(10000)

        # scroll múltiple (Falabella necesita más carga)
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(4000)

        # cards principales
        items = page.locator("a")

        count = items.count()

        seen = set()

        for i in range(count):

            try:
                item = items.nth(i)

                href = item.get_attribute("href")

                if not href:
                    continue

                if "falabella.com.pe/falabella-pe/product" not in href:
                    continue

                if href in seen:
                    continue

                seen.add(href)

                if href.startswith("/"):
                    href = "https://www.falabella.com.pe" + href

                text = item.inner_text()

                if not text:
                    continue

                prices = re.findall(r'S/\s?\d+[.,]?\d*', text)

                nums = []

                for p in prices:
                    try:
                        nums.append(float(re.sub(r'[^0-9.]', '', p)))
                    except:
                        pass

                if len(nums) == 0:
                    continue

                nums.sort()

                price = f"S/ {nums[0]:.2f}"
                old_price = f"S/ {nums[-1]:.2f}" if len(nums) > 1 else price

                lines = text.split("\n")

                title = next(
                    (l.strip() for l in lines if len(l.strip()) > 10 and "S/" not in l),
                    None
                )

                if not title:
                    continue

                keywords = [
                    "lego", "barbie", "hot wheels", "nerf",
                    "muñeca", "juguete", "disney", "fisher",
                    "hasbro", "peluche", "carro", "hot wheels",
                    "peppa","play doh","rompecabezas","pistola",
                    "pj mask","cocina","pista de carreras","set de juego casa",
                    "bonnie","baby","cute","monster","frozen","huanger","nini",
                    "princesas","fashion","litle features","funko","vehiculo",
                    "play set supermercado","triciclo","supermarket","pack de slime",
                    "figura de colección","mini coleccionables","super mario",
                    "perrito","set teens unicornio","pista","set estacion","set de juego",
                    "cocina","casa","hello kitty","pistas","camara","bloques","caja de herramientas",
                    "reborn","karaoke","belleza"
                ]

                if not any(k in title.lower() for k in keywords):
                    continue

                products.append({
                    "title": title,
                    "price": price,
                    "old_price": old_price,
                    "link": href
                })

            except:
                continue

        browser.close()

    return products