from django.views.generic.base import TemplateView
from users.models import User
from django.views.generic import ListView
from common.template.user import get_template_user
from common.templates import get_template_anon_user, get_template_user


class UserPostView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item
        from posts.models import Post, PostList

        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.list = self.post.list
        self.user, self.posts = self.list.creator, self.list.get_items()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.post, "users/lenta/", "post.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.post, "users/lenta/anon_post.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserPostView,self).get_context_data(**kwargs)
        c["object"], c["list"], c["user"], c["next"], c["prev"], c["posts"] = self.post, self.list, self.user, \
        self.posts.filter(pk__gt=self.post.pk).order_by('pk').first(), \
        self.posts.filter(pk__lt=self.post.pk).order_by('pk').first(), self.posts
        return c

class UserFixPostView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_item, get_template_anon_user_item
        from posts.models import Post, PostList

        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.list = PostList.objects.get(creator_id=self.user.pk, type=PostList.FIXED)
        self.posts = self.list.get_fix_items()
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.post, "users/lenta/", "fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.post, "users/lenta/anon_fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserFixPostView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserFixPostView,self).get_context_data(**kwargs)
        c["object"], c["list"], c["user"], c["next"], c["prev"] = self.post, self.list, self.user, \
        self.posts.filter(pk__gt=self.post.pk).order_by('pk').first(), \
        self.posts.filter(pk__lt=self.post.pk).order_by('pk').first()
        return c


