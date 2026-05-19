from scrapers.metro import scrape_metro

products = scrape_metro()

print("\n====================")
print("TOTAL PRODUCTOS:", len(products))
print("====================\n")

for p in products:
    print("TITLE:", p["title"])
    print("PRICE:", p["price"])
    print("OLD PRICE:", p["old_price"])
    print("LINK:", p["link"])
    print("--------------------")