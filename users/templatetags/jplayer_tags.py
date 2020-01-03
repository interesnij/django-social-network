from django import template
from music.models import Playlist
register = template.Library()


@register.filter
def render_jplayer(context, player):
    all_track_playlist = Playlist.objects.get(id=1)
    return {'player': all_track_playlist}
