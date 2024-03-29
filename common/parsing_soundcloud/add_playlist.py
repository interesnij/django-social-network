import soundcloud
from music.models import *
from datetime import datetime, date, time
import json, requests


def add_playlist(_url, request_user, list):
    response = requests.get(url= "https://api.soundcloud.com/resolve?url=" + _url + "&client_id=dce5652caa1b66331903493735ddd64d")
    data = response.json()

    if data:
        try:
            playlist_url = data[0]['artwork_url'].replace("large.jpg", "crop.jpg")
            list.get_remote_image(playlist_url)
        except:
            pass
        for track in data[0]['tracks']:
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
                                                        uri=track['uri'],
                                                        type=Music.PUBLISHED,
                                                        creator=list.creator,
                                                        community=list.community)
                try:
                    new_track.get_remote_image(track['artwork_url'])
                except:
                    pass
                request_user.profile.tracks += 1
                request_user.profile.save(update_fields=["tracks"])
                list.playlist.add(new_track)
