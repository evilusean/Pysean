# World of Warcraft: Japanese Audio + English Text & Quest Voiceover Setup

## 1. Native Client Japanese Audio (English Text / UI)
Sets native NPC barks, combat shouts, cinematic dialogue, and vendor greetings to full Japanese while keeping all UI, quest logs, and item tooltips in English.

### Method A: Battle.net Launcher
1. Open **Battle.net Desktop App**.
2. Go to **Settings** -> **Game Settings**.
3. Under **World of Warcraft**, locate the language settings.
4. Set **Game Text Language** to `English`.
5. Set **Audio Language** to `Japanese (日本語)`.
6. Click **Done** and allow Battle.net to download the Japanese audio patch (~1.5 GB).

### Method B: Direct Configuration Edit (Config.wtf)
If the launcher enforces a matching text/audio pair, manually split the locales in your local configuration:

1. Open your WoW installation directory:
   `World of Warcraft/_classic_era_/WTF/`
2. Edit **Config.wtf** in a plain text editor.
3. Add or modify the following lines:
   SET textLocale "enUS"
   SET audioLocale "jaJP"
4. Save and launch the game.

---

## 2. Full Quest Dialogue AI TTS Addons (Japanese Audio + Read-Along English Text)
Native WoW only voices vendor greetings and boss lines. To hear full quest text read aloud in AI Japanese while reading along in English, install the **VoiceOver** framework alongside a reading UI addon.

### Core Addons Required
* **VoiceOver (Classic / Era Core)**: The underlying audio playback engine that streams quest voice lines.
* **VoiceOver Sounds (Japanese / jaJP Pack)**: The AI-generated neural TTS sound database containing thousands of voiced Japanese quest narratives.
* **Storyline** or **Immersion**: (Optional UI Addon) Replaces the standard quest window with an animated, cinematic dialogue frame (similar to modern RPGs/FFXIV) that displays English subtitles line-by-line in sync with the Japanese audio playback.

### Step-by-Step Installation
1. Install **VoiceOver (Classic)** via CurseForge, WoWUp, or manual extract:
   * Path: `World of Warcraft/_classic_era_/Interface/AddOns/VoiceOver/`
2. Download and extract the **Japanese AI Voice Pack**:
   * Path: `World of Warcraft/_classic_era_/Interface/AddOns/VoiceOver_Sounds_jaJP/`
3. (Optional) Install **Storyline** or **Immersion** for cinematic read-along frames:
   * Path: `World of Warcraft/_classic_era_/Interface/AddOns/Storyline/`
4. Launch the game and verify all installed addons are checked in the Character Selection **AddOns** menu.

---

## 3. Workflow & In-Game Controls
* **UI & Quest Frame**: Displays 100% English text for fast objective verification and sentence alignment.
* **Audio Playback**: Accepting or opening a quest triggers the Japanese AI voice engine automatically.
* **Read-Along Immersion**: With Storyline or Immersion enabled, quest text pages advance sequentially as the Japanese TTS audio plays, making it easy to parse English context against Japanese listening.
* **In-Game Commands**:
  * Type `/fvo` or `/voiceover` in-chat to bring up the control panel.
  * Adjust volume channels, toggle auto-play on quest open, or tweak speech playback speed.
 
## World of Warcraft: Japanese Voiceover Addon Mechanics

### How VoiceOver Handles Localization
* **No Real-Time Screen Scraping**: The VoiceOver addon does not translate on-the-fly or read English text aloud. 
* **Quest ID Mapping**: It operates using Blizzard's hidden **Quest ID** system, matching each unique quest identifier to a pre-rendered audio file stored inside the addon's data folder.
* **Native Japanese Scripts**: The `jaJP` sound pack is compiled using official Japanese localized quest text (authored by Blizzard's native localization team) processed through neural TTS models.
* **Result**: Even though your client UI and screen text are set to English (`enUS`), opening a quest triggers the corresponding Quest ID audio file, playing natural, contextually accurate Japanese voice acting for language immersion.
