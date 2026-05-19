### Hard Drive Encryption Guide (LUKS + ext4)

#### 1. Preparation
* **Identify Drive:** Use `lsblk` to find the correct device (e.g., `/dev/sdX1`).
* **Unmount:** Ensure the partition is not in use:
    ```bash
    udisksctl unmount -b /dev/sdX1
    ```

#### 2. Encryption Process
* **Format with LUKS:** Initialize the encryption layer.
    ```bash
    sudo cryptsetup luksFormat /dev/sdX1
    ```
    *(Type 'YES' in caps and set a strong passphrase)*

* **Open Container:** Map the encrypted partition to a virtual device.
    ```bash
    sudo cryptsetup open /dev/sdX1 external_crypt
    ```

* **Create Filesystem:** Format the internal virtual device to ext4.
    ```bash
    sudo mkfs.ext4 /dev/mapper/external_crypt
    ```

#### 3. Set Permissions
* **Mount and Chown:** Mount the drive manually once to set user ownership so `sudo` isn't required for file transfers.
    ```bash
    sudo mkdir -p /mnt/encrypted
    sudo mount /dev/mapper/external_crypt /mnt/encrypted
    sudo chown -R $USER:$USER /mnt/encrypted
    ```

#### 4. Future Usage (Hyprland/Omarchy)
* **GUI Access:** Simply plug the drive in. Your file manager (Thunar/Dolphin) will show a locked icon. Click it and enter your passphrase when prompted.
* **CLI Unlocking:**
    ```bash
    # To Open
    sudo cryptsetup open /dev/sdX1 external_crypt
    sudo mount /dev/mapper/external_crypt /mnt/mountpoint

    # To Close
    sudo umount /mnt/mountpoint
    sudo cryptsetup close external_crypt
    ```

#### Important Commands
* **Reclaim Reserved Space:** `sudo tune2fs -m 0 /dev/mapper/external_crypt` (Gain ~45GB back on 1TB drives).
* **Check Status:** `sudo cryptsetup status external_crypt`
