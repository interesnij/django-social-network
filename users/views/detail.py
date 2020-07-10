import re
from django.views.generic.base import TemplateView
from users.models import User
from django.views.generic import ListView
from music.models import SoundcloudParsing
from communities.models import Community
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


class UserPostView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import Post
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.posts = self.user.get_posts()

        if request.user.is_authenticated:
            if self.user.pk == request.user.pk:
                self.template_name = "lenta/my_post.html"
            elif request.user.is_post_manager():
                self.template_name = "lenta/staff_post.html"
            elif self.user != request.user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
                if self.user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
                self.template_name = "lenta/post.html"
        elif request.user.is_anonymous:
            if self.user.is_closed_profile():
                raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
            else:
                self.template_name = "lenta/anon_post.html"

        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        self.next = self.posts.filter(pk__gt=self.post.pk).order_by('pk').first()
        self.prev = self.posts.filter(pk__lt=self.post.pk).order_by('-pk').first()
        return super(UserPostView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPostView,self).get_context_data(**kwargs)
        context["object"] = self.post
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context

class UserCommunities(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="user_community/", template="communities.html", request=request)
        if self.user.is_staffed_user() and self.user == request.user:
            self.template_name = "user_community/my_staffed_communities.html"
        return super(UserCommunities,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCommunities, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        communities_list = Community.objects.filter(memberships__user__id=self.user.pk)
        return communities_list

class UserStaffCommunities(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_staffed_user() and self.user == request.user:
            self.template_name = "user_community/staffed_communities.html"
        return super(UserStaffCommunities,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserStaffCommunities, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        communities_list = self.user.get_staffed_communities()
        return communities_list


class UserMobStaffed(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user == request.user:
            self.template_name = "mob_user_community/staffed.html"
        return super(UserMobStaffed,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserMobStaffed, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context


class UserMusic(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from music.models import SoundList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.playlist = SoundList.objects.get(creator_id=self.user.pk, community=None, is_generic=True, name="Основной плейлист")
        except:
            self.playlist = SoundList.objects.create(creator_id=self.user.pk, community=None, is_generic=True, name="Основной плейлист")
        self.template_name = self.user.get_template_user(folder="user_music/", template="music.html", request=request)
        return super(UserMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserMusic,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['playlist'] = self.playlist
        return context

    def get_queryset(self):
        music_list = self.user.get_music()
        return music_list


class UserVideo(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from video.models import VideoAlbum

        self.template_name = request.user.get_template_user(folder="user_video_list/", template="list.html", request=request)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.album = VideoAlbum.objects.get(creator_id=self.user.pk, community=None, is_generic=True, title="Все видео")
        except:
            self.album = VideoAlbum.objects.create(creator_id=self.user.pk, community=None, is_generic=True, title="Все видео")
        if self.user == request.user:
            self.video_list = self.album.get_my_queryset()
        else:
            self.video_list = self.album.get_queryset()
        return super(UserVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideo,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


class ProfileUserView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from stst.models import UserNumbers

        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.get_buttons_block = self.user.get_buttons_profile(self.user.pk)

        if self.user.pk == request.user.pk:
            if not request.user.is_phone_verified:
                self.template_name = "main/phone_verification.html"
            elif self.user.is_suspended():
                self.template_name = "main/you_suspended.html"
            elif self.user.is_blocked():
                self.template_name = "main/you_global_block.html"
            else:
                self.template_name = "account/my_user.html"
        elif request.user.pk != self.user.pk and request.user.is_authenticated:
            if not request.user.is_phone_verified:
                self.template_name = "main/phone_verification.html"
            elif self.user.is_suspended():
                self.template_name = "main/user_suspended.html"
                self.get_buttons_block = self.user.get_staff_buttons_profile(self.user.pk)
            elif self.user.is_blocked():
                self.template_name = "main/user_global_block.html"
            elif request.user.is_user_manager() or request.user.is_superuser:
                self.template_name = "account/staff_user.html"
            elif request.user.is_blocked_with_user_with_id(user_id=self.user.pk):
                self.template_name = "account/block_user.html"
            elif self.user.is_closed_profile():
                if request.user.is_followers_user_with_id(user_id=self.user.pk):
                    self.template_name = "account/user.html"
                elif not request.user.is_connected_with_user_with_id(user_id=self.user.pk):
                    self.template_name = "account/close_user.html"
                else:
                    self.template_name = "account/user.html"
            else:
                self.template_name = "account/user.html"
        elif request.user.is_anonymous and self.user.is_closed_profile():
            self.template_name = "account/close_user.html"
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.template_name = "account/anon_user.html"

        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
            if request.user.is_authenticated and request.user.pk != self.user.pk:
                UserNumbers.objects.create(visitor=request.user.pk, target=self.user.pk, platform=1)
        else:
            if request.user.is_authenticated and request.user.pk != self.user.pk:
                UserNumbers.objects.create(visitor=request.user.pk, target=self.user.pk, platform=0)
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['communities'] = self.user.get_pop_communities()
        context['get_buttons_block'] = self.get_buttons_block
        if self.request.user.is_authenticated:
            context['common_frends'] = self.user.get_common_friends_of_user(self.request.user)[0:5]
        return context
