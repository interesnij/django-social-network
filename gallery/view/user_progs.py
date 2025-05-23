from users.models import User
from gallery.models import PhotoList, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.user import check_user_can_get_list
from users.models import User
from common.templates import get_settings_template, render_for_platform
from django.views.generic.base import TemplateView


class UserAddAvatar(View):
    """
    загрузка аватара пользователя
    """
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and user == request.user:
            photo_input = request.FILES.get('file')
            _list = PhotoList.objects.get(creator=user, type=PhotoList.AVATAR, community__isnull=True)
            photo = Photo.create_photo(creator=user, image=photo_input, list=_list, type="PHAVA", community=None)
            request.user.create_s_avatar(photo_input)
            request.user.create_b_avatar(photo_input)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoAttachUserCreate(View):
    def post(self, request, *args, **kwargs):
        photos = []
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            list = PhotoList.objects.get(creator=request.user, type="WAL", community=None)
            for p in request.FILES.getlist('file'):
                photo = Photo.create_photo(creator=request.user, image=p, list=list, type="PHWAL", community=None)
                photos += [photo,]
            return render_for_platform(request, 'gallery/new_photos.html',{'object_list': photos, 'list': list})
        else:
            raise Http404

class UserPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_image.is_valid() and photo.creator.pk == request.user.pk:
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class UserPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user:
            photo.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserPhotoRecover(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user:
            photo.restore_item()
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user:
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user:
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user:
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user:
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404


class UserRemoveAvatarPhoto(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and user.pk == request.user.pk:
            photo.list = None
            list = PhotoList.objects.get(creator=user, community__isnull=True, type=PhotoList.AVATAR)
            photo.list = list
            photo.save()
            return HttpResponse()
        else:
            raise Http404
