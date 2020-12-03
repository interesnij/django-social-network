from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from gallery.models import Photo, Album
from users.models import User
from notify.model.photo import *
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.attach.post_attacher import get_post_attach
from common.processing.post import get_post_processing, repost_message_send, repost_community_send
from common.template.user import get_detect_platform_template


class UUCMPhotoWindow(TemplateView):
    """
    форма репоста записи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("gallery/photo_repost_window/u_ucm_photo.html", request.user, request.META['HTTP_USER_AGENT'])
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
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("gallery/photo_repost_window/c_ucm_photo.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("gallery/photo_repost_window/u_ucm_photo_album.html", request.user, request.META['HTTP_USER_AGENT'])
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
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("gallery/photo_repost_window/c_ucm_photo_album.html", request.user, request.META['HTTP_USER_AGENT'])
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
        repost_community_send(photo, Post.PHOTO_REPOST, None, request)
        return HttpResponse()


class CCPhotoRepost(View):
    """
    создание репоста записи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_community_send(photo, Post.PHOTO_REPOST, community, request)
        return HttpResponse()


class UMPhotoRepost(View):
    """
    создание репоста записи пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(photo, Post.PHOTO_REPOST, None, request, "Репост фотографии пользователя")
        return HttpResponse()


class CMPhotoRepost(View):
    """
    создание репоста записи сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(photo, Post.PHOTO_REPOST, community, request, "Репост фотографии сообщества")
        return HttpResponse()


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
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.PHOTO_ALBUM_REPOST)
            album.post.add(parent)
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
            parent = Post.create_parent_post(creator=album.creator, community=community, status=Post.PHOTO_ALBUM_REPOST)
            album.post.add(parent)
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
        repost_community_send(album, Post.PHOTO_ALBUM_REPOST, None, request)
        return HttpResponse()


class CCPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_community_send(album, Post.PHOTO_ALBUM_REPOST, community, request)
        return HttpResponse()


class UMPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(album, Post.PHOTO_ALBUM_REPOST, None, request, "Репост фотоальбома пользователя")
        return HttpResponse()


class CMPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(album, Post.PHOTO_ALBUM_REPOST, community, request, "Репост фотоальбома сообщества")
        return HttpResponse()
