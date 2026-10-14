# Roxy Waifu Hook 🌸

Posts an anime waifu image to your Discord channel **every 10 minutes** using the free [nekos.best](https://nekos.best) API. No API key needed. Stdlib only — no `pip install`.

## How it works

1. Fetches from `https://nekos.best/api/v2/waifu` (fallback: `/neko`)
2. Sends a Discord embed with the image + artist credit
3. Sleeps 600s, repeats forever

## Setup

**1. Get a Discord webhook URL**

Discord Server → Settings → Integrations → Webhooks → New Webhook → Copy URL. It looks like:
`https://discord.com/api/webhooks/123.../abc...`

**2. Run**

```bash
# recommended: env var (keeps secrets out of code)
export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN'
python3 waifu_webhook.py
```

Or edit `DISCORD_WEBHOOK_URL` at the top of `waifu_webhook.py`.

**Requirements:** Python 3.6+ only. No dependencies.

## Run 24/7

```bash
# background with logs
nohup python3 -u waifu_webhook.py > waifu.log 2>&1 &
echo $! > waifu.pid

# check logs
cat waifu.log

# stop
kill $(cat waifu.pid)
```

On Pterodactyl, add a `python3 -u waifu_webhook.py` spawn to your `start.js` so it auto-starts on container reboot (see this project's history for an example).

## Important: User-Agent

nekos.best **blocks** generic / browser / library User-Agents (`Mozilla/5.0`, `python-requests`, `test`, `bot` → HTTP 403).

This script sends:
```
RoxyWaifuHook (https://github.com/manish-boyy/roxy-waifu-hook)
```

Change the contact part to your own repo/profile per [their docs](https://docs.nekos.best/getting-started/api-reference.html#user-agent).

## Config

| Variable | Default | Meaning |
|---|---|---|
| `DISCORD_WEBHOOK_URL` | `PASTE_YOUR_...` | Discord webhook to post to |
| `INTERVAL_SECONDS` | `600` | Delay between posts |
| `USER_AGENT` | `RoxyWaifuHook (...)` | Required by nekos.best |

## Troubleshooting

- `ERROR: Set your Discord webhook URL first` → export the env var
- `HTTP 403 from nekos.best` → fix `USER_AGENT` to `AppName (contact)` format
- `HTTP 403 from Discord` → webhook deleted/invalid, or blocked UA — regenerate webhook
- Dead APIs tried earlier: `waifu.pics` (DNS), `waifu.im` (Cloudflare), `*.vercel.app` mirrors (deleted)

## License

MIT — do what you want, credit appreciated.
