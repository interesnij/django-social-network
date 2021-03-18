from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from video.models import Video, VideoAlbum
from users.models import User
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import get_post_processing, repost_message_send
from common.template.user import get_detect_platform_template
from common.notify.notify import *


class UUCMVideoWindow(TemplateView):
    """
    форма репоста видеозаписи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("video/repost/u_ucm_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UUCMVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMVideoWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.video
        context["user"] = self.user
        return context

class CUCMVideoWindow(TemplateView):
    """
    форма репоста видеозаписи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("video/repost/c_ucm_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CUCMVideoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMVideoWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.video
        context["community"] = self.community
        return context


class UUCMVideoAlbumWindow(TemplateView):
    """
    форма репоста видеоальбома пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("video/repost/u_ucm_video_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UUCMVideoAlbumWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMVideoAlbumWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["user"] = self.user
        return context

class CUCMVideoAlbumWindow(TemplateView):
    """
    форма репоста видеоальбома сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("video/repost/c_ucm_video_album.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CUCMVideoAlbumWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMVideoAlbumWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["community"] = self.community
        return context


class UUVideoRepost(View):
    """
    создание репоста видеозаписи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=None, attach="vid"+str(video.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            user_notify(request.user, video.creator.pk, None, "vid"+video.pk, "u_video_repost", "RE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUVideoRepost(View):
    """
    создание репоста видеозаписи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=community, attach="vid"+str(video.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            community_notify(request.user, community, None, "vid"+video.pk, "c_video_repost", 'RE')
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCVideoRepost(View):
    """
    создание репоста видеозаписи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        lists = request.POST.getlist("lists")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=community, attach="vid"+str(video.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    user_notify(request.user, video.creator.pk, community_id, "vid"+video.pk, "u_video_repost", 'CR')
        return HttpResponse()


class CCVideoRepost(View):
    """
    создание репоста видеозаписи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        lists = request.POST.getlist("lists")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=community, attach="vid"+str(video.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    community_notify(request.user, community, community_id, "vid"+video.pk, "c_video_repost", 'CR')
        return HttpResponse()


class UMVideoRepost(View):
    """
    создание репоста видеозаписи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(video, "vid"+str(video.pk), None, request, "Репост видеозаписи пользователя")
        return HttpResponse()


class CMVideoRepost(View):
    """
    создание репоста видеозаписи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(video, "vid"+str(video.pk), community, request, "Репост видеозаписи сообщества")
        return HttpResponse()


class UUVideoAlbumRepost(View):
    """
    создание репоста видеоальбома пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=None, attach="lvi"+str(album.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            user_notify(request.user, album.creator.pk, None, "vid"+album.pk, "u_video_list_repost", "LRE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUVideoAlbumRepost(View):
    """
    создание репоста видеоальбома сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=community, attach="lvi"+str(album.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            community_notify(request.user, community, None, "vid"+album.pk, "c_video_list_repost", 'LRE')
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCVideoAlbumRepost(View):
    """
    создание репоста видеоальбома пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        lists = request.POST.getlist("lists")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=community, attach="lvi"+str(album.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    user_notify(request.user, album.creator.pk, community_id, "vid"+album.pk, "u_video_list_repost", 'CLR')
        return HttpResponse()


class CCVideoAlbumRepost(View):
    """
    создание репоста видеоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        lists = request.POST.getlist("lists")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=community, attach="lvi"+str(album.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    community_notify(request.user, community, community_id, "vid"+album.pk, "c_video_list_repost", 'CLR')
        return HttpResponse()


class UMVideoAlbumRepost(View):
    """
    создание репоста видеоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(album, "lvi"+str(album.pk), None, request, "Репост видеоальбома пользователя")
        return HttpResponse()


class CMVideoAlbumRepost(View):
    """
    создание репоста видеоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(album, "lvi"+str(album.pk), community, request, "Репост видеоальбома сообщества")
        return HttpResponse()
