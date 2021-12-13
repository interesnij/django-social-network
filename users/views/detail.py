from django.views.generic.base import TemplateView
from users.models import User
from django.views.generic import ListView
from common.templates import get_template_user_list, get_template_anon_user_list


class UserGallery(TemplateView):
    template_name, is_user_can_see_photo_section = None, None

    def get(self,request,*args,**kwargs):
        from gallery.models import PhotoList
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_photo_list()
        if request.user.pk == self.user.pk:
            self.get_lists = PhotoList.get_user_staff_lists(self.user.pk)
            self.is_user_can_see_photo_section = True
        else:
            self.get_lists = PhotoList.get_user_lists(self.user.pk)
            self.is_user_can_see_photo_section = self.user.is_user_can_see_photo(request.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/photos/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_photo_section = self.user.is_anon_user_can_see_photo()
        else:
            self.template_name = get_template_user_list(self.list, "users/photos/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        self.count_lists = PhotoList.get_user_lists_count(self.user.pk)
        self.is_can_see = self.user.is_user_can_see_info(request.user.pk)
        return super(UserGallery,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserGallery,self).get_context_data(**kwargs)
        c['is_can_see'], c['user'], c['list'], c['get_lists'], c['count_lists'], c['is_user_can_see_photo_section'] = self.is_can_see, self.user, self.list, self.get_lists, self.count_lists, self.is_user_can_see_photo_section
        return c

class UserCommunities(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/user_community/anon_communities.html", request.user, request.META['HTTP_USER_AGENT'])
        elif self.user.is_staffed_user() and self.user == request.user:
            from common.templates import get_detect_platform_template
            self.template_name = get_detect_platform_template("users/user_community/my_staffed_communities.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_user_list(self.user, "users/user_community/", "communities.html", request.user, request.META['HTTP_USER_AGENT'])
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
    template_name, paginate_by, is_user_can_see_music_section, is_user_can_see_music_list, is_user_can_create_tracks = None, 15, None, None, None

    def get(self,request,*args,**kwargs):
        from music.models import MusicList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list, self.get_lists = self.user.get_playlist(), None
        if request.user.pk == self.user.pk:
            self.get_lists = MusicList.get_user_staff_lists(self.user.pk)
            self.is_user_can_see_music_section = True
            self.is_user_can_create_tracks = True
            self.is_user_can_see_music_list = True
        elif request.user.is_authenticated:
            self.is_user_can_see_music_section = self.user.is_user_can_see_music(request.user.pk)
            self.is_user_can_see_music_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_tracks = self.list.is_user_can_create_el(request.user.pk)
            self.get_lists = MusicList.get_user_lists(self.user.pk)
        self.count_lists = MusicList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/music/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_music_section = self.user.is_anon_user_can_see_music()
            self.is_user_can_see_music_list = self.list.is_anon_user_can_see_el()
            self.get_lists = MusicList.get_user_lists(self.user.pk)
        else:
            self.template_name = get_template_user_list(self.list, "users/music/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserMusic,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'], c['is_user_can_see_music_section'], c['is_user_can_see_music_section'], c['is_user_can_create_tracks'] = self.user, self.list, self.count_lists, self.get_lists, self.is_user_can_see_music_section, self.is_user_can_see_music_list, self.is_user_can_create_tracks
        return c

    def get_queryset(self):
        return self.list.get_items()


class UserDocs(ListView):
    template_name, paginate_by, is_user_can_see_doc_section, is_user_can_see_doc_list, is_user_can_create_docs = None, 15, None, None, None

    def get(self,request,*args,**kwargs):
        from docs.models import DocsList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_doc_list()
        if request.user.pk == self.user.pk:
            self.get_lists = DocsList.get_user_staff_lists(self.user.pk)
            self.is_user_can_see_doc_section = True
            self.is_user_can_create_docs = True
            self.is_user_can_see_doc_list = True
        elif request.user.is_authenticated:
            self.is_user_can_see_doc_section = self.user.is_user_can_see_doc(request.user.pk)
            self.is_user_can_see_doc_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_docs = self.list.is_user_can_create_el(request.user.pk)
            self.get_lists = DocsList.get_user_lists(self.user.pk)
        self.count_lists = DocsList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/docs/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_doc_section = self.user.is_anon_user_can_see_doc()
            self.is_user_can_see_doc_list = self.list.is_anon_user_can_see_el()
            self.get_lists = DocsList.get_user_lists(self.user.pk)
        else:
            self.template_name = get_template_user_list(self.list, "users/docs/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocs,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserDocs,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'], c['is_user_can_see_doc_section'], c['is_user_can_see_doc_section'], c['is_user_can_create_docs'] = self.user, self.list, self.count_lists, self.get_lists, self.is_user_can_see_doc_section, self.is_user_can_see_doc_list, self.is_user_can_create_docs
        return c

    def get_queryset(self):
        return self.list.get_items()


class UserGoods(ListView):
    template_name, paginate_by, is_user_can_see_good_section, is_user_can_see_good_list, is_user_can_create_goods = None, 15, None, None, None

    def get(self,request,*args,**kwargs):
        from goods.models import GoodList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_good_list()
        if request.user.pk == self.user.pk:
            self.get_lists = GoodList.get_user_staff_lists(self.user.pk)
            self.is_user_can_see_good_section = True
            self.is_user_can_create_goods = True
            self.is_user_can_see_good_list = True
        elif request.user.is_authenticated:
            self.is_user_can_see_good_section = self.user.is_user_can_see_good(request.user.pk)
            self.is_user_can_see_good_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_goods = self.list.is_user_can_create_el(request.user.pk)
            self.get_lists = GoodList.get_user_lists(self.user.pk)
        self.count_lists = GoodList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/goods/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_good_section = self.user.is_anon_user_can_see_good()
            self.is_user_can_see_good_list = self.list.is_anon_user_can_see_el()
            self.get_lists = GoodList.get_user_lists(self.user.pk)
        else:
            self.template_name = get_template_user_list(self.list, "users/goods/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserGoods,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'], c['is_user_can_see_good_section'], c['is_user_can_see_good_section'], c['is_user_can_create_goods'] = self.user, self.list, self.count_lists, self.get_lists, self.is_user_can_see_good_section, self.is_user_can_see_good_list, self.is_user_can_create_goods
        return c

    def get_queryset(self):
        return self.list.get_items()


class UserVideo(ListView):
    template_name, paginate_by, is_user_can_see_video_section, is_user_can_see_video_list, is_user_can_create_videos = None, 15, None, None, None

    def get(self,request,*args,**kwargs):
        from video.models import VideoList

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = self.user.get_video_list()
        if request.user.pk == self.user.pk:
            self.get_lists = VideoList.get_user_staff_lists(self.user.pk)
            self.is_user_can_see_video_section = True
            self.is_user_can_create_videos = True
            self.is_user_can_see_video_list = True
        elif request.user.is_authenticated:
            self.is_user_can_see_video_section = self.user.is_user_can_see_video(request.user.pk)
            self.is_user_can_see_video_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_videos = self.list.is_user_can_create_el(request.user.pk)
            self.get_lists = VideoList.get_user_lists(self.user.pk)
        self.count_lists = VideoList.get_user_lists_count(self.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/video/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_video_section = self.user.is_anon_user_can_see_video()
            self.is_user_can_see_video_list = self.list.is_anon_user_can_see_el()
            self.get_lists = VideoList.get_user_lists(self.user.pk)
        else:
            self.template_name = get_template_user_list(self.list, "users/video/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(UserVideo,self).get_context_data(**kwargs)
        c['user'], c['list'], c['count_lists'], c['get_lists'], c['is_user_can_see_video_section'], c['is_user_can_see_video_list'], c['is_user_can_create_videos'] = self.user, self.list, self.count_lists, self.get_lists, self.is_user_can_see_video_section, self.is_user_can_see_video_list, self.is_user_can_create_videos
        return c

    def get_queryset(self):
        return self.list.get_items()


class ProfileUserView(TemplateView):
    is_photo_open,is_post_open,is_friend_open,is_doc_open,is_video_open,is_music_open,is_community_open,is_good_open,template_name,common_friends_count,common_frends,get_buttons_block = None,None,None,None,None,None,None,None,None,None,None,None

    def get(self,request,*args,**kwargs):
        from common.templates import update_activity, get_folder

        user_pk, r_user_pk = int(self.kwargs["pk"]), request.user.pk
        self.user = User.objects.get(pk=user_pk)
        if request.user.is_authenticated:
            if request.user.is_no_phone_verified():
                self.template_name = "main/phone_verification.html"
            elif user_pk == r_user_pk:
                self.is_community_open, self.is_photo_open, self.is_video_open, self.is_music_open, self.is_friend_open, self.is_good_open  = True,True,True,True,True,True
                if self.user.is_suspended():
                    self.template_name = "generic/u_template/you_suspended.html"
                elif self.user.is_closed():
                    self.template_name = "generic/u_template/you_closed.html"
                elif self.user.is_child():
                    self.template_name = "users/account/my_user_child.html"
                else:
                    self.template_name = "users/account/my_user.html"
            elif r_user_pk != user_pk:
                self.get_buttons_block, self.common_frends = request.user.get_buttons_profile(user_pk), self.user.get_common_friends_of_user(self.request.user)[0:5]

                self.is_photo_open = self.user.is_user_can_see_photo(r_user_pk)
                self.is_video_open = self.user.is_user_can_see_video(r_user_pk)
                self.is_music_open = self.user.is_user_can_see_music(r_user_pk)
                self.is_doc_open = self.user.is_user_can_see_doc(r_user_pk)
                self.is_community_open = self.user.is_user_can_see_community(r_user_pk)
                self.is_friend_open = self.user.is_user_can_see_friend(r_user_pk)
                self.is_good_open = self.user.is_user_can_see_good(r_user_pk)

                if self.user.is_suspended():
                    self.template_name = "generic/u_template/user_suspended.html"
                elif self.user.is_closed():
                    self.template_name = "generic/u_template/user_closed.html"
                elif request.user.is_user_manager() or request.user.is_superuser:
                    self.template_name, self.get_buttons_block = "users/account/staff_user.html", request.user.get_staff_buttons_profile(user_pk)
                    if request.user.is_connected_with_user_with_id(user_id=user_pk):
                        request.user.plus_friend_visited(user_pk)
                elif request.user.is_blocked_with_user_with_id(user_id=user_pk):
                    self.template_name = "users/account/block_user.html"
                elif request.user.is_connected_with_user_with_id(user_id=user_pk):
                    self.template_name = "users/account/user.html"
                    request.user.plus_friend_visited(user_pk)
                elif self.user.is_closed_profile():
                    if request.user.is_followers_user_with_id(user_id=user_pk) or request.user.is_connected_with_user_with_id(user_id=user_pk):
                        self.template_name = "users/account/user.html"
                    else:
                        self.template_name = "users/account/close_user.html"
                elif request.user.is_child() and not self.user.is_child_safety():
                    self.template_name = "users/account/no_child_safety.html"
                else:
                    self.template_name = "users/account/user.html"
            update_activity(request.user, request.META['HTTP_USER_AGENT'])
        elif request.user.is_anonymous:
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
            self.is_photo_open = self.user.is_anon_user_can_see_photo()
            self.is_video_open = self.user.is_anon_user_can_see_video()
            self.is_music_open = self.user.is_anon_user_can_see_music()
            self.is_doc_open = self.user.is_anon_user_can_see_doc()
            self.is_community_open = self.user.is_anon_user_can_see_community()
            self.is_friend_open = self.user.is_anon_user_can_see_friend()
            self.is_good_open = self.user.is_anon_user_can_see_good()

        self.template_name = get_folder(request.META['HTTP_USER_AGENT']) + self.template_name

        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        c = super(ProfileUserView, self).get_context_data(**kwargs)
        c['user'],c['get_buttons_block'],c['common_frends'],c['is_photo_open'],c['is_post_open'],c['is_community_open'],c['is_friend_open'],c['is_doc_open'],c['is_video_open'],c['is_music_open'],c['is_good_open'],c['post_list_pk'] = self.user,self.get_buttons_block,self.common_frends,self.is_photo_open,self.is_post_open,self.is_community_open,self.is_friend_open,self.is_doc_open,self.is_video_open,self.is_music_open,self.is_good_open,self.user.get_selected_post_list_pk()
        return c
