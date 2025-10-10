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
