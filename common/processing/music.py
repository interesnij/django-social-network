def get_music_processing(music, type):
    music.type = type
    music.save(update_fields=['type'])
    return music
def get_playlist_processing(playlist, type):
    playlist.type = type
    playlist.save(update_fields=['type'])
    return playlist
