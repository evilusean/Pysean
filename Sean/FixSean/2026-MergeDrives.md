# Storage Consolidation: Merging sdb2 and sdb3
- **Goal:** Expand sdb2 (ZZZ) to 500GB by absorbing sdb3.
- **Tools:** GNOME Disks (Unmounting) & GParted (Partitioning).
- **Condition:** sdb2 and sdb3 must be physically adjacent on the disk map.

---

### Step 0: Slow process of moving all the files over to sdb2
Over 100 gigs of files, hours where I can't do anything else but this, can't stream video or take notes because laptop is working hard, no trig today.
going to make a bigger drive because any game I want to download and play that is over 100gigs(any modern game) needs 200 gigs to install because of zip files and unpack

---
### Step 1: Safe Unmounting (GNOME Disks)
Before modifying partitions, the system must release the "lock" on the drives.
1. Open **GNOME Disks**.
2. Select the **1TB Hard Drive** in the left sidebar.
3. Click on the **sdb2** partition block -> Click the **Square (Stop)** button to unmount.
4. Click on the **sdb3** partition block -> Click the **Square (Stop)** button to unmount.
*Note: If the Square button is greyed out, the drive is already unmounted.*

---

#### Step 2: The GParted Merge Process
1. **Launch GParted:**
   `sudo gparted`
2. **Select Device:** Ensure `/dev/sdb` is selected in the top-right dropdown.
3. **Delete the Sacrifice:** - Right-click **sdb3** (the empty/old library).
   - Select **Delete**. It becomes "Unallocated" space.
4. **Expand the Survivor:**
   - Right-click **sdb2** (your active games drive).
   - Select **Resize/Move**.
   - Drag the right-hand slider all the way to the end of the grey bar.
   - Click **Resize/Move**.
5. **Commit:** Click the **Checkmark (Apply)** icon in the toolbar.

---

#### Step 3: Post-Merge Verification & Mounting
Once GParted finishes, you need to refresh the system's view of the drive.
1. **Mount the new 500GB volume:**
   `sudo mount /dev/sdb2 /mnt/sdb2`
2. **Verify Space:**
   `df -h | grep sdb2`
3. **Update UUID (Optional but Recommended):**
   If you use `/etc/fstab`, ensure the UUID hasn't changed (though resizing usually preserves it):
   `lsblk -f`

---

#### Step 4: Maintenance Commands
- **Check for Errors:** `sudo e2fsck -f /dev/sdb2`
- **Permissions Fix:** `sudo chown -R $USER:$USER /mnt/sdb2`
- **Force Library Scan:** Restart Steam to allow it to recognize the expanded capacity.
