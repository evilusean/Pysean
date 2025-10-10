## 🛠️ Complete Wacom Intuos BT M Bluetooth & Stylus Fix Guide

This guide resolves the aggressive Bluetooth idle timeout and ensures the stylus is properly recognized by the Wacom driver on Arch Linux.

### Step 1: Fix Bluetooth Idle Timeout (Stability)

This step sets a long idle timeout (30 minutes) for the general Human Interface Device (HID) layer, preventing the Wacom tablet from disconnecting when the pen is lifted.

1.  **Create a kernel module configuration file:**
    ```bash
    sudo nano /etc/modprobe.d/wacom-bluetooth-fix.conf
    ```

2.  **Add the following content** to the file:
    ```conf
    # Set the general HID timeout to 30 minutes (1800 seconds) to prevent Wacom BT disconnects.
    options hid_core idle_timeout=1800
    ```

3.  **Save and exit** (Ctrl+O, Enter, Ctrl+X in Nano).

----------------------------------------------------------------------------------------------------------------------------------------------------------------

### Step 2: Install Essential Wacom Drivers and Utilities

Ensure the latest userspace drivers and necessary input utilities are installed for proper device claiming.

1.  **Install the essential packages:**
    ```bash
    sudo pacman -S xorg-xinput xf86-input-wacom
    ```

----------------------------------------------------------------------------------------------------------------------------------------------------------------

### Step 3: Apply Changes and Reboot

1.  **Rebuild the initial ramdisk (initramfs)** to incorporate the new kernel module parameter:
    ```bash
    sudo mkinitcpio -P
    ```

1.5 : Manually load the Wacom kernel module: This forces the kernel to load the module, which should then scan for connected Wacom devices (like your Bluetooth tablet) and claim them.
    ```bash
    sudo modprobe wacom
    ```

2.  **Reboot your system** to load the kernel modules with the new configuration:
    ```bash
    reboot
    ```

----------------------------------------------------------------------------------------------------------------------------------------------------------------

### Step 4: Verification

After rebooting, the tablet should be stable and functional.

1.  **Verify Stylus Recognition:** Check the device list (you should see 'xwayland-tablet stylus' if using Wayland, or 'Wacom Intuos BT M Pen' if using native Xorg):
    ```bash
    xinput list
    ```

2.  **Test Live Input:** If the stylus ID is, for example, '10', use:
    ```bash
    xinput test 10
    ```
    Moving the pen should now produce a stream of position and pressure data.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

# Wacom Intuos BT M Pad Mapping Fix for Xournal++

This guide assumes 'input-remapper-git' is installed on Arch Linux and the daemon fails to start automatically. The fix addresses three main issues: macro syntax, user/root configuration path conflicts, and systemd service file errors.

## I. Fix Xournal++ Macro Syntax

The GUI fails to properly record complex hotkeys (like Shift+Ctrl+E). You must manually enter the hotkeys in the GUI using the specific human-readable format `Key_Side + Key_Side + letter`.

### A. Xournal++ Hotkeys to Map:
| Action | Xournal++ Hotkey | Input Remapper Output (Manual Entry) |
| :--- | :--- | :--- |
| **Eraser** | Shift+Ctrl+E | `Shift_L + Control_L + e` |
| **Pen** | Shift+Ctrl+P | `Shift_L + Control_L + p` |
| **Grab/Hand** | Shift+Ctrl+A | `Shift_L + Control_L + a` |
| **Undo** | Ctrl+Z | `Control_L + z` |

### B. Verification (Editing the JSON)
To confirm or manually fix a malformed file:
1.  Open the configuration file:
    ```bash
    nano /home/ArchSean/.config/input-remapper-2/config.json
    ```
2.  Locate your mappings and ensure the `output_symbol` value matches the required format (e.g., `"Shift_L + Control_L + e"`).
3.  Save and close the file.

---

## II. Fix Daemon Startup (System Service)

Since the `input-remapper-service` binary is limited and runs as root, we must ensure it can find and read the configuration file from your user's home directory.

### A. Create Symlink for Root Access
This links your user's config file to the location the root daemon expects (`/root/.config/...`).

1.  Stop the service:
    ```bash
    sudo systemctl stop input-remapper.service
    ```
2.  Create the necessary root directory:
    ```bash
    sudo mkdir -p /root/.config/input-remapper-2
    ```
3.  Create the symbolic link:
    ```bash
    sudo ln -s /home/ArchSean/.config/input-remapper-2/config.json /root/.config/input-remapper-2/config.json
    ```

### B. Fix the System Service File
We must ensure the service file is restored to its original state (no arguments), as the binary does not support `--dir` or `--config`.

1.  Edit the service file:
    ```bash
    sudo nano /usr/lib/systemd/system/input-remapper.service
    ```
2.  Ensure the `ExecStart` line under `[Service]` is the original, simple command:
    ```ini
    ExecStart=/usr/bin/input-remapper-service
    ```
3.  Save and exit.

### C. Final Service Reload and Restart
```bash
sudo systemctl daemon-reload
sudo systemctl restart input-remapper.service
```
```bash
# This step is what was required to make the keys work.
input-remapper-gtk
# Inside the GUI, click the 'Apply' button to force the daemon to start and read the config.
```
