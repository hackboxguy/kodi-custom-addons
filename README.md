# kodi-custom-addons

A meta-layer package for adding custom functionality to vanilla Kodi installations on Raspberry Pi. Designed to work with [custom-pi-imager](https://github.com/hackboxguy/misc-tools) SD card image builder.

## Included Addons

### Video Loop Toggle (`script.videoloop.toggle`)

Adds a loop on/off toggle button to the Kodi video player OSD for single-file repeat playback.

**Features:**
- **OSD toggle button** - Loop icon in the video player OSD button bar (red=off, green=on)
- **Keyboard shortcut** - Press `L` during video playback to toggle
- **API control** - Toggle via JSON-RPC on port 8080 (e.g. from Elgato StreamDeck)
- **State sync** - Background service keeps OSD icon in sync with actual repeat state
- **Pre-configured** - Addon auto-enabled, Kodi web server enabled out of the box

## Installation via custom-pi-imager

Add this line to your packages list (e.g. `micropanel-packages.txt`):

```
packages/kodi-custom-addons-hook.sh|https://github.com/hackboxguy/kodi-custom-addons.git|main|/home/pi/kodi-custom-addons
```

The hook script must be copied to your `custom-pi-imager/packages/` directory, or referenced with a relative path.

### What the hook installs

| Step | What | Where |
|------|------|-------|
| 1 | Clone this repo | `/tmp` (build only) |
| 2 | Addon files | `~/.kodi/addons/script.videoloop.toggle/` |
| 3 | Patched Estuary skin + icons | `~/.kodi/addons/skin.estuary/` |
| 4 | Keymap (`L` key) | `~/.kodi/userdata/keymaps/videoloop.xml` |
| 5 | guisettings.xml (web server enabled) | `~/.kodi/userdata/guisettings.xml` |
| 6 | Addons33.db (addon pre-enabled) | `~/.kodi/userdata/Database/Addons33.db` |
| 7 | Source copy for reference | `/home/pi/kodi-custom-addons/` |

## API Usage (StreamDeck / External Control)

Kodi's HTTP JSON-RPC is pre-enabled on port 8080 with no authentication.

### Direct Kodi JSON-RPC

```bash
# Enable loop (single file repeat)
curl -s http://<pi-ip>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Player.SetRepeat","params":{"playerid":1,"repeat":"one"},"id":1}'

# Disable loop
curl -s http://<pi-ip>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Player.SetRepeat","params":{"playerid":1,"repeat":"off"},"id":1}'

# Cycle (off -> one -> all -> off)
curl -s http://<pi-ip>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Player.SetRepeat","params":{"playerid":1,"repeat":"cycle"},"id":1}'
```

### Via addon (toggles off/one)

```bash
curl -s http://<pi-ip>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Addons.ExecuteAddon","params":{"addonid":"script.videoloop.toggle"},"id":1}'
```

The background service polls every 2 seconds, so the OSD icon reflects the current state regardless of which method is used to change it.

## File Structure

```
kodi-custom-addons/
├── addons/
│   └── script.videoloop.toggle/
│       ├── addon.xml                 # Addon manifest
│       ├── default.py                # Toggle script (off <-> one)
│       ├── service.py                # Background state monitor
│       ├── guisettings.xml           # Pre-configured Kodi settings (web server enabled)
│       ├── loop-off.png              # OSD icon: loop disabled (red)
│       ├── loop-on.png               # OSD icon: loop enabled (green)
│       ├── tmp/                      # Source BMP icons (for reference)
│       └── resources/keymaps/
│           └── videoloop.xml         # 'L' key binding
├── db/
│   └── Addons33.db                   # Pre-built Kodi addons database (addon enabled)
├── skin-patches/
│   └── VideoOSD.xml                  # Patched Estuary OSD with loop button
└── packages/
    └── kodi-custom-addons-hook.sh    # Hook script for custom-pi-imager
```

## Installed Paths on Pi

```
~/.kodi/addons/script.videoloop.toggle/              # Addon files
~/.kodi/addons/skin.estuary/xml/VideoOSD.xml         # Patched OSD
~/.kodi/addons/skin.estuary/media/osd/fullscreen/buttons/loop-*.png  # Icons
~/.kodi/userdata/guisettings.xml                     # Kodi settings (web server)
~/.kodi/userdata/keymaps/videoloop.xml               # Key binding
~/.kodi/userdata/Database/Addons33.db                # Addons database
```

## Notes

- The `Addons33.db` and `guisettings.xml` are captured from a working Kodi installation on Raspberry Pi OS Bookworm. Creating these files from scratch does not work due to Kodi's complex database schema and settings format.
- If the Kodi version changes significantly, these files may need to be recaptured from a fresh installation.
- The `tmp/` directory contains the original BMP source icons used to generate the PNG icons.
