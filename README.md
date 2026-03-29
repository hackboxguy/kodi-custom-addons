# kodi-custom-addons

A meta-layer package for adding custom functionality to vanilla Kodi installations on Raspberry Pi. Designed to work with [custom-pi-imager](https://github.com/hackboxguy/misc-tools) SD card image builder.

## Included Addons

### Video Loop Toggle (`script.videoloop.toggle`)

Adds a loop on/off toggle button to the Kodi video player OSD for single-file repeat playback.

**Features:**
- **OSD toggle button** - Loop icon in the video player OSD button bar (gray=off, green=on)
- **Keyboard shortcut** - Press `L` during video playback to toggle
- **API control** - Toggle via JSON-RPC (e.g. from Elgato StreamDeck)
- **State sync** - Background service keeps OSD icon in sync with actual repeat state

## Installation via custom-pi-imager

Add this line to your packages list (e.g. `micropanel-packages.txt`):

```
packages/kodi-custom-addons-hook.sh|https://github.com/hackboxguy/kodi-custom-addons.git|main|/home/pi/kodi-custom-addons|sqlite3
```

The hook script must be copied to your `custom-pi-imager/packages/` directory, or reference it with the full path.

## API Usage (StreamDeck / External Control)

### Option 1: Direct Kodi JSON-RPC (no addon needed)

```bash
# Enable loop
curl -s -u kodi:kodi http://<host>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Player.SetRepeat","params":{"playerid":1,"repeat":"one"},"id":1}'

# Disable loop
curl -s -u kodi:kodi http://<host>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Player.SetRepeat","params":{"playerid":1,"repeat":"off"},"id":1}'

# Cycle (off -> one -> all -> off)
curl -s -u kodi:kodi http://<host>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Player.SetRepeat","params":{"playerid":1,"repeat":"cycle"},"id":1}'
```

### Option 2: Via addon (toggles off/one)

```bash
curl -s -u kodi:kodi http://<host>:8080/jsonrpc -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Addons.ExecuteAddon","params":{"addonid":"script.videoloop.toggle"},"id":1}'
```

Note: The background service updates the OSD icon every 2 seconds, so the icon reflects the state regardless of which method is used to change it.

## File Structure

```
kodi-custom-addons/
├── addons/
│   └── script.videoloop.toggle/
│       ├── addon.xml                 # Addon manifest
│       ├── default.py                # Toggle script (off <-> one)
│       ├── service.py                # Background state monitor
│       ├── loop-off.png              # OSD icon: loop disabled (gray)
│       ├── loop-on.png               # OSD icon: loop enabled (green)
│       └── resources/keymaps/
│           └── videoloop.xml         # 'L' key binding
├── skin-patches/
│   └── VideoOSD.xml                  # Patched Estuary OSD with loop button
└── packages/
    └── kodi-custom-addons-hook.sh    # Hook script for custom-pi-imager
```

## Installed Paths on Pi

```
~/.kodi/addons/script.videoloop.toggle/   # Addon files
~/.kodi/addons/skin.estuary/xml/VideoOSD.xml  # Patched OSD
~/.kodi/addons/skin.estuary/media/osd/fullscreen/buttons/loop-*.png  # Icons
~/.kodi/userdata/keymaps/videoloop.xml    # Key binding
```
