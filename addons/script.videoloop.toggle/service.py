#!/usr/bin/env python3
"""
Video Loop Toggle - Background Service

Monitors the Kodi player repeat state and keeps the skin property
'videoloop.enabled' in sync. This ensures the OSD icon reflects the
actual state even when repeat is changed externally (e.g. via
StreamDeck calling Player.SetRepeat directly through JSON-RPC).
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


def update_skin_property(enabled):
    """Update the skin property used by VideoOSD.xml for icon visibility."""
    window = xbmcgui.Window(10000)
    if enabled:
        window.setProperty("videoloop.enabled", "true")
    else:
        window.clearProperty("videoloop.enabled")


class VideoLoopService:
    """Background service that syncs repeat state with skin property."""

    def __init__(self):
        self.monitor = xbmc.Monitor()
        self.last_state = "off"

    def run(self):
        xbmc.log("VideoLoop: service started", xbmc.LOGINFO)

        # Start with loop off
        update_skin_property(False)

        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(2):
                break

            player_id = get_active_video_player_id()
            if player_id is not None:
                state = get_repeat_state(player_id)
                enabled = state != "off"

                if state != self.last_state:
                    update_skin_property(enabled)
                    xbmc.log(
                        f"VideoLoop: state changed to {state}",
                        xbmc.LOGDEBUG
                    )
                    self.last_state = state
            else:
                # No video playing - reset state
                if self.last_state != "off":
                    update_skin_property(False)
                    self.last_state = "off"

        xbmc.log("VideoLoop: service stopped", xbmc.LOGINFO)


if __name__ == "__main__":
    service = VideoLoopService()
    service.run()
