from gallery.models import PhotoList, Photo, PhotoComment
from gallery.forms import PhotoDescriptionForm, CommentForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from common.check.community import check_can_get_lists
from communities.models import Community
from common.templates import render_for_platform, get_community_manage_template
from django.views.generic.base import TemplateView


class CommunityAddAvatar(View):
    """
    загрузка аватара сообщества
    """
    def post(self, request, *args, **kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.user.is_administrator_of_community(community.pk):
            photo_input = request.FILES.get('file')
            _list = PhotoList.objects.get(community=community, type=PhotoList.AVATAR)
            photo = Photo.create_photo(creator=request.user, image=photo_input, list=_list, type="PHAVA", community=community)
            community.create_s_avatar(photo_input)
            community.create_b_avatar(photo_input)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityPhotoDescription(View):
    form_image = None

    def post(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["pk"])
        community = photo.community
        form_image = PhotoDescriptionForm(request.POST, instance=photo)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and form_image.is_valid() and request.user.is_administrator_of_community(community.pk):
            form_image.save()
            return HttpResponse(form_image.cleaned_data["description"])
        else:
            raise Http404


class CommunityPhotoDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityPhotoRecover(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.restore_item()
            return HttpResponse()
        else:
            raise Http404


class CommunityOpenCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.comments_enabled = True
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCommentPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.comments_enabled = False
            photo.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.votes_on = False
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesPhoto(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(pk=self.kwargs["photo_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and photo.creator == request.user or request.user.is_administrator_of_community(community.pk):
            photo.votes_on = True
            photo.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404
