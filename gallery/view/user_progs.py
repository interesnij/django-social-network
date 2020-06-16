from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import Album, Photo
from gallery.forms import PhotoDescriptionForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.utils import is_mobile


class UserPhotoDescription(TemplateView):
    template_name = "photo_user/photo/my_photo.html"
    form_image=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.form_image=PhotoDescriptionForm(instance=self.photo)
        return super(UserPhotoDescription,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        self.form_image=PhotoDescriptionForm(request.POST, instance=self.photo)
        if self.form_image.is_valid():
            self.form_image.save()
            if request.is_ajax():
                return HttpResponse ('!')
        return super(UserPhotoDescription,self).post(request,*args,**kwargs)

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
        try:
            album = Album.objects.get(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        except:
            album = Album.objects.create(creator=user, community=None, title="Фото со страницы",  is_generic=True,)
        if user == request.user:
            photo.save(update_fields=['album'])
        return HttpResponse("!")

class UserRemoveAvatarPhoto(View):
    success_url = "/"
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if user == request.user:
            photo.album = None
            try:
                album = Album.objects.get(creator=user, community=None, title="Сохраненные фото",  is_generic=True,)
            except:
                album = Album.objects.create(creator=user, community=None, title="Сохраненные фото",  is_generic=True,)
            photo.album = album
            photo.save()
        return HttpResponse("!")
