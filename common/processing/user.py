from users.model.settings import *
from users.model.list import *
from users.model.profile import *
from music.models import SoundList
from video.models import VideoAlbum
from gallery.models import Album


def create_user_models(user):
    try:
        UserNotifications.objects.get(user=user)
    except:
        UserNotifications.objects.create(user=user)
    try:
        UserNotificationsPost.objects.get(user=user)
    except:
        UserNotificationsPost.objects.create(user=user)
    try:
        UserNotificationsPhoto.objects.get(user=user)
    except:
        UserNotificationsPhoto.objects.create(user=user)
    try:
        UserNotificationsGood.objects.get(user=user)
    except:
        UserNotificationsVideo.objects.create(user=user)
    try:
        UserNotificationsMusic.objects.get(user=user)
    except:
        UserNotificationsMusic.objects.create(user=user)

    try:
        UserPrivate.objects.get(user=user)
    except:
        UserPrivate.objects.create(user=user)
    try:
        UserPrivatePost.objects.get(user=user)
    except:
        UserPrivatePost.objects.create(user=user)
    try:
        UserPrivatePhoto.objects.get(user=user)
    except:
        UserPrivatePhoto.objects.create(user=user)
    try:
        UserPrivateGood.objects.get(user=user)
    except:
        UserPrivateGood.objects.create(user=user)
    try:
        UserPrivateVideo.objects.get(user=user)
    except:
        UserPrivateMusic.objects.create(user=user)

    try:
        UserColorSettings.objects.get(user=user)
    except:
        UserColorSettings.objects.create(user=user)
    try:
        UserProfile.objects.get(user=user)
    except:
        UserProfile.objects.create(user=user)
    try:
        OneUserLocation.objects.get(user=user)
    except:
        OneUserLocation.objects.create(user=user)
    try:
        IPUser.objects.get(user=user)
    except:
        IPUser.objects.create(user=user)
    try:
        UserProfileFamily.objects.get(user=user)
    except:
        UserProfileFamily.objects.create(user=user)
    try:
        UserProfileAnketa.objects.get(user=user)
    except:
        UserProfileAnketa.objects.create(user=user)
    try:
        Album.objects.get(creator=user, community=None, type=Album.AVATAR, title="Фото со страницы")
    except:
        Album.objects.create(creator=user, community=None, type=Album.AVATAR, title="Фото со страницы")
    try:
        Album.objects.get(creator=user, community=None, type=Album.WALL, title="Фото со стены")
    except:
        Album.objects.create(creator=user, community=None, type=Album.WALL, title="Фото со стены")
