from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import json



def safe_json(data):
    return mark_safe(json(data))

class PlayerObject(dict):
    def __init__(self, playerid, playlist, autoplay, base_path, ogg_support):
        self.id = playerid
        self.playlist = playlist
        self.get_json_autoplay = autoplay
        self.get_base_path = base_path
        self.get_json_ogg_support = ogg_support
        self._cached_playlist = None

    def get_json_playlist(self):
        if self._cached_playlist is None:
            self._cached_playlist = safe_json(self.playlist)
        return self._cached_playlist

    def render(self, request):
        return render_jplayer(self, request)


def build_player(playerid, playlist, autoplay=True, base_path=settings.JPLAYER_BASE_PATH):
    def _get_ogg(songobj):
        try:
            return bool(songobj['ogg'])
        except (KeyError, TypeError):
            return hasattr(songobj, 'ogg') and bool(getattr(songobj, 'ogg', False))
    oggsupport = safe_json(all([_get_ogg(song) for song in playlist]))
    autoplay = safe_json(autoplay)
    base_path = safe_json(base_path)
    return PlayerObject(playerid, playlist, autoplay, base_path, oggsupport)

def render_jplayer(player_object, request):
    return render_to_string('base_block/player.html', {'player': player_object}, RequestContext(request))
