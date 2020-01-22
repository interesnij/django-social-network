from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.forms import PhotoDescriptionForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


class UserPhotoDescription(View):
    form_image = None
    def post(self,request,*args,**kwargs):
        context = {}
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        form_image = PhotoDescriptionForm(request.POST,instance=photo)
        context['form_image'] = form_image
        if form_image.is_valid() and user == request.user:
            form_image.save()
            return HttpResponse("!")
        else:
            return HttpResponseBadRequest()


class UserPhotoDelete(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.is_deleted = True
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class UserPhotoAbortDelete(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.is_deleted = False
            photo.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class UserOpenCommentPhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserCloseCommentPhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
        return HttpResponse("!")


class UserOnPrivatePhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.is_public = False
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")

class UserOffPrivatePhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.is_public = True
            photo.save(update_fields=['is_public'])
        return HttpResponse("!")


class UserAddAvatarPhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        album = Album.objects.get(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        if user == request.user:
            photo.album_2 = album
            photo.save(update_fields=['album_2'])
        return HttpResponse("!")

class UserRemoveAvatarPhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.album_2 = None
            photo.save(update_fields=['album_2'])
        return HttpResponse("!")
