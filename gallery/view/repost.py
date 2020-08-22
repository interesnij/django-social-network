from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from gallery.models import Photo, Album
from users.models import User
from chat.models import Message
from django.shortcuts import render
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.post_attacher import get_post_attach
from common.processing.post import get_post_processing


class UUCMPhotoWindow(TemplateView):
    """
    форма репоста записи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "photo_repost_window/u_ucm_photo.html"
        return super(UUCMPhotoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMPhotoWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.photo
        context["user"] = self.user
        return context

class CUCMPhotoWindow(TemplateView):
    """
    форма репоста записи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "photo_repost_window/c_ucm_photo.html"
        else:
            Http404
        return super(CUCMPhotoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMPhotoWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.photo
        context["community"] = self.community
        return context


class UUCMPhotoAlbumWindow(TemplateView):
    """
    форма репоста фотоальбома пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.album = Album.objects.get(uuid=self.kwargs["uuid"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "photo_repost_window/u_ucm_photo_album.html.html"
        return super(UUCMPhotoAlbumWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMPhotoAlbumWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["user"] = self.user
        return context

class CUCMPhotoAlbumWindow(TemplateView):
    """
    форма репоста фотоальбома сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "photo_repost_window/c_ucm_photo_album.html"
        else:
            Http404
        return super(CUCMPhotoAlbumWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMPhotoAlbumWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["community"] = self.community
        return context


class UUPhotoRepost(View):
    """
    создание репоста записи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=None, status=Post.PHOTO_REPOST)
            photo.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPhotoRepost(View):
    """
    создание репоста записи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=community, status=Post.PHOTO_REPOST)
            photo.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCPhotoRepost(View):
    """
    создание репоста записи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=photo.creator, community=None, status=Post.PHOTO_REPOST)
            photo.item.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community_with_name(community.name):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCPhotoRepost(View):
    """
    создание репоста записи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=photo.creator, community=community, status=Post.PHOTO_REPOST)
            photo.item.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMPhotoRepost(View):
    """
    создание репоста записи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=photo.creator, community=None, status=Post.PHOTO_REPOST)
            photo.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост фотографии пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMPhotoRepost(View):
    """
    создание репоста записи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=photo.creator, community=community, status=Post.PHOTO_REPOST)
            photo.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост фотографии сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UUPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, community=None, status=Post.PHOTO_ALBUM_REPOST)
            album.post_album.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=playlist.creator, community=community, status=Post.PHOTO_ALBUM_REPOST)
            album.post_album.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=None, status=Post.PHOTO_ALBUM_REPOST)
            album.post_album.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community_with_name(community.name):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=community, status=Post.PHOTO_ALBUM_REPOST)
            album.post_album.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=None, status=Post.PHOTO_ALBUM_REPOST)
            album.post_album.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост фотоальбома пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=playlist.creator, community=community, status=Post.PHOTO_ALBUM_REPOST)
            album.post_album.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост фотоальбома сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
