import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from posts.models import Post
from communities.models import Community, CommunityMembership
from follows.models import CommunityFollow
from common.checkers import check_can_get_posts_for_community_with_name
from django.views.generic import ListView
from rest_framework.exceptions import PermissionDenied


class CommunityMusic(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from music.models import SoundList

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.playlist = SoundList.objects.get(community_id=self.community.pk, is_generic=True, name="Основной плейлист")
        except:
            self.playlist = None
        self.template_name = self.user.get_template(folder="community_music/", template="music.html", request=request)
        return super(CommunityMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityMusic,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['playlist'] = self.playlist
        return context

    def get_queryset(self):
        music_list = self.community.get_music()
        return music_list


class CommunityVideo(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from video.models import VideoAlbum

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_template(folder="community_video/", template="list.html", request=request)
        try:
            self.album = VideoAlbum.objects.get(community_id=self.community.pk, is_generic=True, title="Все видео")
        except:
            self.album = None
        if request.user.is_staff_of_community_with_name(self.community.name):
            self.video_list = self.album.get_my_queryset()
        else:
            self.video_list = self.album.get_queryset()
        return super(CommunityVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideo,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


class PostsCommunity(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.fixed = Post.objects.get(community=community, is_fixed=True)
        except:
            self.fixed = None

        if request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_lenta/admin_list.html"
            elif request.user.is_post_manager():
                self.template_name = "c_lenta/staff_list.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_lenta/list.html"
            else:
                self.template_name = "c_lenta/list.html"
        elif request.user.is_anonymous:
            if self.community.is_public():
                self.template_name = "c_lenta/list.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(PostsCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostsCommunity,self).get_context_data(**kwargs)
        context['object'] = self.fixed
        context["community"] = self.community
        return context

    def get_queryset(self):
        item_list = self.community.get_posts().order_by('-created')
        return item_list


class PostCommunity(TemplateView):
    model = Post
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.items = self.community.get_posts()
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()

        if request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_lenta/admin_item.html"
            elif request.user.is_post_manager():
                self.template_name = "c_lenta/staff_item.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_lenta/item.html"
            else:
                self.template_name = "c_lenta/item.html"
        elif request.user.is_anonymous:
            if self.community.is_public():
                self.template_name = "c_lenta/item.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(PostCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunity,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["community"] = self.community
        context["next"] = self.next
        context["prev"] = self.prev
        return context


class CommunityDetail(TemplateView):
    template_name = None
    common_friends = None

    def get(self,request,*args,**kwargs):
        from stst.models import CommunityNumbers

        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if self.community.is_suspended():
            self.template_name = "c_detail/community_suspended.html"
        elif self.community.is_blocked():
            self.template_name = "c_detail/community_blocked.html"
        elif request.user.is_authenticated:
            if request.user.is_member_of_community_with_name(self.community.name):
                if request.user.is_administrator_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/admin_community.html"
                elif request.user.is_moderator_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/moderator_community.html"
                elif request.user.is_editor_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/editor_community.html"
                elif request.user.is_advertiser_of_community_with_name(self.community.name):
                    self.template_name = "c_detail/advertiser_community.html"
                elif request.user.is_community_manager():
                    self.template_name = "c_detail/staff_community.html"
                else:
                    self.template_name = "c_detail/member_community.html"
            elif request.user.is_follow_from_community_with_name(self.community.pk):
                self.template_name = "c_detail/follow_community.html"
            elif request.user.is_community_manager():
                self.template_name = "c_detail/staff_community.html"
            elif request.user.is_banned_from_community_with_name(self.community.name):
                self.template_name = "c_detail/block_community.html"
            elif self.community.is_public():
                self.template_name = "c_detail/public_community.html"
            elif self.community.is_closed():
                self.template_name = "c_detail/close_community.html"
            elif self.community.is_private():
                self.template_name = "c_detail/private_community.html"
            if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                CommunityNumbers.objects.create(user=request.user.pk, community=self.community.pk, platform=1)
            else:
                CommunityNumbers.objects.create(user=request.user.pk, community=self.community.pk, platform=0)
            self.common_friends = request.user.get_common_friends_of_community(self.community.pk)[0:6]
        elif request.user.is_anonymous:
            if self.community.is_public():
                self.template_name = "c_detail/anon_public_community.html"
            elif self.community.is_closed():
                self.template_name = "c_detail/anon_close_community.html"
            elif self.community.is_private():
                self.template_name = "c_detail/anon_private_community.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(CommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDetail,self).get_context_data(**kwargs)
        context["membersheeps"] = self.community.get_community_with_name_members(self.community.name)[0:6]
        context["community"] = self.community
        context["common_friends"] = self.common_friends
        return context
