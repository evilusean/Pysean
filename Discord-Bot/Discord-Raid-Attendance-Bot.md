### Discord & Web Ecosystem Attendance Setup

Automation via Discord and web integration minimizes officer workload by linking raid sign-ups, in-game rosters, and combat log data into a single tracking pipeline.

---

### Method 1: `wowaudit` + Discord Bot (Fully Automated)

#### Overview
`wowaudit` connects directly to your Discord server and Warcraft Logs. It synchronizes sign-ups from Discord event scheduling tools (like Raid-Helper) with actual combat logs to verify attendance without manual data entry.

#### Setup Pipeline
1. **Connect Platform**: Link your guild on `wowaudit.com` using Battle.net OAuth.
2. **Discord Bot Authorization**: Invite the `wowaudit` Discord Bot to your server and grant permissions to inspect raid sign-up channels.
3. **Log Integration**: Connect your guild's Warcraft Logs API key to `wowaudit`.

#### Automated Tracking Logic
