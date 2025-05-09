#!/bin/bash
#should open the keyboard and close it if pressed again

PID=$(pgrep -x wvkbd-mobintl)

if [ -n "$PID" ]; then
    kill "$PID" # Terminate the wvkbd process
else
    /usr/bin/wvkbd-mobintl # Launch wvkbd
fi
