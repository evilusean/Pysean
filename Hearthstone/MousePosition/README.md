# mouse_position.py

Simple script that reads the current mouse cursor position and prints it to stdout.

Requirements
- Python 3.6+
- pynput

Install

```bash
pip install -r requirements.txt
```

Usage

```bash
# continuous print (every 0.1s)
python3 mouse_position.py

# one-shot
python3 mouse_position.py --one-shot

# custom interval and format
python3 mouse_position.py -i 0.2 -f "x={x},y={y}"

# append to logfile
python3 mouse_position.py -l positions.log
```

Notes
- Ctrl-C stops continuous printing.
- Works on Linux, macOS, and Windows (requires X display on Linux).
