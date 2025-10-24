#!/usr/bin/env bash

# The actual VENV launch command
cd ~/venv && source bin/activate

# Replace the current process with an interactive shell
exec "$SHELL"
