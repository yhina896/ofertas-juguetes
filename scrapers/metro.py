import requests


def scrape_metro():

    CATEGORY_ID = "1001467"  # ⚠️ ejemplo, puede cambiar

    url = f"https://www.metro.pe/api/catalog_system/pub/products/search?fq=C:{CATEGORY_ID}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    products = []

    for item in data:

        try:
            title = item.get("productName")

            # precios VTEX
            price = item["items"][0]["sellers"][0]["commertialOffer"]["Price"]
            list_price = item["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]

            # link limpio
            link = "https://www.metro.pe" + item.get("link", "")

            product = {
                "title": title,
                "price": f"S/ {price:.2f}",
                "old_price": f"S/ {list_price:.2f}",
                "link": link
            }

            products.append(product)

            print("METRO:", product)

        except Exception as e:
            print("ERROR:", e)

    return products


if __name__ == "__main__":
    data = scrape_metro()
    print("TOTAL:", len(data))