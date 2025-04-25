# searchers/ebay.py

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
}

def search(query):
    term = query['term'].replace(' ', '+')
    url = f"https://www.ebay.co.uk/sch/i.html?_nkw={term}&_sop=10"

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print("[eBay] Request failed:", e, flush=True)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = []

    for listing in soup.select(".s-item"):
        title_el = listing.select_one(".s-item__title")
        price_el = listing.select_one(".s-item__price")
        link_el = listing.select_one(".s-item__link")

        if title_el and price_el and link_el:
            item_id = link_el['href'].split('/')[-1].split('?')[0]
            items.append({
                "id": item_id,
                "title": title_el.text.strip(),
                "price": price_el.text.strip(),
                "url": link_el['href']
            })

    return items
