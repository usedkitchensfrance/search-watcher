# searchers/ebay.py

import requests
from bs4 import BeautifulSoup

def search(query):
    term = query["term"]
    print(f"📡 [eBay] Searching eBay for '{term}'")

    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={term.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ [eBay] Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    listings = soup.select(".s-item")
    for listing in listings:
        title_elem = listing.select_one(".s-item__title")
        link_elem = listing.select_one(".s-item__link")
        price_elem = listing.select_one(".s-item__price")

        if not (title_elem and link_elem and price_elem):
            continue

        title = title_elem.get_text(strip=True)
        url = link_elem["href"]
        price = price_elem.get_text(strip=True)
        item_id = url.split("/")[-1].split("?")[0]

        items.append({
            "id": item_id,
            "title": title,
            "price": price,
            "url": url
        })

    print(f"📦 [eBay] Found {len(items)} results for '{term}'")
    return items
