from django.views.generic.base import TemplateView
from users.models import User
from django.views.generic import ListView
from common.template.user import get_template_user


class UserPostView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.post import get_template_user_post
        from posts.models import Post, PostList

        self.list, self.post = PostList.objects.get(pk=self.kwargs["pk"]), Post.objects.get(uuid=self.kwargs["uuid"])
        self.user, self.posts = self.list.creator, self.list.get_posts()
        self.template_name = get_template_user_post(self.list, "users/lenta/", "post.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPostView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserPostView,self).get_context_data(**kwargs)
        c["object"], c["list"], c["user"], c["next"], c["prev"] = self.post, self.list, self.user, \
        self.posts.filter(pk__gt=self.post.pk, is_deleted=False).order_by('pk').first(), \
        self.posts.filter(pk__lt=self.post.pk, is_deleted=False).order_by('pk').first()
        return c

class UserFixPostView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.post import get_template_user_post
        from posts.models import Post, PostList

        self.user, self.post = User.objects.get(pk=self.kwargs["pk"]), Post.objects.get(uuid=self.kwargs["uuid"])
        self.list = self.user.get_or_create_fix_list()
        self.posts = self.list.get_items()
        self.template_name = get_template_user_post(self.list, "users/lenta/", "fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserFixPostView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserFixPostView,self).get_context_data(**kwargs)
        c["object"], c["list"], c["user"], c["next"], c["prev"] = self.post, self.list, self.user, \
        self.posts.filter(pk__gt=self.post.pk, is_deleted=False).order_by('pk').first(), \
        self.posts.filter(pk__lt=self.post.pk, is_deleted=False).order_by('pk').first()
        return c


class UserGallery(TemplateView):
    """
    галерея для пользователя, своя галерея, галерея для анонима, плюс другие варианты
    """
    template_name = None
    def get(self,request,*args,**kwargs):
        from common.template.photo import get_template_user_photo
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_photo_list()
        self.template_name = get_template_user_photo(self.list, "users/user_gallery/", "gallery.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGallery,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserGallery,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.user, self.list
        return c

class UserPhotoList(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.photo import get_template_user_photo
        from gallery.models import PhotoList

        self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_template_user_photo(self.list, "users/user_photo_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPhotoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserPhotoList,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.user, self.list
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
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_staffed_user() and self.user == request.user:
            self.template_name = "users/user_community/staffed_communities.html"
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
        from common.template.music import get_template_user_music
        from music.models import SoundList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.playlist = self.user.get_playlist()
        self.template_name = get_template_user_music(self.playlist, "users/user_music/", "music.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserMusic,self).get_context_data(**kwargs)
        c['user'], c['playlist'] = self.user, self.playlist
        return c

    def get_queryset(self):
        return self.playlist.get_items().order_by('-created')


class UserDocs(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.template.doc import get_template_user_doc

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_doc_list()
        if self.user.pk == request.user.pk:
            self.doc_list = self.list.get_staff_items()
        else:
            self.doc_list = self.list.get_items()

        self.template_name = get_template_user_doc(self.list, "users/user_docs/", "docs.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserDocs,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.user, self.list
        return c

    def get_queryset(self):
        return self.doc_list


class UserGoods(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.template.good import get_template_user_good

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_good_list()
        if self.user.pk == request.user.pk:
            self.goods_list = self.list.get_staff_items()
        else:
            self.goods_list = self.list.get_items()

        self.template_name = get_template_user_good(self.list, "users/user_goods/", "goods.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserGoods,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.user, self.list
        return c

    def get_queryset(self):
        return self.goods_list


class UserVideo(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from video.models import VideoList
        from common.template.video import get_template_user_video

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_video_list()
        if self.user == request.user:
            self.video_list = self.list.get_staff_items()
        else:
            self.video_list = self.list.get_items()
        self.template_name = get_template_user_video(self.list, "users/user_video/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserVideo,self).get_context_data(**kwargs)
        c['user'], c['list'] = self.user, self.list
        return c

    def get_queryset(self):
        return self.video_list


class ProfileUserView(TemplateView):
    template_name, get_buttons_block, common_frends = None, None, None

    def get(self,request,*args,**kwargs):
        from stst.models import UserNumbers
        import re
        from posts.models import PostList

        self.user, user_agent, MOBILE_AGENT_RE, user_pk, r_user_pk = User.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'], re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE), int(self.kwargs["pk"]), request.user.pk

        if request.user.is_authenticated:
            if request.user.is_no_phone_verified():
                self.template_name = "main/phone_verification.html"
            elif user_pk == r_user_pk:
                if self.user.is_suspended():
                    self.template_name = "generic/u_template/you_suspended.html"
                elif self.user.is_blocked():
                    self.template_name = "generic/u_template/you_global_block.html"
                elif self.user.is_child():
                    self.template_name = "users/account/my_user_child.html"
                else:
                    self.template_name = "users/account/my_user.html"
                    self.post_lists = PostList.get_user_staff_lists(user_pk)
            elif r_user_pk != user_pk:
                self.post_lists, self.get_buttons_block, self.common_frends = PostList.get_user_lists(user_pk), request.user.get_buttons_profile(user_pk), self.user.get_common_friends_of_user(self.request.user)[0:5]
                if self.user.is_suspended():
                    self.template_name = "generic/u_template/user_suspended.html"
                elif self.user.is_blocked():
                    self.template_name = "generic/u_template/user_global_block.html"
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
            if self.user.is_suspended():
                self.template_name = "generic/u_template/anon_user_suspended.html"
            elif self.user.is_blocked():
                self.template_name = "generic/u_template/anon_user_global_block.html"
            elif self.user.is_closed_profile():
                self.template_name = "users/account/anon_close_user.html"
            elif not self.user.is_child_safety():
                self.template_name = "users/account/anon_no_child_safety.html"
            else:
                self.template_name = "users/account/anon_user.html"

        if MOBILE_AGENT_RE.match(user_agent):
            self.template_name = "mobile/" + self.template_name
        else:
            self.template_name = "desctop/" + self.template_name
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        c = super(ProfileUserView, self).get_context_data(**kwargs)
        c['user'], c['fix_list'], c['photo_list'], c['video_list'], c['playlist'], \
        c['docs_list'], c['good_list'],c['get_buttons_block'], c['common_frends'], c['posts_lists'] = \
        self.user, self.user.get_fix_list(), self.user.get_photo_list(), self.user.get_video_list(), \
        self.user.get_playlist(), self.user.get_doc_list(), self.user.get_good_list(), \
        self.get_buttons_block, self.common_frends, self.posts_lists
        return c
