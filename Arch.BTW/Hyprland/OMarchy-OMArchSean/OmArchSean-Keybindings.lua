-- Keep only your personal keybinding overrides here. Add new bindings or
-- unbind defaults before replacing them.

-- omarchy-quatro updated messed up my keybindings, went from .conf to .lua

-- ==========================================
-- Application Bindings
-- ==========================================

local terminal = "uwsm app -- " .. os.getenv("TERMINAL")
local browser = "omarchy-launch-browser"

o.bind("SUPER + RETURN", "Terminal", terminal .. ' --working-directory="$(omarchy-cmd-terminal-cwd)"')
o.bind("SUPER + SHIFT + F", "File manager", "uwsm app -- nautilus --new-window")
o.bind("SUPER + B", "Browser", browser)
o.bind("SUPER + CTRL + B", "Browser (private)", browser .. " --private")
o.bind("SUPER + SHIFT + S", "Music", "omarchy-launch-or-focus spotify")
o.bind("SUPER + SHIFT + N", "Editor", "omarchy-launch-editor")
o.bind("SUPER + CTRL + DELETE", "Activity (btop)", terminal .. " -e btop")
o.bind("SUPER + SHIFT + D", "Docker", terminal .. " -e lazydocker")
o.bind("SUPER + M", "Signal", 'omarchy-launch-or-focus signal "uwsm app -- signal-desktop"')
o.bind("SUPER + ALT + M", "WhatsApp", 'omarchy-launch-or-focus-webapp WhatsApp "https://web.whatsapp.com/"')
o.bind("SUPER + SHIFT + M", "Google Messages", 'omarchy-launch-or-focus-webapp "Google Messages" "https://messages.google.com/web/conversations"')
o.bind("SUPER + O", "Obsidian", 'omarchy-launch-or-focus obsidian "uwsm app -- obsidian -disable-gpu --enable-wayland-ime"')
o.bind("SUPER + SHIFT + SLASH", "Passwords", "uwsm app -- 1password")

-- Web Apps
o.bind("SUPER + CTRL + A", "ChatGPT", 'omarchy-launch-webapp "https://chatgpt.com"')
o.bind("SUPER + SHIFT + A", "Grok", 'omarchy-launch-webapp "https://grok.com"')
o.bind("SUPER + A", "Gemini", 'omarchy-launch-webapp "https://gemini.google.com/"')
o.bind("SUPER + ALT + C", "Calendar", 'omarchy-launch-webapp "https://calendar.google.com"')
o.bind("SUPER + SHIFT + E", "Email", 'omarchy-launch-webapp "https://mail.google.com"')
o.bind("SUPER + E", "Proton Mail", 'omarchy-launch-webapp "https://mail.proton.me"')
o.bind("SUPER + ALT + E", "Outlook Email", 'omarchy-launch-webapp "https://outlook.live.com/"')
o.bind("SUPER + SHIFT + Y", "YouTube", 'omarchy-launch-or-focus-webapp YouTube "https://youtube.com/"')
o.bind("SUPER + SHIFT + X", "X", 'omarchy-launch-webapp "https://x.com/"')
o.bind("SUPER + SHIFT + ALT + X", "X Post", 'omarchy-launch-webapp "https://x.com/compose/post"')

-- ==========================================
-- Custom Keybindings
-- ==========================================
o.bind("SUPER + L", "Lock Screen", "omarchy-lock-screen")
o.bind("SUPER + SHIFT + L", "Suspend System", "~/Scripts/system/lock_and_suspend.sh")
o.bind("SUPER + ALT + L", "Restart System", "systemctl reboot")
o.bind("SUPER + ALT + SHIFT + L", "Shutdown System", "systemctl poweroff")
o.bind("SUPER + C", "VS Code", "code")
o.bind("SUPER + SHIFT + C", "Cursor", "cursor")
o.bind("SUPER + CTRL + C", "Kiro IDE", "uwsm app -- kiro")

