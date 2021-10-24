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

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_community_list, get_template_anon_community_list

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(community_id=self.community.pk, type=PhotoList.MAIN)
        if request.is_ajax():
            if request.user.is_authenticated:
                self.template_name = get_template_community_list(self.list, "communities/photos/main_list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_community_list(self.list, "communities/photos/main_list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_staff_of_community(self.community.pk):
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(CommunityPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list

class CommunityAlbumPhotosList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_community_list, get_template_anon_community_list

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            if request.user.is_authenticated:
                self.template_name = get_template_community_list(self.list, "communities/photos/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            else:
                self.template_name = get_template_anon_community_list(self.list, "communities/photos/list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        if request.user.is_authenticated and request.user.is_staff_of_community(self.community.pk):
            self.photo_list = self.list.get_staff_items()
        else:
            self.photo_list = self.list.get_items()
        return super(CommunityAlbumPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityAlbumPhotosList,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['list'] = self.list
        return context

    def get_queryset(self):
        photo_list = self.photo_list
        return photo_list


class CommunityAlbumPhotoList(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_community_item, get_template_anon_community_item

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
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
