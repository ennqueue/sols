

Copyright 2026 ennqueue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:



#!/usr/bin/env python3
"""
Roblox Aura and Biome detection (TUI)

Monitor Sober Roblox logs for changes in Rich Presence (Aura and Biome).
Listens to latest.log, parses SetRichPresence messages, and prints when
the Aura (data.state) or Biome (data.largeImage.hoverText) changes.

To run:
cd ~/.var/app/org.vinegarhq.Sober/data/sober/sober_logs/
./sober_monitor.py

"""

import json
import subprocess
import sys
import time

LOG_FILE = "latest.log"  # latest log file of sober

def extract_fields(line: str):
    """Return (aura, biome) if line is a valid SetRichPresence, else return None"""
    marker = "[BloxstrapRPC] "
    if marker not in line:
        return None

    json_start = line.index(marker) + len(marker)
    json_str = line[json_start:].strip()
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return None

    if data.get("command") != "SetRichPresence":
        return None

    rpc_data = data.get("data", {})
    aura = rpc_data.get("state", "?")
    large_image = rpc_data.get("largeImage", {})
    biome = large_image.get("hoverText", "?")

    return aura, biome

def main():
    print("Monitoring Sober Rich Presence (Aura / Biome)")
    print("Press Ctrl+C to stop.\n")

    last_aura = None
    last_biome = None

    # Use tail -F to follow the file
    proc = subprocess.Popen(
        ["tail", "-F", LOG_FILE],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )

    try:
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue

            result = extract_fields(line)
            if result is None:
                continue

            aura, biome = result

            # Check for changes and print
            changed = False
            if aura != last_aura:
                print(f"Aura  changed: {aura}")
                last_aura = aura
                changed = True
            if biome != last_biome:
                print(f"Biome changed: {biome}")
                last_biome = biome
                changed = True

    except KeyboardInterrupt:
        print("\nExiting.")
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    main()
