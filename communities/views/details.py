from django.views.generic.base import TemplateView
from posts.models import Post
from communities.models import Community, CommunityMembership
from follows.models import CommunityFollow
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied
from common.template.post import get_template_community_post
from common.template.photo import get_template_community_photo


class PostCommunity(TemplateView):
    model = Post
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.items = self.community.get_posts()
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()

        self.template_name = get_template_community_post(self.community, "communities/lenta/", "item.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunity,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["community"] = self.community
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class CommunityDetail(TemplateView):
    template_name, common_friends, common_friends_count = None, None, None

    def get(self,request,*args,**kwargs):
        from stst.models import CommunityNumbers
        import re
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

        self.community, user_agent = Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT']

        if self.community.is_suspended():
            self.template_name = "communities/detail/community_suspended.html"
        elif self.community.is_blocked():
            self.template_name = "communities/detail/community_blocked.html"
        elif request.user.is_authenticated:
            if request.user.is_member_of_community(self.community.pk):
                if request.user.is_administrator_of_community(self.community.pk):
                    self.template_name = "communities/detail/admin_community.html"
                elif request.user.is_moderator_of_community(self.community.pk):
                    self.template_name = "communities/detail/moderator_community.html"
                elif request.user.is_editor_of_community(self.community.pk):
                    self.template_name = "communities/detail/editor_community.html"
                elif request.user.is_advertiser_of_community(self.community.pk):
                    self.template_name = "communities/detail/advertiser_community.html"
                elif request.user.is_community_manager():
                    self.template_name = "communities/detail/staff_member_community.html"
                else:
                    self.template_name = "communities/detail/member_community.html"
                request.user.create_or_plus_populate_community(self.community.pk)
            elif request.user.is_follow_from_community(self.community.pk):
                self.template_name = "communities/detail/follow_community.html"
            elif request.user.is_community_manager():
                self.template_name = "communities/detail/staff_community.html"
            elif request.user.is_banned_from_community(self.community.pk):
                self.template_name = "communities/detail/block_community.html"
            elif self.community.is_public():
                if request.user.is_child() and not self.community.is_verified():
                    self.template_name = "communities/detail/no_child_safety.html"
                else:
                    self.template_name = "communities/detail/public_community.html"
            elif self.community.is_closed():
                self.template_name = "communities/detail/close_community.html"
            elif self.community.is_private():
                self.template_name = "generic/c_template/private_community.html"
            if MOBILE_AGENT_RE.match(user_agent):
                CommunityNumbers.objects.create(user=request.user.pk, community=self.community.pk, platform=1)
            else:
                CommunityNumbers.objects.create(user=request.user.pk, community=self.community.pk, platform=0)
            self.common_friends, self.common_friends_count = request.user.get_common_friends_of_community(self.community.pk)[0:6], request.user.get_common_friends_of_community_count_ru(self.community.pk)
        elif request.user.is_anonymous:
            if self.community.is_public():
                if not self.community.is_verified():
                    self.template_name = "communities/detail/anon_no_child_safety.html"
                else:
                    self.template_name = "communities/detail/anon_community.html"
            elif self.community.is_closed():
                self.template_name = "communities/detail/anon_close_community.html"
            elif self.community.is_private():
                self.template_name = "communities/detail/anon_private_community.html"

        if MOBILE_AGENT_RE.match(user_agent):
            self.template_name = "mobile/" + self.template_name
        else:
            self.template_name = "mobile/" + self.template_name
        return super(CommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDetail,self).get_context_data(**kwargs)
        context["membersheeps"] = self.community.get_members(self.community.pk)[0:6]
        context["community"] = self.community
        context["common_friends"] = self.common_friends
        context["common_friends_count"] = self.common_friends_count
        context['photo_album'] = self.community.get_or_create_photo_album()
        context['video_album'] = self.community.get_or_create_video_album()
        context['music_list'] = self.community.get_or_create_playlist()
        context['docs_list'] = self.community.get_or_create_doc_list()
        context['good_album'] = self.community.get_or_create_good_album()
        return context


class CommunityGallery(TemplateView):
    """
    галерея сообщества с правами доступа
    """
    template_name = None
    def get(self,request,*args,**kwargs):
        from gallery.models import Album

        self.community, self.album, self.albums_list, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), Album.objects.get(community_id=self.community.pk, type=Album.MAIN), self.community.get_albums().order_by('-created'), get_template_community_photo(self.community, "communities/gallery/", "gallery.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityGallery,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGallery,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['albums_list'] = self.albums_list
        context['album'] = self.album
        return context

class CommunityAlbum(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from gallery.models import Album

        self.community, self.album, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), Album.objects.get(uuid=self.kwargs["uuid"]), get_template_community_photo(self.community, "communities/album/", "album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityAlbum,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbum,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context