hl.unbind("SUPER + Q")
o.bind("SUPER + Q", "Close Window", 'hyprctl dispatch killactive ""')

o.bind("SUPER + SHIFT + T", "OCR to Clipboard", "~/Scripts/system/ocr_to_clipboard.sh")
o.bind("SUPER + ALT + T", "OCR Japanese to Clipboard", "~/Scripts/system/ocr_to_clipboard_jpn.sh")
o.bind("SUPER + S", "Screen snip", "pidof slurp || hyprshot --freeze --clipboard-only --mode region --silent")

-- Recording
o.bind("SUPER + ALT + R", "Record region (no sound)", "~/Scripts/system/record.sh")
o.bind("SUPER + SHIFT + R", "Record region (with sound)", "~/Scripts/system/record.sh --sound")
o.bind("SUPER + SHIFT + ALT + R", "Record screen (with sound)", "~/Scripts/system/record.sh --fullscreen-sound")
o.bind("SUPER + CTRL + R", "Reload Hyprland", "hyprctl reload")

-- Apps & Environments
hl.unbind("SUPER + J")
o.bind("SUPER + J", "Anki", "uwsm app -- anki")
o.bind("SUPER + SHIFT + J", "Xournal", "omarchy-launch-or-focus xournalpp")
o.bind("SUPER + V", "Python VENV", "uwsm app -- $TERMINAL -e bash -c 'cd ~/venv && source bin/activate && exec $SHELL'")
o.bind("SUPER + SHIFT + V", "Pysean VENV", "uwsm app -- $TERMINAL -e bash -c '~/Scripts/system/launch_pysean.sh'")
o.bind("SUPER + ALT + V", "Scripts VENV", "uwsm app -- $TERMINAL -e bash -c 'cd ~/Scripts && source ~/venv/bin/activate && exec $SHELL'")
o.bind("SUPER + G", "GitHub Profile", 'omarchy-launch-browser "https://github.com/evilusean"')
o.bind("SUPER + SHIFT + G", "GitHub Desktop", "omarchy-launch-or-focus github-desktop")

-- Zoom
o.bind("SUPER + EQUAL", "Zoom In", "~/Scripts/zoom.sh increase 0.1")
o.bind("SUPER + MINUS", "Zoom Out", "~/Scripts/zoom.sh decrease 0.1")

-- Move active window to a specific workspace and follow (Super + Alt + Number)
o.bind("SUPER + ALT + 1", "Move to workspace 1", "hyprctl dispatch movetoworkspace 1 && hyprctl dispatch workspace 1")
o.bind("SUPER + ALT + 2", "Move to workspace 2", "hyprctl dispatch movetoworkspace 2 && hyprctl dispatch workspace 2")
o.bind("SUPER + ALT + 3", "Move to workspace 3", "hyprctl dispatch movetoworkspace 3 && hyprctl dispatch workspace 3")
o.bind("SUPER + ALT + 4", "Move to workspace 4", "hyprctl dispatch movetoworkspace 4 && hyprctl dispatch workspace 4")
o.bind("SUPER + ALT + 5", "Move to workspace 5", "hyprctl dispatch movetoworkspace 5 && hyprctl dispatch workspace 5")
o.bind("SUPER + ALT + 6", "Move to workspace 6", "hyprctl dispatch movetoworkspace 6 && hyprctl dispatch workspace 6")
o.bind("SUPER + ALT + 7", "Move to workspace 7", "hyprctl dispatch movetoworkspace 7 && hyprctl dispatch workspace 7")
o.bind("SUPER + ALT + 8", "Move to workspace 8", "hyprctl dispatch movetoworkspace 8 && hyprctl dispatch workspace 8")
o.bind("SUPER + ALT + 9", "Move to workspace 9", "hyprctl dispatch movetoworkspace 9 && hyprctl dispatch workspace 9")
