# Roblox Aura and Biome detection (TUI)

Monitor Sober Roblox logs for changes in Rich Presence (Aura and Biome).
Listens to latest.log, parses SetRichPresence messages, and prints when
the Aura (data.state) or Biome (data.largeImage.hoverText) changes.

## To run:
cd ~/.var/app/org.vinegarhq.Sober/data/sober/sober_logs/
./sober_monitor.py

## LICENSE: MIT
