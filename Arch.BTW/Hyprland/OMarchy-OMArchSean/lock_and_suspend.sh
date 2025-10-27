#!/bin/bash

# 1. Lock the session asynchronously and disown the process.
# This runs the lock screen in the background.
omarchy-lock-screen &
LOCK_PID=$!

# 2. Wait a moment (adjust if necessary) for the lock screen to initialize.
sleep 1

# 3. Suspend the system.
systemctl suspend
