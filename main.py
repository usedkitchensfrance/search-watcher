# main.py
import time
import json
import threading
import os

print("📦 Importing modules...")

from searchers import ebay, gumtree, leboncoin
from email_alerts import send_email

print("📂 Loading searches...")

with open("searches.json") as f:
    search_queries = json.load(f)

print("📂 Loading seen items...")

try:
    with open("seen_items.json") as f:
        seen_items = json.load(f)
except FileNotFoundError:
    seen_items = {}

print("✅ Startup successful. Beginning search loop...")
print("Using Gmail from:", os.environ.get("EMAIL_FROM", "<not set>"))
