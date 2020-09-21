import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from common.template.photo import get_template_user_photo, get_permission_user_photo, get_permission_user_photo_detail
from django.http import Http404
from gallery.forms import PhotoDescriptionForm


class UserPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "user_gallery/", "list.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        photo_list = self.user.get_photos().order_by('-created')
        return photo_list

class UserAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "user_album/", "list.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        photo_list = self.album.get_photos().order_by('-created')
        return photo_list


class UserPhoto(TemplateView):
    """
    страница фото, не имеющего альбома для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album.creator, "u_photo/photo/", "photo.html", request.user)
        else:
            raise Http404

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["album"] = self.album
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(uuid=self.kwargs["uuid"])
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.album.creator, "u_photo/album_photo/", "photo.html", request.user)
        else:
            raise Http404

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserAlbumPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["album"] = self.album
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class UserWallPhoto(TemplateView):
    """
    страница отдельного фото альбома пользователя "Фото со стены"
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.WALL, community=None)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo_detail(self.user, self.photo, "u_photo/wall_photo/", "photo.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWallPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["album"] = self.album
        context["user"] = self.user
        return context


class UserDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.AVATAR, community=None)
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "u_photo/avatar/", "photo.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.user
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["album"] = self.album
        return context

class UserFirstAvatar(TemplateView):
    """
    страница аватара пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = Album.objects.get(creator=self.user, type=Album.AVATAR, community=None)
        self.photo = self.album.get_first_photo()
        self.photos = self.album.get_photos()
        if request.is_ajax():
            self.template_name = get_permission_user_photo(self.user, "u_photo/avatar/", "photo.html", request.user)
        else:
            raise Http404
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(UserFirstAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserFirstAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        context["album"] = self.album
        context["user"] = self.user
        return context
