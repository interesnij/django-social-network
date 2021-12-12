from django.views.generic.base import TemplateView
from communities.models import Community
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from rest_framework.exceptions import PermissionDenied
from common.check.community import check_can_get_lists
from gallery.forms import PhotoDescriptionForm


class CommunityPhotosList(ListView):
    template_name = None
    paginate_by = 15
    is_user_can_see_photo_section = None
    is_user_can_see_photo_list = None
    is_user_can_create_photos = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_community_list, get_template_anon_community_list

        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(community_id=self.c.pk, type=PhotoList.MAIN)
        if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
            self.is_user_can_see_photo_section = True
            self.is_user_can_create_photos = True
            self.is_user_can_see_photo_list = True
            self.template_name = get_template_community_list(self.list, "communities/photo/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        elif request.user.is_anonymous:
            self.template_name = get_template_anon_community_list(self.list, "communities/photo/list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_photo_section = self.c.is_anon_user_can_see_photo()
            self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
        else:
            self.is_user_can_see_photo_section = self.c.is_user_can_see_photo(request.user.pk)
            self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
            self.template_name = get_template_community_list(self.list, "communities/photo/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPhotosList,self).get_context_data(**kwargs)
        context['is_user_can_see_photo_section'] = self.is_user_can_see_photo_section
        context['is_user_can_see_photo_list'] = self.is_user_can_see_photo_list
        context['is_user_can_create_photos'] = self.is_user_can_create_photos
        context['community'] = self.c
        return context

    def get_queryset(self):
        return self.list.get_items()


class CommunityAlbumPhotoList(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_community_item, get_template_anon_community_item

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.photo, "gallery/c_photo/list_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.photo, "gallery/c_photo/list_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        if request.user.is_authenticated and request.user.is_administrator_of_community(self.list.community.pk):
            self.photos = self.list.get_staff_items()
        else:
            self.photos = self.list.get_items()
        return super(CommunityAlbumPhotoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumPhotoList,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["community"] = self.list.community
        context["list"] = self.list
        context["next"] = self.photos.filter(pk__gt=self.photo.pk).order_by('pk').first()
        context["prev"] = self.photos.filter(pk__lt=self.photo.pk).order_by('-pk').first()
        context["avatar"] = self.photo.is_avatar(self.request.user)
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context

class GetCommunityPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            self.template_name = get_detect_platform_template("gallery/c_photo/preview/admin_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GetCommunityPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GetCommunityPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
