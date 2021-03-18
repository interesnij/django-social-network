from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from gallery.models import Photo
from users.models import User
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import get_post_processing
from common.notify.notify import *


class UUCMPhotoWindow(TemplateView):
    """
    форма репоста фотографии пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.user import get_detect_platform_template

        self.photo, self.user, self.template_name = Photo.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/u_ucm_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMPhotoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMPhotoWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["user"] = PostForm(), self.photo, self.user
        return context

class CUCMPhotoWindow(TemplateView):
    """
    форма репоста фотографии сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.user import get_detect_platform_template

        self.photo, self.c, self.template_name = Photo.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/c_ucm_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.community)
        return super(CUCMPhotoWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMPhotoWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"] = PostForm(), self.photo, self.c
        return context


class UUCMPhotoAlbumWindow(TemplateView):
    """
    форма репоста фотоальбома пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from gallery.models import Album
        from common.template.user import get_detect_platform_template

        self.album, self.user, self.template_name = Album.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/u_ucm_photo_album.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMPhotoAlbumWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMPhotoAlbumWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["user"] = PostForm(), self.album, self.user
        return context

class CUCMPhotoAlbumWindow(TemplateView):
    """
    форма репоста фотоальбома сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        from gallery.models import Album
        from common.template.user import get_detect_platform_template

        self.album, self.c, self.template_name = Album.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("gallery/repost/c_ucm_photo_album.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.community)
        return super(CUCMPhotoAlbumWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CUCMPhotoAlbumWindow,self).get_context_data(**kwargs)
        c["form"], c["object"], c["community"] = PostForm(), self.album, self.c
        return c


class UUPhotoRepost(View):
    """
    создание репоста фотографии пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=None, attach="pho"+str(photo.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            user_notify(request.user, photo.creator.pk, None, "pho"+photo.pk, "u_photo_repost", "RE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPhotoRepost(View):
    """
    создание репоста фотографии сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=community, attach="pho"+str(photo.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            community_notify(request.user, community, None, "pho"+photo.pk, "c_photo_repost", "RE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCPhotoRepost(View):
    """
    создание репоста фотографии пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, attach="pho"+str(photo.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    user_notify(request.user, photo.creator.pk, community_id, "pho"+photo.pk, "u_photo_repost", 'CR')
        return HttpResponse()


class CCPhotoRepost(View):
    """
    создание репоста фотографии сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=community, attach="pho"+str(photo.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    community_notify(request.user, community, community_id, "pho"+photo.pk, "c_photo_repost", 'CR')
        return HttpResponse()


class UMPhotoRepost(View):
    """
    создание репоста фотографии пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(photo, "pho"+str(photo.pk), None, request, "Репост фотографии пользователя")
        return HttpResponse()


class CMPhotoRepost(View):
    """
    создание репоста фотографии сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from common.processing.post import repost_message_send

        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(photo, "pho"+str(photo.pk), community, request, "Репост фотографии сообщества")
        return HttpResponse()


class UUPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import Album

        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=None, attach="lph"+str(album.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            user_notify(request.user, album.creator.pk, None, "lph"+album.pk, "u_photo_list_repost", "LRE")
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import Album

        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=community, attach="lph"+str(album.pk))
            new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_processing(new_post)
            community_notify(request.user, community, None, "lph"+album.pk, "c_photo_repost", 'LRE')
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UCPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import Album

        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, attach="lph"+str(album.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    user_notify(request.user, album.creator.pk, community_id, "lph"+album.pk, "u_photo_list_repost", 'CLR')
        return HttpResponse()


class CCPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import Album

        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        lists, attach = request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, attach="lph"+str(album.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, attach=attach, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                    get_post_processing(new_post)
                    community_notify(request.user, community, community_id, "lph"+album.pk, "c_photo_list_repost", 'CLR')
        return HttpResponse()


class UMPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import Album
        from common.processing.post import repost_message_send

        album = Album.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(album, "lph"+str(album.pk), None, request, "Репост фотоальбома пользователя")
        return HttpResponse()


class CMPhotoAlbumRepost(View):
    """
    создание репоста фотоальбома сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        from gallery.models import Album
        from common.processing.post import repost_message_send

        album = Album.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(album, "lph"+str(album.pk), community, request, "Репост фотоальбома сообщества")
        return HttpResponse()
