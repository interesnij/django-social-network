from communities.model.settings import *
from music.models import SoundList
from video.models import VideoAlbum
from gallery.models import Album

def create_community_models(community):
    CommunityPrivatePost.objects.create(community=community)
    CommunityPrivatePhoto.objects.create(community=community)
    CommunityPrivateGood.objects.create(community=community)
    CommunityPrivateVideo.objects.create(community=community)

    CommunitySectionsOpen.objects.create(community=community)

    CommunityNotificationsPost.objects.create(community=community)
    CommunityNotificationsPhoto.objects.create(community=community)
    CommunityNotificationsGood.objects.create(community=community)
    CommunityNotificationsVideo.objects.create(community=community)

    SoundList.objects.create(creator=community.creator, community=community, type=SoundList.MAIN, name="Основной плейлист")
    VideoAlbum.objects.create(creator=community.creator, community=community, type=VideoAlbum.MAIN, title="Основной список")

    Album.objects.create(creator=community.creator, community=community, type=Album.AVATAR, title="Фото со страницы")
    Album.objects.create(creator=community.creator, community=community, type=Album.MAIN, title="Основной альбом")
    Album.objects.create(creator=community.creator, community=community, type=Album.WALL, title="Фото со стены")
