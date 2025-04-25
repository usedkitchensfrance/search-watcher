# main.py
import time
import json
import threading
import os

print("📦 Importing modules...")

from searchers import ebay, gumtree, leboncoin
from email_alerts import send_email

print("📂 Loading searches...")

try:
    with open("searches.json") as f:
        search_queries = json.load(f)
except Exception as e:
    print("❌ Failed to load searches.json:", e)
    search_queries = {}

print("📂 Loading seen items...")

try:
    with open("seen_items.json") as f:
        seen_items = json.load(f)
except FileNotFoundError:
    seen_items = {}
except Exception as e:
    print("❌ Failed to load seen_items.json:", e)
    seen_items = {}

SEARCH_FUNCTIONS = {
    "ebay": ebay.search,
    "gumtree": gumtree.search,
    "leboncoin": leboncoin.search
}

def run_search(platform, query):
    print(f"🔍 Searching {platform} for: {query['term']}")
    results = SEARCH_FUNCTIONS[platform](query)
    new_results = []

    for result in results:
        if result['id'] not in seen_items.get(platform, []):
            seen_items.setdefault(platform, []).append(result['id'])
            new_results.append(result)

    if new_results:
        print(f"📬 Found {len(new_results)} new results for {query['term']} on {platform}. Sending email...")
        send_email(platform, query['term'], new_results)

def send_test_email():
    print("📧 Sending startup test email...")
    test_items = [
        {
            "id": "test123",
            "title": "🔥 TEST ITEM: Toaster Deluxe",
            "price": "£20",
            "url": "https://example.com/item/test123",
            "location": "London"
        }
    ]
    send_email("test_platform", "test search", test_items)

def search_loop():
    print("🔁 Starting main search loop (every 50 seconds)...")
    while True:
        for platform, queries in search_queries.items():
            for query in queries:
                threading.Thread(target=run_search, args=(platform, query)).start()

        with open("seen_items.json", "w") as f:
            json.dump(seen_items, f, indent=2)

        time.sleep(50)

if __name__ == "__main__":
    print("✅ Search Watcher started.")
    print("Using Gmail from:", os.environ.get("EMAIL_FROM", "<not set>"))

    send_test_email()  # <-- THIS sends test email on every startup
    search_loop()
