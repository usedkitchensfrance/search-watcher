# main.py
import time

print("✅ Web Service started!", flush=True)

counter = 0
while True:
    print(f"🔁 Loop {counter}", flush=True)
    time.sleep(10)
    counter += 1
