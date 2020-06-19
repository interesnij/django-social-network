from django.views.generic.base import TemplateView
from users.models import User
from posts.models import PostComment
from gallery.models import Album, Photo
from django.http import HttpResponse, HttpResponseBadRequest
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from gallery.forms import PhotoDescriptionForm
from common.utils import is_mobile
from communities.models import Community


class UserPhoto(TemplateView):
    """
    страница отдельного фото в списке или везде для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.photos = self.user.get_photos()
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_permission_list_user(folder="photo_user/", template="photo.html", request=request)
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user"]=self.user
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["form_image"]=PhotoDescriptionForm(instance=self.photo)
        return context


class UserAlbumPhoto(TemplateView):
    """
    страница отдельного фото в альбоме для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        self.album=Album.objects.get(uuid=self.kwargs["album_uuid"])
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.photos = self.user.get_photos_for_my_album(album_id=self.album.pk)
        self.template_name = self.user.get_permission_list_user(folder="album_photo_user/", template="photo.html", request=request)
        return super(UserAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserAlbumPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["album"]=self.album
        context["user"]=self.user
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["form_image"]=PhotoDescriptionForm(instance=self.photo)
        return context


class UserWallPhoto(TemplateView):
    """
    страница отдельного фото альбома пользователя "Фото со стены"
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.album=Album.objects.get(creator_id=self.user.pk, is_generic=True, community=None, title="Фото со стены")
        self.photos = request.user.get_photos_for_my_album(album_id=self.album.pk)
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_permission_list_user(folder="photo_user/", template="wall_photo.html", request=request)
        return super(UserWallPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserWallPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        context["avatar"]=self.photo.is_avatar(self.request.user)
        context["next"]=self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"]=self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return context


class UserDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.avatar_photos = self.user.get_avatar_photos()
        self.template_name = self.user.get_permission_list_user(folder="photo_user/", template="photo.html", request=request)
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.user
        context["next"] = self.avatar_photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.avatar_photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        return context

class CommunityDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community =  Community.objects.get(pk=self.kwargs["pk"])
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.form_image = PhotoDescriptionForm(request.POST,instance=self.photo)
        self.avatar_photos = self.community.get_avatar_photos()
        self.template_name = self.community.get_template_list(folder="photo_community/", template="photo.html", request=request)
        return super(CommunityDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.community
        context["next"] = self.avatar_photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.avatar_photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["user_form"]=PhotoDescriptionForm(instance=self.photo)
        return context
