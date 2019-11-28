from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.helpers import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import ListView
from gallery.forms import AlbumForm, AvatarUserForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from generic.mixins import EmojiListMixin
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied


class UserPhoto(EmojiListMixin, TemplateView):
    template_name="gallery_user/photo.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.avatar_album = Album.objects.get(creator=self.user, title="Фото со страницы", is_generic=True)
        try:
            self._avatar = Photo.objects.filter(album_2=self.avatar_album).order_by('-id')[0]
            if self._avatar.id == self.photo.id:
                self.avatar = True
            else:
                self.avatar = None
        except:
            self.avatar = None
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.photos = self.user.get_photos()
        elif self.user == request.user and request.user.is_authenticated:
            self.photos = self.user.get_photos()
        elif self.user.is_closed_profile() and request.user.is_anonymous:
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.photos = self.user.get_photos()
        self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return super(UserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPhoto,self).get_context_data(**kwargs)
        context["object"]=self.photo
        context["user"]=self.user
        context["next"]=self.next
        context["prev"]=self.prev
        context["avatar"]=self.avatar
        return context


class UserDetailAvatar(EmojiListMixin, TemplateView):
    template_name="gallery_user/photo.html"

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.photos = self.user.get_avatar_photos()
        elif self.user == request.user and request.user.is_authenticated:
            self.photos = self.user.get_avatar_photos()
            self.avatar_album = Album.objects.get(creator_id=self.id, title="Фото со страницы", is_generic=True)
            self.photos_query = Q(creator_id=self.user.id, is_deleted=False, community=None, album_2=avatar_album)
            self.exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
            self.photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
            self.photos = Photo.objects.filter(photos_query)
        elif self.user.is_closed_profile() and request.user.is_anonymous:
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.photos = self.user.get_avatar_photos()
        self.next = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        self.prev = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        return super(UserDetailAvatar,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserDetailAvatar,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context
