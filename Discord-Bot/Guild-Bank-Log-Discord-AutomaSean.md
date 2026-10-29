# Guild Bank Automation & Logging Architecture

This guide breaks down the technical setup for automating World of Warcraft guild bank updates to Discord, along with recommended logging addons and the technical limitations of the client.

---

## Part 1: Automated Guild Bank Discord Pipeline

### The Engine Limitation
World of Warcraft Lua addons run in a sandboxed environment without direct internet privileges. An addon **cannot** make HTTP requests (like sending a Discord webhook) while the game client is running.

The WoW client only writes memory data out to disk (`SavedVariables` `.lua` files) when:
1. You exit the game (`/exit` or `Alt+F4`).
2. You logout to character select.
3. You execute an UI reload (`/reload`).

### The Automated Solution Workflow
To achieve automated Discord posting without manually copy-pasting text, you link three components together:

[ In-Game Guild Bank ]
        │
        ▼ (Open bank & trigger addon scan)
[ In-Game Addon Data ]
        │
        ▼ (Execute /reload command)
[ SavedVariables .lua File on SSD ]
        │
        ▼ (Local Python/Node background script detects file edit)
[ Desktop Automation Script ]
        │
        ▼ (Sends HTTP POST payload)
[ Discord Channel Webhook ]

---

## Step-by-Step Implementation

### Step 1: Discord Webhook Setup
1. Open Discord and go to your server settings for the designated channel (e.g., `#guild-bank-logs`).
2. Navigate to **Integrations** -> **Webhooks** -> **New Webhook**.
3. Name the webhook (e.g., `Guild Bank Bot`) and set its target channel.
4. Click **Copy Webhook URL**.

### Step 2: Local Desktop Automation Script (Python)
Run a local script in the background on your PC that watches your WoW `SavedVariables` file. When the addon updates the file upon `/reload`, the script reads the inventory array and pushes it to Discord via Webhook.

**Python Dependencies Required:**
```bash
pip install requests watchdog
```