class UserGallery(TemplateView):
    """
    галерея для пользователя, своя галерея, галерея для анонима, плюс другие варианты
    """
    template_name = None
    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_photo_list()
        if request.user.pk == self.user.pk:
            self.get_lists = PhotoList.get_user_staff_lists(self.user.pk)
        else:
            self.get_lists = PhotoList.get_user_lists(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user(self.list, "users/photos/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_user(self.list, "users/photos/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
        self.count_lists = PhotoList.get_user_lists_count(self.user.pk)
        return super(UserGallery,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserGallery,self).get_context_data(**kwargs)
        c['user'], c['list'], c['get_lists'], c['count_lists'] = self.user, self.list, self.get_lists, self.count_lists
        return c

class UserCommunities(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_staffed_user() and self.user == request.user:
            from common.template.user import get_detect_platform_template
            self.template_name = get_detect_platform_template("users/user_community/my_staffed_communities.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            from common.template.user import get_template_user
            self.template_name = get_template_user(self.user, "users/user_community/", "communities.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCommunities,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCommunities, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        return self.user.get_communities()

class UserStaffCommunities(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.utils import get_folder
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_staffed_user() and self.user == request.user:
            self.template_name = get_folder(request.META['HTTP_USER_AGENT']) + "users/user_community/staffed_communities.html"

        return super(UserStaffCommunities,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserStaffCommunities, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        return self.user.get_staffed_communities()


class UserMobStaffed(ListView):
    template_name, paginate_by = "mobile/users/user_community/staffed.html", 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        return super(UserMobStaffed,self).get(request,*args,**kwargs)

    def get_queryset(self):
        return self.user.get_staffed_communities()


class UserMusic(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from music.models import SoundList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list, self.get_lists = self.user.get_playlist(), None
        if request.user.pk == self.user.pk:
            self.get_items = self.list.get_staff_items()
            self.get_lists = SoundList.get_user_staff_lists(self.user.pk)
        else:
            self.get_items = self.list.get_items()
            self.get_lists = SoundList.get_user_lists(self.user.pk)
        self.count_lists = SoundList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user(self.list, "users/music/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_user(self.list, "users/music/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
        return super(UserMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserMusic,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'] = self.user, self.list, self.count_lists, self.get_lists
        return c

    def get_queryset(self):
        return self.get_items


class UserDocs(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from docs.models import DocList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_doc_list()
        if request.user.pk == self.user.pk:
            self.get_lists = DocList.get_user_staff_lists(self.user.pk)
            self.get_items = self.list.get_staff_items()
        else:
            self.get_lists = DocList.get_user_lists(self.user.pk)
            self.get_items = self.list.get_items()
        self.count_lists = DocList.get_user_lists_count(self.user.pk)

        if request.user.is_anonymous:
            self.template_name = get_template_anon_user(self.list, "users/docs/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_user(self.list, "users/docs/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
        return super(UserDocs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserDocs,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'] = self.user, self.list, self.count_lists, self.get_lists
        return c

    def get_queryset(self):
        return self.get_items


class UserGoods(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from goods.models import GoodList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_good_list()
        if request.user.pk == self.user.pk:
            self.get_lists = GoodList.get_user_staff_lists(self.user.pk)
            self.get_items = self.list.get_staff_items()
        else:
            self.get_lists = GoodList.get_user_lists(self.user.pk)
            self.get_items = self.list.get_items()
        self.count_lists = GoodList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user(self.list, "users/goods/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_user(self.list, "users/goods/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_good_manager())
        return super(UserGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserGoods,self).get_context_data(**kwargs)
        c['user'], c['list'], c['get_lists'], c['count_lists'] = self.user, self.list, self.get_lists, self.count_lists
        return c

    def get_queryset(self):
        return self.get_items


class UserVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from video.models import VideoList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_video_list()
        if request.user.pk == self.user.pk:
            self.get_lists = VideoList.get_user_staff_lists(self.user.pk)
            self.get_items = self.list.get_staff_items()
        else:
            self.get_lists = VideoList.get_user_lists(self.user.pk)
            self.get_items = self.list.get_items()
        self.count_lists = VideoList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user(self.list, "users/video/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_user(self.list, "users/video/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
        return super(UserVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserVideo,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'] = self.user, self.list, self.count_lists, self.get_lists
        return c

    def get_queryset(self):
        return self.get_items


class ProfileUserView(TemplateView):
    is_photo_open,is_post_open,is_friend_open,is_doc_open,is_video_open,is_music_open,is_community_open,is_good_open,template_name,get_buttons_block,common_frends,user_photos,user_goods,user_musics,user_videos,user_docs,user_friends,user_communities,user_workspaces,user_boards = None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None

    def get(self,request,*args,**kwargs):
        from stst.models import UserNumbers
        import re

        user_pk, r_user_pk = int(self.kwargs["pk"]), request.user.pk
        user_agent, MOBILE_AGENT_RE = request.META['HTTP_USER_AGENT'], re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if request.user.is_authenticated:
            if request.user.is_no_phone_verified():
                self.template_name = "main/phone_verification.html"
            elif user_pk == r_user_pk:
                self.user = User.objects.select_related('profile').get(pk=self.kwargs["pk"])
                if self.user.is_suspended():
                    self.template_name = "generic/u_template/you_suspended.html"
                elif self.user.is_closed():
                    self.template_name = "generic/u_template/you_closed.html"
                elif self.user.is_child():
                    self.template_name = "users/account/my_user_child.html"
                else:
                    self.template_name = "users/account/my_user.html"
            elif r_user_pk != user_pk:
                self.user = User.objects.select_related('profile', 'user_private').get(pk=self.kwargs["pk"])
                self.get_buttons_block, self.common_frends = request.user.get_buttons_profile(user_pk), self.user.get_common_friends_of_user(self.request.user)[0:5]

                self.is_photos_open = self.user.is_photo_open(r_user_pk)
                self.is_post_open = self.user.is_post_open(r_user_pk)
                self.is_video_open = self.user.is_video_open(r_user_pk)
                self.is_music_open = self.user.is_music_open(r_user_pk)
                self.is_doc_open = self.user.is_doc_open(r_user_pk)
                self.is_community_open = self.user.is_community_open(r_user_pk)
                self.is_friend_open = self.user.is_friend_open(r_user_pk)
                self.is_good_open = self.user.is_good_open(r_user_pk)

                if self.user.is_suspended():
                    self.template_name = "generic/u_template/user_suspended.html"
                elif self.user.is_closed():
                    self.template_name = "generic/u_template/user_closed.html"
                elif request.user.is_user_manager() or request.user.is_superuser:
                    self.template_name, self.get_buttons_block = "users/account/staff_user.html", request.user.get_staff_buttons_profile(user_pk)
                    if request.user.is_connected_with_user_with_id(user_id=user_pk):
                        request.user.create_or_plus_populate_friend(user_pk)
                elif request.user.is_blocked_with_user_with_id(user_id=user_pk):
                    self.template_name = "users/account/block_user.html"
                elif request.user.is_connected_with_user_with_id(user_id=user_pk):
                    self.template_name = "users/account/user.html"
                    request.user.create_or_plus_populate_friend(user_pk)
                elif self.user.is_closed_profile():
                    if request.user.is_followers_user_with_id(user_id=user_pk) or request.user.is_connected_with_user_with_id(user_id=user_pk):
                        self.template_name = "users/account/user.html"
                    else:
                        self.template_name = "users/account/close_user.html"
                elif request.user.is_child() and not self.user.is_child_safety():
                    self.template_name = "users/account/no_child_safety.html"
                else:
                    self.template_name = "users/account/user.html"
                if MOBILE_AGENT_RE.match(user_agent):
                    UserNumbers.objects.create(visitor=r_user_pk, target=user_pk, device=UserNumbers.PHONE)
                else:
                    UserNumbers.objects.create(visitor=r_user_pk, target=user_pk, device=UserNumbers.DESCTOP)
        elif request.user.is_anonymous:
            self.user = User.objects.select_related('profile', 'user_private').get(pk=self.kwargs["pk"])
            if self.user.is_suspended():
                self.template_name = "generic/u_template/anon_user_suspended.html"
            elif self.user.is_closed():
                self.template_name = "generic/u_template/anon_user_closed.html"
            elif self.user.is_closed_profile():
                self.template_name = "users/account/anon_close_user.html"
            elif not self.user.is_child_safety():
                self.template_name = "users/account/anon_no_child_safety.html"
            else:
                self.template_name = "users/account/anon_user.html"

        self.user_photos = self.user.get_user_photos(r_user_pk)

        if MOBILE_AGENT_RE.match(user_agent):
            self.template_name = "mobile/" + self.template_name
        else:
            self.template_name = "desctop/" + self.template_name
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        c = super(ProfileUserView, self).get_context_data(**kwargs)
        c['user'],
        c['photo_list'],
        c['video_list'],
        c['music_list'],
        c['docs_list'],
        c['good_list'],
        c['get_buttons_block'],
        c['common_frends'],
        c['post_list_pk'] =
        self.user,
        self.user_photos,
        self.user.get_video_list(),
        self.user.get_playlist(),
        self.user.get_doc_list(),
        self.user.get_good_list(),
        self.get_buttons_block,
        self.common_frends,
        self.user.get_selected_post_list_pk()
        return c
