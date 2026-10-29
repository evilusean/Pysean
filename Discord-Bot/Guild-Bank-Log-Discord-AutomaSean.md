### Guild Bank Automation & Logging Architecture

This guide breaks down the technical setup for automating World of Warcraft guild bank updates to Discord, along with recommended logging addons and the technical limitations of the client.

---

### Part 1: Automated Guild Bank Discord Pipeline

#### The Engine Limitation
World of Warcraft Lua addons run in a sandboxed environment without direct internet privileges. An addon **cannot** make HTTP requests (like sending a Discord webhook) while the game client is running. 

The WoW client only writes memory data out to disk (`SavedVariables` `.lua` files) when:
1. You exit the game (`/exit` or `Alt+F4`).
2. You logout to character select.
3. You execute an UI reload (`/reload`).

#### The Automated Solution Workflow
To achieve automated Discord posting without manually copy-pasting text, you link three components together:
