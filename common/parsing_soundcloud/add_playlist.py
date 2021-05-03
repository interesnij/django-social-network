import soundcloud
from music.models import *
from datetime import datetime, date, time
import json, requests


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')


def add_playlist(url, request_user, list):
    response = requests.get(url= "https://api.soundcloud.com/resolve?url=" + url + "&client_id=dce5652caa1b66331903493735ddd64d")
    data = response.json()

    if data:
        try:
            playlist_url = data['artwork_url'].replace("large.jpg", "crop.jpg")
            list.get_remote_image(playlist_url)
        except:
            pass
        for track in data['tracks']:
            created = track['created_at']
            created = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

            if track['description']:
                description = track['description'][:500]
            else:
                description = None

            if track['genre'] and track['duration'] > 9000:
                track_genre = track['genre'].replace("'", '')
                try:
                    genre = SoundGenres.objects.get(name=track_genre)
                except:
                    genre = SoundGenres.objects.create(name=track_genre)
                new_track = Music.objects.create(created=created,
                                                        description=description,
                                                        duration=track['duration'],
                                                        genre=genre,
                                                        title=track['title'],
                                                        uri=track['uri'])
                try:
                    new_track.get_remote_image(track['artwork_url'])
                except:
                    pass
                list.players.add(new_track)
