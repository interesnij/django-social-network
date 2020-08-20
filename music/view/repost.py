from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from music.models import SoundList, SoundcloudParsing
from users.models import User
from chat.models import Message
from django.shortcuts import render
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.post_attacher import get_post_attach
from common.processing.post import get_post_processing


class UUCMMusicWindow(TemplateView):
    """
    форма репоста аудиозаписи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "music_repost_window/u_ucm_music.html"
        return super(UUCMMusicWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMMusicWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.track
        context["user"] = self.user
        return context

class CUCMMusicWindow(TemplateView):
    """
    форма репоста аудиозаписи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "music_repost_window/c_ucm_music.html"
        else:
            Http404
        return super(CUCMMusicWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMMusicWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.track
        context["community"] = self.community
        return context

class UUCMMusicListWindow(TemplateView):
    """
    форма репоста плейлиста пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "music_repost_window/u_ucm_list_music.html"
        return super(UUCMMusicListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMMusicListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.playlist
        context["user"] = self.user
        return context

class CUCMMusicListWindow(TemplateView):
    """
    форма репоста плейлиста сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "music_repost_window/c_ucm_list_music.html"
        else:
            Http404
        return super(CUCMMusicListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMMusicListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.playlist
        context["community"] = self.community
        return context


class UUMusicRepost(View):
    """
    создание репоста записи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=user, community=None, status=Post.MUSIC_REPOST)
            track.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status=Post.STATUS_PROCESSING)
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUMusicRepost(View):
    """
    создание репоста записи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=request.user, community=community, status=Post.MUSIC_REPOST)
            track.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCMusicRepost(View):
    """
    создание репоста записи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=user, community=None, status=Post.MUSIC_REPOST)
            track.item.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community_with_name(community.name):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCMusicRepost(View):
    """
    создание репоста записи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=request.user, community=community, status=Post.MUSIC_REPOST)
            track.item.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMMusicRepost(View):
    """
    создание репоста записи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=user, community=None, status=Post.MUSIC_REPOST)
            track.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост записи со стены пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMMusicRepost(View):
    """
    создание репоста записи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["track_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=request.user, community=community, status=Post.MUSIC_REPOST)
            track.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост записи со стены сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UUMusicListRepost(View):
    """
    создание репоста плейлиста пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, community=None, status=Post.MUSIC_LIST_REPOST)
            playlist.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUMusicListRepost(View):
    """
    создание репоста плейлиста сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, community=community, status=Post.MUSIC_LIST_REPOST)
            playlist.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCMusicListRepost(View):
    """
    создание репоста плейлиста пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=None, status=Post.MUSIC_LIST_REPOST)
            playlist.post.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community_with_name(community.name):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCMusicListRepost(View):
    """
    создание репоста плейлиста сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=community, status=Post.MUSIC_LIST_REPOST)
            playlist.post.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMMusicListRepost(View):
    """
    создание репоста плейлиста пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=None, status=Post.MUSIC_LIST_REPOST)
            playlist.post.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост записи со стены пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMMusicListRepost(View):
    """
    создание репоста плейлиста сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=community, status=Post.MUSIC_LIST_REPOST)
            playlist.post.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост записи со стены сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
