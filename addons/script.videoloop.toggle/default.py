#!/usr/bin/env python3
"""
Video Loop Toggle - toggles single-video repeat on/off.

Entry points:
  - OSD button (RunScript)
  - Keyboard shortcut ('L' key via keymap)
  - JSON-RPC: Addons.ExecuteAddon("script.videoloop.toggle")
  - JSON-RPC: Player.SetRepeat (direct Kodi API, no addon needed)
"""

import json
import xbmc
import xbmcgui


def get_active_video_player_id():
    """Return the player ID of the active video player, or None."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.GetActivePlayers",
        "id": 1
    })
    response = json.loads(xbmc.executeJSONRPC(request))
    for player in response.get("result", []):
        if player.get("type") == "video":
            return player["playerid"]
    return None


def get_repeat_state(player_id):
    """Return current repeat state: 'off', 'one', or 'all'."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.GetProperties",
        "params": {"playerid": player_id, "properties": ["repeat"]},
        "id": 1
    })
    response = json.loads(xbmc.executeJSONRPC(request))
    return response.get("result", {}).get("repeat", "off")


def set_repeat_state(player_id, state):
    """Set repeat state to 'off', 'one', or 'all'."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "method": "Player.SetRepeat",
        "params": {"playerid": player_id, "repeat": state},
        "id": 1
    })
    xbmc.executeJSONRPC(request)


def update_skin_property(enabled):
    """Update the skin property used by VideoOSD.xml for icon visibility."""
    window = xbmcgui.Window(10000)  # Home window
    if enabled:
        window.setProperty("videoloop.enabled", "true")
    else:
        window.clearProperty("videoloop.enabled")


def toggle_loop():
    """Toggle video loop on/off for the currently playing video."""
    player_id = get_active_video_player_id()
    if player_id is None:
        xbmcgui.Dialog().notification(
            "Video Loop",
            "No video playing",
            xbmcgui.NOTIFICATION_WARNING,
            2000
        )
        return

    current = get_repeat_state(player_id)

    if current == "off":
        set_repeat_state(player_id, "one")
        update_skin_property(True)
        xbmcgui.Dialog().notification(
            "Video Loop",
            "Loop ON",
            xbmcgui.NOTIFICATION_INFO,
            2000
        )
        xbmc.log("VideoLoop: repeat set to ONE", xbmc.LOGINFO)
    else:
        set_repeat_state(player_id, "off")
        update_skin_property(False)
        xbmcgui.Dialog().notification(
            "Video Loop",
            "Loop OFF",
            xbmcgui.NOTIFICATION_INFO,
            2000
        )
        xbmc.log("VideoLoop: repeat set to OFF", xbmc.LOGINFO)


if __name__ == "__main__":
    toggle_loop()
