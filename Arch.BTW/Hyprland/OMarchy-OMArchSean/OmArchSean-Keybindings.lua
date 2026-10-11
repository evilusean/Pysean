-- Keep only your personal keybinding overrides here. Add new bindings or
-- unbind defaults before replacing them.

-- ==========================================
-- Application Bindings
-- ==========================================

local terminal = "uwsm app -- " .. os.getenv("TERMINAL")
local browser = "omarchy-launch-browser"

-- o.bind("SUPER + RETURN", "Terminal", terminal .. ' --working-directory="$(omarchy-cmd-terminal-cwd)"')
-- o.bind("SUPER + SHIFT + F", "File manager", "uwsm app -- nautilus --new-window")
o.bind("SUPER + B", "Browser", browser)
-- Omarchy default: Bluetooth; replaced with private browser.
hl.unbind("SUPER + CTRL + B")
o.bind("SUPER + CTRL + B", "Browser (private)", browser .. " --private")
-- Omarchy default: Google Maps; replaced with Spotify.
hl.unbind("SUPER + SHIFT + S")
o.bind("SUPER + SHIFT + S", "Music", "omarchy-launch-or-focus spotify")
-- Omarchy default: Editor; replaced with the custom editor launcher.
hl.unbind("SUPER + SHIFT + N")
o.bind("SUPER + SHIFT + N", "Editor", "omarchy-launch-editor")
-- Omarchy default: laptop display toggle; replaced with btop.
hl.unbind("SUPER + CTRL + DELETE")
o.bind("SUPER + CTRL + DELETE", "Activity (btop)", terminal .. " -e btop")
-- Omarchy default: Docker TUI; replaced with the custom Docker launcher.
hl.unbind("SUPER + SHIFT + D")
o.bind("SUPER + SHIFT + D", "Docker", terminal .. " -e lazydocker")
o.bind("SUPER + M", "Signal", 'omarchy-launch-or-focus signal "uwsm app -- signal-desktop"')
o.bind("SUPER + ALT + M", "WhatsApp", 'omarchy-launch-or-focus-webapp WhatsApp "https://web.whatsapp.com/"')
-- Omarchy default: Music; replaced with Google Messages.
hl.unbind("SUPER + SHIFT + M")
o.bind("SUPER + SHIFT + M", "Google Messages",
  'omarchy-launch-or-focus-webapp "Google Messages" "https://messages.google.com/web/conversations"')
-- Omarchy default: pop window out; replaced with Obsidian.
hl.unbind("SUPER + O")
o.bind("SUPER + O", "Obsidian",
  'omarchy-launch-or-focus obsidian "uwsm app -- obsidian -disable-gpu --enable-wayland-ime"')
-- Omarchy default: Passwords; retained with the custom launcher below.
hl.unbind("SUPER + SHIFT + SLASH")
o.bind("SUPER + SHIFT + SLASH", "Passwords", "uwsm app -- 1password")
o.bind("SUPER + GRAVE", "ChatGPT Desktop", "omarchy-launch-or-focus chatgpt")

-- Web Apps
-- Replace Omarchy defaults on these chords so only the intended web app launches.
-- Omarchy default: Audio panel; replaced with ChatGPT.
hl.unbind("SUPER + CTRL + A")
o.bind("SUPER + CTRL + A", "ChatGPT", 'omarchy-launch-webapp "https://chatgpt.com"')
-- Omarchy default: ChatGPT; replaced with Claude.
hl.unbind("SUPER + SHIFT + A")
o.bind("SUPER + SHIFT + A", "Claude", 'omarchy-launch-webapp "https://claude.ai"')
o.bind("SUPER + A", "Gemini", 'omarchy-launch-webapp "https://gemini.google.com/"')
o.bind("SUPER + ALT + C", "Calendar", 'omarchy-launch-webapp "https://calendar.google.com"')
-- Omarchy default: Email; replaced with Gmail.
hl.unbind("SUPER + SHIFT + E")
o.bind("SUPER + SHIFT + E", "Email", 'omarchy-launch-webapp "https://mail.google.com"')
o.bind("SUPER + E", "Proton Mail", 'omarchy-launch-webapp "https://mail.proton.me"')
o.bind("SUPER + ALT + E", "Outlook Email", 'omarchy-launch-webapp "https://outlook.live.com/"')
-- Omarchy default: YouTube; retained with the custom focus-aware launcher.
hl.unbind("SUPER + SHIFT + Y")
o.bind("SUPER + SHIFT + Y", "YouTube", 'omarchy-launch-or-focus-webapp YouTube "https://youtube.com/"')
-- Omarchy default: X; retained with the custom webapp launcher.
hl.unbind("SUPER + SHIFT + X")
o.bind("SUPER + SHIFT + X", "X", 'omarchy-launch-webapp "https://x.com/"')
-- Omarchy default: X Post; retained with the custom webapp launcher.
hl.unbind("SUPER + SHIFT + ALT + X")
o.bind("SUPER + SHIFT + ALT + X", "X Post", 'omarchy-launch-webapp "https://x.com/compose/post"')

