#!/usr/bin/env python3
"""Navigation helpers for the KyuuyakuTen debug build.

The script talks to the TCP debug server on port 4377. It is intentionally
small: the goal is to make movement reproducible while probing Mikon City.

Observed state (2026-11-17):
  0x877  x
  0x878  y
  0x80f  facing: 0=N, 1=E, 2=S, 3=W
  0x811  forward-move counter
  0x813  turn counter
  0x865  area/room id
  0x867  view/background id (direction dependent)

Controls observed: up = forward, left/right = 90-degree turn. Down can behave
as a 180-degree turn in some states, so the helpers use left/right for turns.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "snesrecomp" / "tools"))

from sneslib.client import DebugClient  # noqa: E402

FACING = {0: "N", 1: "E", 2: "S", 3: "W"}
DIRS = {"N": 0, "E": 1, "S": 2, "W": 3}


def u8(client: DebugClient, addr: int) -> int:
    raw = client.query(f"read_ram {addr:x} 1")["hex"].split()
    return int(raw[0], 16)


def u16(client: DebugClient, addr: int) -> int:
    raw = client.query(f"read_ram {addr:x} 2")["hex"].split()
    return int(raw[0], 16)


def state(client: DebugClient) -> dict:
    return {
        "x": u8(client, 0x877),
        "y": u8(client, 0x878),
        "facing": u8(client, 0x80F),
        "move": u16(client, 0x811),
        "turn": u16(client, 0x813),
        "area": u16(client, 0x865),
        "view": u16(client, 0x867),
    }


def show_state(client: DebugClient, label: str = "") -> dict:
    s = state(client)
    prefix = f"{label}: " if label else ""
    print(
        f"{prefix}x={s['x']} y={s['y']} facing={FACING.get(s['facing'], '?')} "
        f"area=0x{s['area']:04x} view=0x{s['view']:04x} "
        f"move={s['move']} turn={s['turn']}",
        flush=True,
    )
    return s


def press(client: DebugClient, button: str, hold: int = 8, wait: int = 70) -> None:
    client.query(f"set_controller {button}", retry=False)
    client.query(f"step {hold}", retry=False)
    client.query("clear_controller", retry=False)
    client.query(f"step {wait}", retry=False)


def face(client: DebugClient, target: int, retries: int = 8) -> bool:
    for _ in range(retries):
        cur = u8(client, 0x80F)
        if cur == target:
            return True
        delta = (target - cur) % 4
        if delta == 1:
            press(client, "right", 8, 55)
        elif delta == 3:
            press(client, "left", 8, 55)
        else:
            press(client, "left", 8, 55)
    return u8(client, 0x80F) == target


def forward_once(client: DebugClient) -> bool:
    before = (u8(client, 0x877), u8(client, 0x878), u16(client, 0x865))
    press(client, "up", 8, 75)
    after = (u8(client, 0x877), u8(client, 0x878), u16(client, 0x865))
    return after != before


def forward(client: DebugClient, count: int = 1, retries: int = 3) -> int:
    moved = 0
    for _ in range(count):
        for _attempt in range(retries):
            if forward_once(client):
                moved += 1
                break
        else:
            break
    return moved


def turn_180(client: DebugClient) -> None:
    # Two left turns avoid the ambiguous down/back behaviour.
    press(client, "left", 8, 55)
    press(client, "left", 8, 55)


def open_automap(client: DebugClient) -> None:
    """Open the local auto-map: A -> COMP -> 5th item -> A."""
    press(client, "a", 8, 90)
    press(client, "a", 8, 120)
    for _ in range(4):
        press(client, "down", 8, 90)
    press(client, "a", 8, 120)


def close_menus(client: DebugClient, count: int = 4) -> None:
    for _ in range(count):
        press(client, "b", 8, 45)


def screenshot(client: DebugClient, name: str) -> None:
    client.query(f"screenshot {name}", retry=False)
    print(f"screenshot: {name}", flush=True)


def probe(client: DebugClient) -> None:
    """Try N/E/S/W, returning to the original cell after each successful move."""
    orig_face = u8(client, 0x80F)
    orig = (u8(client, 0x877), u8(client, 0x878), u16(client, 0x865))
    print(f"origin={orig} facing={FACING.get(orig_face)}", flush=True)
    for name, d in DIRS.items():
        if not face(client, d):
            print(f"{name}: could not face", flush=True)
            continue
        before = (u8(client, 0x877), u8(client, 0x878), u16(client, 0x865))
        press(client, "up", 8, 75)
        after = (u8(client, 0x877), u8(client, 0x878), u16(client, 0x865))
        moved = after != before
        print(f"{name}: {before} -> {after} moved={moved}", flush=True)
        if moved:
            face(client, (d + 2) % 4)
            press(client, "up", 8, 75)
            back = (u8(client, 0x877), u8(client, 0x878), u16(client, 0x865))
            print(f"  return={back} ok={back == before}", flush=True)
    face(client, orig_face)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4377)
    parser.add_argument("--loadstate", type=int, metavar="N")
    parser.add_argument("--state", action="store_true", help="print state and exit")
    parser.add_argument("--forward", type=int, metavar="N", default=0)
    parser.add_argument("--turn180", action="store_true")
    parser.add_argument("--face", choices=list(DIRS), metavar="N/E/S/W")
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--automap", action="store_true")
    parser.add_argument("--close-menus", action="store_true")
    parser.add_argument("--press", metavar="BUTTON")
    parser.add_argument("--screenshot", metavar="NAME")
    args = parser.parse_args()

    client = DebugClient(args.port, timeout=30)
    if not client.is_alive():
        print(f"debug server not responding on port {args.port}", file=sys.stderr)
        return 1

    client.query("clear_controller", retry=False)
    if args.loadstate is not None:
        print(client.query(f"loadstate {args.loadstate}", retry=False))
        client.query("step 20", retry=False)
    if args.close_menus:
        close_menus(client)
    if args.turn180:
        turn_180(client)
    if args.face:
        face(client, DIRS[args.face])
    if args.forward:
        print(f"moved {forward(client, args.forward)} cell(s)")
    if args.probe:
        probe(client)
    if args.automap:
        open_automap(client)
        for _ in range(8):
            client.query("step 10", retry=False)
    if args.press:
        press(client, args.press)
    if args.screenshot:
        screenshot(client, args.screenshot)
    if args.state or not any(
        [
            args.loadstate is not None,
            args.turn180,
            args.face,
            args.forward,
            args.probe,
            args.automap,
            args.close_menus,
            args.press,
            args.screenshot,
        ]
    ):
        show_state(client)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
