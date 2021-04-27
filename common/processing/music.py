def get_music_processing(music, status):
    music.status = status
    music.save(update_fields=['status'])
    return music
def get_playlist_processing(playlist, status):
    playlist.type = status
    playlist.save(update_fields=['type'])
    return playlist
