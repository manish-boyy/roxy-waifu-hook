#!/usr/bin/env python3
"""
Roxy Waifu Hook - Anime waifu images to Discord webhook every 10 minutes.

Public API: nekos.best (no key needed)
  - https://nekos.best/api/v2/waifu (primary)
  - https://nekos.best/api/v2/neko  (fallback)

Setup:
  1. Set your Discord webhook URL (env var recommended):
       export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'
  2. Run:
       python3 waifu_webhook.py

Discord webhook: Server Settings -> Integrations -> Webhooks -> New Webhook -> Copy URL

NOTE: nekos.best requires a proper User-Agent header:
  format `AppName (contact)` - e.g. `RoxyWaifuHook (https://github.com/manish-boyy/roxy-waifu-hook)`
  Generic values like `Mozilla/5.0`, `python-requests`, `test`, `bot` get HTTP 403.
"""
import json
import time
import urllib.request
import urllib.error
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "PASTE_YOUR_DISCORD_WEBHOOK_URL_HERE")
INTERVAL_SECONDS = 10 * 60  # 10 minutes

# Change contact URL to your own repo/profile (required by nekos.best API rules)
USER_AGENT = "RoxyWaifuHook (https://github.com/manish-boyy/roxy-waifu-hook)"

API_URLS = [
    "https://nekos.best/api/v2/waifu",
    "https://nekos.best/api/v2/neko",
]


def get_waifu_image():
    for api_url in API_URLS:
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
                result = data["results"][0]
                return result["url"], result.get("artist_name", "unknown"), result.get("source_url", "")
        except Exception as e:
            print(f"[WARN] {api_url} failed: {e}")
            continue
    return None, None, None


def send_to_discord(image_url, artist, source_url):
    payload = {
        "content": "Here's your waifu",
        "embeds": [{
            "title": "Anime Waifu",
            "color": 16751916,
            "image": {"url": image_url},
            "footer": {"text": f"Artist: {artist} | Powered by nekos.best"},
        }]
    }
    if source_url:
        payload["embeds"][0]["url"] = source_url

    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        print(f"[OK] Discord responded {r.status}")


def job():
    print("Fetching waifu image...")
    url, artist, source = get_waifu_image()
    if not url:
        print("[FAIL] All APIs failed, skipping this round.")
        return
    print(f"[OK] Got image: {url}")
    send_to_discord(url, artist, source)


if __name__ == "__main__":
    if "PASTE_YOUR" in DISCORD_WEBHOOK_URL or not DISCORD_WEBHOOK_URL.startswith("http"):
        print("ERROR: Set your Discord webhook URL first.")
        print("  Option 1: export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'")
        print("  Option 2: edit DISCORD_WEBHOOK_URL in this file")
        exit(1)
    print("Starting waifu webhook, every 10 min. Press Ctrl+C to stop.")
    while True:
        try:
            job()
        except urllib.error.HTTPError as e:
            print(f"[ERROR] Discord failed: {e.code} {e.read().decode()[:200]}")
        except Exception as e:
            print(f"[ERROR] {e}")
        print(f"Sleeping {INTERVAL_SECONDS}s...")
        time.sleep(INTERVAL_SECONDS)
