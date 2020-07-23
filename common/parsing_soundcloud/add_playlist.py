import soundcloud
from music.models import *
from datetime import datetime, date, time


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]



def load_playlist(permalink_url, request_user, list):

    tracks = client.get('/tracks', permalink_url=permalink_url)
    if tracks:
        for track in tracks:
            created_at = track.created_at
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            if track.description:
                description = track.description[:500]
            else:
                description = None
            if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                new_track = SoundcloudParsing.objects.create(id=track.id,
                                                            artwork_url=track.artwork_url,
                                                            created_at=created_at,
                                                            description=description,
                                                            duration=track.duration,
                                                            genre=genre,
                                                            title=track.title,
                                                            uri=track.uri,
                                                            release_year=track.release_year,
                                                            list=list)
