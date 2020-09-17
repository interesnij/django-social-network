from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from video.models import Video, VideoAlbum
from users.models import User
from chat.models import Message
from django.shortcuts import render
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.post_attacher import get_post_attach
from common.processing.post import get_post_processing, get_post_message_processing


class UUCMVideoWindow(TemplateView):
    """
    форма репоста видеозаписи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.video = Video.objects.get(uuid=self.kwargs["uuid"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "video_repost_window/u_ucm_video.html"
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
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "video_repost_window/c_ucm_video.html"
        else:
            Http404
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
        if request.user.is_authenticated:
            self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "video_repost_window/u_ucm_video_album.html"
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
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "video_repost_window/c_ucm_video_album.html"
        else:
            Http404
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
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=None, status=Post.VIDEO_REPOST)
            video.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
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
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=video.creator, community=community, status=Post.VIDEO_REPOST)
            video.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
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
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=video.creator, community=None, status=Post.VIDEO_REPOST)
            video.item.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community_with_name(community.name):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCVideoRepost(View):
    """
    создание репоста видеозаписи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=video.creator, community=community, status=Post.VIDEO_REPOST)
            video.item.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMVideoRepost(View):
    """
    создание репоста видеозаписи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=video.creator, community=None, status=Post.VIDEO_REPOST)
            video.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_message_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост видеозаписи пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMVideoRepost(View):
    """
    создание репоста видеозаписи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=video.creator, community=community, status=Post.VIDEO_REPOST)
            video.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_message_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост видеозаписи сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


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
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.VIDEO_LIST_REPOST)
            album.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
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
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=community, status=Post.VIDEO_LIST_REPOST)
            album.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
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
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.VIDEO_LIST_REPOST)
            album.post.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community_with_name(community.name):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCVideoAlbumRepost(View):
    """
    создание репоста видеоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=album.creator, community=community, status=Post.VIDEO_LIST_REPOST)
            album.post.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMVideoAlbumRepost(View):
    """
    создание репоста видеоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.VIDEO_LIST_REPOST)
            album.post.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_message_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост видеоальбома пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMVideoAlbumRepost(View):
    """
    создание репоста видеоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=album.creator, community=community, status=Post.VIDEO_LIST_REPOST)
            album.post.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_message_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост видеоальбома сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
