import soundcloud
from music.models import *
from datetime import datetime, date, time
import json, requests


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]


def load_playlist(url, request_user, list):
    response = requests.get(url= "https://api.soundcloud.com/resolve?url=" + url + "&client_id=dce5652caa1b66331903493735ddd64d")
    data = response.json()

    if data:
        for track in data['tracks']:
            created_at = track['created_at']
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

            if track['description']:
                description = track['description'][:500]
            else:
                description = None
            track_genre = track['genre'].replace("'", '')
            try:
                genre = SoundGenres.objects.get(name=track_genre)
            except:
                genre = SoundGenres.objects.create(name=track_genre, order=SoundGenres.get_new_order())
            try:
                new_track = SoundcloudParsing.objects.get(id=track['id'])
            except:
                new_track = SoundcloudParsing.objects.create(id=track['id'],
                                                        artwork_url=track['artwork_url'],
                                                        created_at=created_at,
                                                        description=description,
                                                        duration=track['duration'],
                                                        genre=genre,
                                                        title=track['title'],
                                                        uri=track['uri'],
                                                    release_year=track['release_year'])
            list.players.add(new_track)
