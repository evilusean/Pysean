# TabulaSean - Chromium Tab Export/Import Extension

## What is TabulaSean?
TabulaSean is a privacy-friendly Chromium extension that lets you save all open tabs (across all windows) to a timestamped text file, and restore them later—even on another device. Great for backup, migration, or sharing your browsing session.

## Features
- Save all open tabs from all windows, grouped and labeled (e.g., "Window 1")
- Export tabs to a text file in `[Tab title, URL]` format, one tab per line, with empty lines between windows
- Filename includes timestamp: `yyyy-mm-dd-HHMMSS.txt`
- Import feature: restore tabs and windows from a saved file
- Works on Linux, Mac, and any Chromium-based browser
- No Google account or cloud required

## Installation
1. Download or clone this repository.
2. Open Chromium/Chrome and go to `chrome://extensions`.
3. Enable "Developer mode" (top right).
4. Click "Load unpacked" and select the `TabulaSean-ChromiumExtenSean` folder.
5. The TabulaSean icon will appear in your browser toolbar.

## Usage
1. Click the TabulaSean icon to open the popup.
2. Click **Save All Tabs** to export all tabs from all windows to a text file in your downloads folder.
3. To restore tabs, click **Import Tabs** and select a previously saved file. Each window group will be opened in its own browser window.

## Privacy
TabulaSean does not send any data to external servers. All tab data is saved locally and only exported/imported by you.

## License
MIT

## To Do / Future Sean Problems :
Save to clipboard
Save to Obsidian
Create a central default folder that will always take the main repos, add to syncthing

Save a single website to a future sean problem text document that will take all the videos on that text document and download the 
Add that document to syncthing and the default folder, so I can have all my tabs on both devices

Have a script that will run a cron job once a day and update the syncthing folder with my latest tabs on both devices