-- ==========================================
-- Custom Keybindings
-- ==========================================
-- Replacement for the broken physical D key; types lowercase "d" in the focused app.
-- SUPER+ALT+SPACE was previously the Omarchy Apps menu.
-- Omarchy default: Apps menu; replaced with typing lowercase d.
hl.unbind("SUPER + ALT + SPACE")
o.bind("SUPER + ALT + SPACE", "Type d (replacement for D key)", "wtype d")
-- Omarchy default: workspace layout toggle; replaced with lock screen.
hl.unbind("SUPER + L")
o.bind("SUPER + L", "Lock Screen", "omarchy-lock-screen")
o.bind("SUPER + SHIFT + L", "Suspend System", "~/Scripts/system/lock_and_suspend.sh")
o.bind("SUPER + ALT + L", "Restart System", "systemctl reboot")
o.bind("SUPER + ALT + SHIFT + L", "Shutdown System", "systemctl poweroff")
o.bind("SUPER + SHIFT + CTRL + C", "VS Code", "code")
-- Omarchy default: Calendar; replaced with Cursor.
hl.unbind("SUPER + SHIFT + C")
o.bind("SUPER + SHIFT + C", "Cursor", "cursor")
-- Omarchy default: Capture menu; replaced with Kiro IDE.
hl.unbind("SUPER + CTRL + C")
o.bind("SUPER + CTRL + C", "Kiro IDE", "uwsm app -- kiro")

-- hl.unbind("SUPER + Q")
-- o.bind("SUPER + Q", "Close Window", 'hyprctl dispatch killactive ""')

o.bind("SUPER + SHIFT + T", "OCR to Clipboard", "~/Scripts/system/ocr_to_clipboard.sh")
o.bind("SUPER + ALT + T", "OCR Japanese to Clipboard", "~/Scripts/system/ocr_to_clipboard_jpn.sh")
-- Omarchy default: scratchpad; replaced with screen snip.
hl.unbind("SUPER + S")
o.bind("SUPER + S", "Screen snip", "pidof slurp || hyprshot --freeze --clipboard-only --mode region --silent")

-- Recording
o.bind("SUPER + ALT + R", "Record region (no sound)", "~/Scripts/system/record.sh")
o.bind("SUPER + SHIFT + R", "Record region (with sound)", "~/Scripts/system/record.sh --sound")
o.bind("SUPER + SHIFT + ALT + R", "Record screen (with sound)", "~/Scripts/system/record.sh --fullscreen-sound")
-- Omarchy default: reminder setter; replaced with Hyprland reload.
hl.unbind("SUPER + CTRL + R")
o.bind("SUPER + CTRL + R", "Reload Hyprland", "hyprctl reload")

-- hl.unbind("SUPER + J")
o.bind("SUPER + CTRL + J", "Anki", "uwsm app -- anki")
o.bind("SUPER + SHIFT + J", "Xournal", "omarchy-launch-or-focus xournalpp")
-- o.bind("SUPER + V", "Python VENV", "uwsm app -- $TERMINAL -e bash -c 'cd ~/venv && source bin/activate && exec $SHELL'")
o.bind("SUPER + SHIFT + V", "Pysean VENV", "uwsm app -- $TERMINAL -e bash -c '~/Scripts/system/launch_pysean.sh'")
o.bind("SUPER + ALT + V", "Scripts VENV",
  "uwsm app -- $TERMINAL -e bash -c 'cd ~/Scripts && source ~/venv/bin/activate && exec $SHELL'")
-- Omarchy default: window grouping; replaced with GitHub profile.
hl.unbind("SUPER + G")
o.bind("SUPER + G", "GitHub Profile", 'omarchy-launch-browser "https://github.com/evilusean"')
-- Omarchy default: Signal; replaced with GitHub Desktop.
hl.unbind("SUPER + SHIFT + G")
o.bind("SUPER + SHIFT + G", "GitHub Desktop", "omarchy-launch-or-focus github-desktop")

-- Zoom
hl.unbind("SUPER + EQUAL")
hl.unbind("SUPER + MINUS")

o.bind("SUPER + EQUAL", "Zoom In", function()
  local zoom = hl.get_config("cursor.zoom_factor") or 1
  hl.config({ cursor = { zoom_factor = math.min(zoom + 0.1, 3) } })
end)

o.bind("SUPER + MINUS", "Zoom Out", function()
  local zoom = hl.get_config("cursor.zoom_factor") or 1
  hl.config({ cursor = { zoom_factor = math.max(zoom - 0.1, 1) } })
end)
