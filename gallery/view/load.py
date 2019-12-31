from django.views.generic.base import TemplateView
from users.models import User
from main.models import ItemComment
from gallery.models import Album, Photo
from django.http import HttpResponse, HttpResponseBadRequest
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied


class UserPhoto(TemplateView):
    """
    страница отдельного фото в списке или везде для пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.photos = self.user.get_photos()
            self.template_name="photo_user/photo/photo.html"
        elif self.user == request.user and request.user.is_authenticated:
            self.photos = self.user.get_my_photos()
            self.template_name="photo_user/photo/my_photo.html"
        elif self.user.is_closed_profile() and request.user.is_anonymous:
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.photos = self.user.get_photos()
            self.template_name="photo_user/photo/anon_photo.html"
        self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user"]=self.user
        context["next"]=self.next
        context["prev"]=self.prev
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
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.photos = self.user.get_photos_for_album(album_id=self.album.pk)
            self.template_name="photo_user/photo/photo.html"
        elif self.user == request.user and request.user.is_authenticated:
            self.photos = self.user.get_photos_for_my_album(album_id=self.album.pk)
            self.template_name="photo_user/photo/my_photo.html"
        elif self.user.is_closed_profile() and request.user.is_anonymous:
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.photos = self.user.get_photos_for_album(album_id=self.album.pk)
            self.template_name="photo_user/photo/anon_photo.html"
        self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return super(UserAlbumPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserAlbumPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user"]=self.user
        context["next"]=self.next
        context["prev"]=self.prev
        return context


class UserCommentPhoto(TemplateView):
    """
    страница отдельного фото комментария к записям пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
            self.template_name="photo_user/photo/photo.html"
        elif self.user == request.user and request.user.is_authenticated:
            self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
            self.template_name="photo_user/photo/my_photo.html"
        elif self.user.is_closed_profile() and request.user.is_anonymous:
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
            self.template_name="photo_user/photo/anon_photo.html"
        return super(UserCommentPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserCommentPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        return context


class UserDetailAvatar(TemplateView):
    """
    страница отдельного фото аватаров (альбом "Фото со страницы") пользователя с разрещениями и без
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.avatar_photos = self.user.get_avatar_photos()
            self.template_name="photo_user/photo/photo.html"
        elif self.user == request.user and request.user.is_authenticated:
            self.avatar_photos = self.user.get_avatar_photos()
            self.template_name="photo_user/photo/my_photo.html"
        elif self.user.is_closed_profile() and request.user.is_anonymous:
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.avatar_photos = self.user.get_avatar_photos()
            self.template_name="photo_user/photo/anon_photo.html"
        self.next = self.avatar_photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        self.prev = self.avatar_photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context
