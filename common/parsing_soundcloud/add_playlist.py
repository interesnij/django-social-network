import soundcloud
from music.models import *
from datetime import datetime, date, time
import json, requests
from PIL import Image


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')


def add_playlist(url, request_user, list):
    response = requests.get(url= "https://api.soundcloud.com/resolve?url=" + url + "&client_id=dce5652caa1b66331903493735ddd64d")
    data = response.json()

    if data:
        try:
            playlist_url = data['artwork_url']
            playlist_url.replace("large.jpg", "crop.jpg")
            img_response = requests.get(url=playlist_url)
            img = Image.open(img_response)
            list.image = img
            list.save(update_fields=["image"])
        except:
            pass
        for track in data['tracks']:
            created_at = track['created_at']
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

            if track['description']:
                description = track['description'][:500]
            else:
                description = None

            if track['genre'] and track['duration'] > 9000:
                track_genre = track['genre'].replace("'", '')
                try:
                    genre = SoundGenres.objects.get(name=track_genre)
                except:
                    genre = SoundGenres.objects.create(name=track_genre, order=SoundGenres.get_new_order())

                new_track = SoundcloudParsing.objects.create(artwork_url=track['artwork_url'],
                                                        created_at=created_at,
                                                        description=description,
                                                        duration=track['duration'],
                                                        genre=genre,
                                                        title=track['title'],
                                                        uri=track['uri'],
                                                        release_year=track['release_year'])
                list.players.add(new_track)
