# Discord & Web Ecosystem Attendance Setup

Automation via Discord and web integration minimizes officer workload by linking raid sign-ups, in-game rosters, and combat log data into a single tracking pipeline.

---

## Method 1: wowaudit + Discord Bot (Fully Automated)

### Overview
`wowaudit` connects directly to your Discord server and Warcraft Logs. It synchronizes sign-ups from Discord event scheduling tools (like Raid-Helper) with actual combat logs to verify attendance without manual data entry.

### Setup Pipeline
1. **Connect Platform**: Link your guild on `wowaudit.com` using Battle.net OAuth.
2. **Discord Bot Authorization**: Invite the `wowaudit` Discord Bot to your server and grant permissions to inspect raid sign-up channels.
3. **Log Integration**: Connect your guild's Warcraft Logs API key to `wowaudit`.

### Automated Tracking Logic
[ Discord Event / Raid-Helper ] --(Sign-ups)--> [ wowaudit Dashboard ]
                                                      ^
                                                      | (Cross-Reference)
[ Warcraft Logs API ] ----------(Actual Kills)--------+
                                                      |
                                                      v
                                       [ Auto-Calculated Attendance ]

* **Signed Up & Present**: Marked as "Attended".
* **Signed Up & Missing**: Marked as "Late / Absenter" (Flaked).
* **Late Sign-Up / Bench**: Marked as "Benched" (Preserves core raider standing).

### Friction Level
* **Initial Setup**: ~5 minutes.
* **Ongoing Officer Effort**: 0 minutes (Runs passively on log upload).

---

## Method 2: Raidify / WoW Classic Raid Tools (WCRT) (Addon Export)

### Overview
For guilds that prefer to manage rosters locally or through custom Discord webhooks, lightweight in-game addons snapshot the raid roster on demand and output structured data.

### In-Game Execution Loop
1. Form the raid group in-game.
2. Run the snapshot command:
   * **Raidify**: Type `/raidify start` at pull / `/raidify end` after boss clear.
   * **WCRT**: Type `/wcrt export` or click the UI snapshot button.
3. The addon writes the roster array (Player Name, Class, Rank, Role, Timestamp) to its `SavedVariables` file.

### Automated Discord Webhook Integration (Python Script)
Pair the addon output with a local Python watcher daemon to push snapshots to Discord automatically:

import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
SAVED_VARS_PATH = r"C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account\YOUR_ACCOUNT\SavedVariables\Raidify.lua"

class RaidLogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(SAVED_VARS_PATH):
            time.sleep(1)
            payload = {
                "username": "Raid Attendance Bot",
                "embeds": [{
                    "title": "Raid Roster Snapshot Captured",
                    "description": "In-game roster successfully synced to attendance ledger.",
                    "color": 3447003,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }]
            }
            requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(RaidLogHandler(), path=os.path.dirname(SAVED_VARS_PATH), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

### Friction Level
* **Initial Setup**: ~10 minutes (Script configuration).
* **Ongoing Officer Effort**: Single `/reload` or slash command per raid.
