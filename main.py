# main.py
import time
import json
import threading
import os
from searchers import ebay, gumtree, leboncoin
from email_alerts import send_email

with open("searches.json") as f:
    search_queries = json.load(f)

try:
    with open("seen_items.json") as f:
        seen_items = json.load(f)
except FileNotFoundError:
    seen_items = {}

SEARCH_FUNCTIONS = {
    "ebay": ebay.search,
    "gumtree": gumtree.search,
    "leboncoin": leboncoin.search
}

def run_search(platform, query):
    print(f"Searching {platform} for: {query['term']}")
    results = SEARCH_FUNCTIONS[platform](query)
    new_results = []

    for result in results:
        if result['id'] not in seen_items.get(platform, []):
            seen_items.setdefault(platform, []).append(result['id'])
            new_results.append(result)

    if new_results:
        send_email(platform, query['term'], new_results)

def search_loop():
    while True:
        for platform, queries in search_queries.items():
            for query in queries:
                threading.Thread(target=run_search, args=(platform, query)).start()

        with open("seen_items.json", "w") as f:
            json.dump(seen_items, f, indent=2)

        time.sleep(50)

if __name__ == "__main__":
    print("Search Watcher started. Running every 50 seconds...")
    print("Using Gmail from:", os.environ.get("EMAIL_FROM", "<not set>"))
    search_loop()
