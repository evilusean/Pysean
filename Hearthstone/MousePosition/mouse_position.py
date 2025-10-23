#!/usr/bin/env python3
"""
mouse_position.py
Simple cross-platform mouse position detector using pynput.

Usage:
  python3 mouse_position.py            # prints coordinates continuously
  python3 mouse_position.py -i 0.2     # print every 0.2s
  python3 mouse_position.py --one-shot # print one position and exit
  python3 mouse_position.py -l out.log # append coords to out.log

Outputs formatted lines like: "100 200" (default). Use -f/--format to change output.
"""

import argparse
import time
import sys
try:
    from pynput.mouse import Controller
except Exception:
    Controller = None


def parse_args():
    p = argparse.ArgumentParser(description="Print current mouse position using pynput.")
    p.add_argument('-i','--interval', type=float, default=0.1, help='Polling interval in seconds (default: 0.1)')
    p.add_argument('-o','--one-shot', action='store_true', dest='one_shot', help='Print one position then exit')
    p.add_argument('-f','--format', default='{x} {y}', help='Output format using {x} and {y} placeholders (default: "{x} {y}")')
    p.add_argument('-l','--logfile', default=None, help='Optional file to append coordinates to')
    return p.parse_args()


def main():
    args = parse_args()
    if Controller is None:
        print("pynput not available. Please install requirements.txt (pip install -r requirements.txt)", file=sys.stderr)
        sys.exit(2)

    mouse = Controller()
    out = None
    if args.logfile:
        try:
            out = open(args.logfile, 'a')
        except Exception as e:
            print(f"Failed to open logfile '{args.logfile}': {e}", file=sys.stderr)
            sys.exit(2)

    try:
        while True:
            pos = mouse.position
            # pos might be a tuple or Point-like
            try:
                x, y = pos
            except Exception:
                x = getattr(pos, 'x', None)
                y = getattr(pos, 'y', None)
            line = args.format.format(x=x, y=y)
            print(line, flush=True)
            if out:
                out.write(line + "\n")
                out.flush()
            if args.one_shot:
                break
            time.sleep(max(0.001, args.interval))
    except KeyboardInterrupt:
        # graceful stop on Ctrl-C
        pass
    finally:
        if out:
            out.close()


if __name__ == '__main__':
    main()
