from communities.model.settings import *
from music.models import SoundList
from video.models import VideoAlbum
from gallery.models import Album
from posts.models import PostList

def create_community_models(community):
    CommunityPrivatePost.objects.create(community=community)
    CommunityPrivatePhoto.objects.create(community=community)
    CommunityPrivateGood.objects.create(community=community)
    CommunityPrivateVideo.objects.create(community=community)
    CommunityPrivateMusic.objects.create(community=community)

    CommunitySectionsOpen.objects.create(community=community)

    CommunityNotificationsPost.objects.create(community=community)
    CommunityNotificationsPhoto.objects.create(community=community)
    CommunityNotificationsGood.objects.create(community=community)
    CommunityNotificationsVideo.objects.create(community=community)

    PostList.objects.create(community=community, type=PostList.MAIN, name="Основной список", order=0, creator=community.creator)
