from users.model.settings import *
from music.models import SoundList
from video.models import VideoAlbum
from gallery.models import Album

def create_user_models(community):
    UserNotifications.objects.create(user=user)
    UserNotificationsPost.objects.create(user=user)
    UserNotificationsPhoto.objects.create(user=user)
    UserNotificationsGood.objects.create(user=user)
    UserNotificationsVideo.objects.create(user=user)
    UserNotificationsMusic.objects.create(user=user)

    UserPrivate.objects.create(user=user)
    UserPrivatePost.objects.create(user=user)
    UserPrivatePhoto.objects.create(user=user)
    UserPrivateGood.objects.create(user=user)
    UserPrivateVideo.objects.create(user=user)
    UserPrivateMusic.objects.create(user=user)

    UserColorSettings.objects.create(user=user)
    UserProfile.objects.create(user=user)
    OneUserLocation.objects.create(user=user)
    IPUser.objects.create(user=user)
    UserProfileFamily.objects.create(user=user)
    UserProfileAnketa.objects.create(user=user)

    SoundList.objects.create(creator=user, community=None, type=SoundList.MAIN, name="Основной плейлист")
    VideoAlbum.objects.create(creator=user, community=None, type=VideoAlbum.MAIN, title="Основной список")

    Album.objects.create(creator=user, community=None, type=Album.AVATAR, title="Фото со страницы")
    Album.objects.create(creator=user, community=None, type=Album.MAIN, title="Основной альбом")
    Album.objects.create(creator=user, community=None, type=Album.WALL, title="Фото со стены")
