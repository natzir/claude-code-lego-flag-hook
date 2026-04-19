#!/usr/bin/env python3
"""Move the Lego mailbox flag. Usage: notify-arduino.py [U|D|W]"""
import glob
import sys
import time
from pathlib import Path

PORT_GLOBS = [
    "/dev/cu.usbserial-*",
    "/dev/cu.wchusbserial*",
    "/dev/cu.SLAB_USBtoUART*",
    "/dev/cu.usbmodem*",
]
BAUD = 9600
BOOT_WAIT = 2.2
LOG = Path("/tmp/notify-arduino.log")


def log(msg: str) -> None:
    with LOG.open("a") as f:
        f.write(f"{time.strftime('%F %T')} {msg}\n")


try:
    import serial
except ImportError:
    log("pyserial missing — run: /usr/bin/python3 -m pip install --user pyserial")
    sys.exit(0)

cmd_char = sys.argv[1][0].upper() if len(sys.argv) > 1 else "W"
if cmd_char not in ("U", "D", "W"):
    log(f"ignored command: {cmd_char!r}")
    sys.exit(0)

ports: list[str] = []
for pattern in PORT_GLOBS:
    ports.extend(glob.glob(pattern))

if not ports:
    log(f"no serial port matching {PORT_GLOBS}")
    sys.exit(0)

for port in ports:
    try:
        with serial.Serial(port, BAUD, timeout=1) as s:
            time.sleep(BOOT_WAIT)
            s.reset_input_buffer()
            s.write(cmd_char.encode())
            s.flush()
            time.sleep(0.1)
        log(f"sent {cmd_char} to {port}")
        sys.exit(0)
    except Exception as e:
        log(f"serial error on {port}: {e}")

log(f"all ports failed: {ports}")
sys.exit(0)
