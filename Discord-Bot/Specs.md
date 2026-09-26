# Guild Discord Bot Architecture & Feature Specification

### Bot Architecture Overview

Bot System Flow:
- Discord Developer Portal (Bot Token, Message Content Intent, Server Members Intent)
  ↓
- Guild Discord Bot
  ├─ Raid Logistics (Embed Rosters, Soft-Reserves, Attendance)
  ├─ Guild Economy (Crafter Directory, Bank Tracking, AH Price Checks)
  ├─ Voice & Audio Engine (FFmpeg Pipeline, yt-dlp & Cookies, Spotify API Resolver)
  ├─ User Verification (Auto-Nicknaming, Role Assignment)
  ├─ In-Game Tooling (Warcraft Logs, Item/Spell Lookups)
  └─ Event & Alert Timers (World Event Countdown, Leveling Milestones)
  ↓
- Persistent Hosting Server (Home Server / Pi / VPS, Docker Containerization, FFmpeg + Python / Node.js)

---

#### Core Dependencies & System Requirements

To build a fully functional Discord bot capable of handling text commands, interactive UI components, and voice channel audio, 
  you will need the following core resources and system tools:

##### Developer Platform & Credentials
* **Discord Developer Portal:** Create a new application at [Discord Developer Portal](https://discord.com/developers/applications) to generate your **Bot Token** and **Application ID**.
* **Privileged Gateway Intents:** Enable **Message Content Intent** and **Server Members Intent** under the Bot settings tab. These are mandatory for reading slash commands, managing guild members, and processing text inputs.
* **OAuth2 Permissions:** Generate an invite URL using the OAuth2 URL Generator with the `bot` scope and permissions: `Send Messages`, `Manage Roles`, `Manage Nicknames`, `Connect`, `Speak`, `Use Voice Activity`, and `Use Application Commands`.

##### Software Runtime & Libraries
* **Language Runtime:** [Node.js (v18+)](https://nodejs.org/) or [Python (3.10+)](https://www.python.org/).
* **Discord API Wrapper:** `discord.js` (v14) for JavaScript/TypeScript OR `discord.py` / `disnake` for Python.
* **Audio Encoding:** [FFmpeg](https://ffmpeg.org/) installed directly on the hosting OS or containerized environment to convert media streams into PCM/Opus format.
* **Media Stream Extraction:** [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) to resolve YouTube, SoundCloud, and direct web links into streamable audio.
* **External APIs:** [Spotify Web API](https://developer.spotify.com/documentation/web-api) to translate Spotify track/album links into YouTube metadata queries, and [Warcraft Logs API](https://www.warcraftlogs.com/api/docs) for combat log parsing.

##### Hosting Environment
* **Persistent Host:** A continuous WebSocket connection is required for Discord voice and real-time events. Serverless platforms (e.g., Vercel, AWS Lambda) are incompatible. Use a local home server, Raspberry Pi, Docker container, or a Linux VPS ([Hetzner](https://www.hetzner.com/), [DigitalOcean](https://www.digitalocean.com/), or [Linode](https://www.linode.com/)).

---

#### Module Specifications & Feature Roadmap

##### Module 1: Voice & Audio Playback (Music & Song Requests)
* **Audio Queue Architecture:** Implements a per-guild queue storing requested tracks, duration, thumbnail, and the user who requested it.
* **Stream Resolution:** Uses `yt-dlp` to extract direct audio streams.
* **Anti-Blocking Measures:** Configure `yt-dlp` with a `cookies.txt` file exported from an active browser or set up residential proxies to prevent YouTube HTTP 429 (Rate Limit) and sign-in verification errors.
* **Playback Controls:** Interactive embed with buttons for `Play/Pause`, `Skip`, `Stop`, and `Queue List`.

##### Module 2: Raid Logistics & Roster Management
* **Interactive Sign-ups:** Post `/raid` embeds featuring Discord UI buttons (`Tank`, `Healer`, `Melee DPS`, `Ranged DPS`, `Bench`, `Absence`). Pressing a button updates the embed dynamically and stores user IDs in the database.
* **Utility Auditing:** Parses roster assignments to check for critical class utilities (e.g., Curse of Elements, Bloodlust/Heroism, Sunder Armor, Soulstones) and alerts raid leaders if key buffs are missing.
* **Soft-Reserves:** A `/sr` command allowing members to reserve specific item IDs prior to the raid lockouts, automatically exporting a clean list for the raid leader.

##### Module 3: Onboarding & Member Verification
* **Auto-Verification Flow:** Automatically assigns a "Guest" role upon server join. The bot prompts the user for their main character name, class, and primary spec via a modal interface.
* **Role & Nickname Synchronization:** Sets the user's Discord nickname format to `CharacterName (Class - Spec)` and assigns class-specific roles (e.g., `@Mage`, `@Raider`).

##### Module 4: Guild Economy & Crafter Directory
* **Recipe Indexing:** Crafters register their maxed professions and notable recipes via `/recipe add [Profession] [Recipe Name]`.
* **Crafter Lookup:** Guild members query required items using `/findcraft [Item Name]`. The bot returns an embed listing online members capable of crafting the requested item along with required reagent lists.
* **Bank & Bounties:** Displays an updated channel embed listing priority guild bank requests (e.g., target stacks of raid consumables/reagents) and current bounties.

##### Module 5: Game Data & Log Integration
* **Warcraft Logs Webhooks:** Listens for new uploads via the Warcraft Logs API and automatically broadcasts a summary embed containing fight durations, wipe counts, top DPS/HPS, and execution metrics.
* **Item & Spell Tooltips:** Allows members to type `/item [Item Name]` or `/spell [Spell Name]` to fetch tooltips, drop rates, and source locations.

---

#### Recommended Open-Source Implementations

If you prefer deploying a tested codebase rather than writing raw audio pipelines from scratch, consider these open-source templates:

* **[Vocard](https://github.com/vaxerdec/Vocard):** Fully featured Python music bot with a built-in web dashboard, DJ roles, and native YouTube/Spotify playlist handling.
* **[Muse](https://github.com/codetheweb/muse):** Self-hosted TypeScript/Node.js audio bot optimized for private Discord communities.
* **[Discord.py Examples](https://github.com/Rapptz/discord.py/tree/master/examples):** Official code samples including basic voice connection, slash commands, and interactive button UI components.
