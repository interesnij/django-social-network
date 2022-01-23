from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from gallery.forms import PhotoDescriptionForm
from common.templates import get_detect_platform_template


class UserPhotosList(ListView):
    template_name = None
    paginate_by = 15
    is_user_can_see_photo_section = None
    is_user_can_see_photo_list = None
    is_user_can_create_photos = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_list, get_template_anon_user_list

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(creator_id=self.user.pk, type=PhotoList.MAIN, community__isnull=True)

        if self.user.pk == request.user.pk:
            if request.user.pk == self.list.creator.pk:
                self.is_user_can_see_photo_section = True
                self.is_user_can_see_photo_list = True
                self.is_user_can_create_photos = True
            else:
                self.is_user_can_see_photo_section = True
                self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
                self.is_user_can_create_tracks = self.list.is_user_can_create_el(request.user.pk)
        else:
            self.is_user_can_see_photo_section = self.user.is_user_can_see_photo(request.user.pk)
            self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/photos/main_list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_photo_section = self.user.is_anon_user_can_see_photo()
            self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
        else:
            self.template_name = get_template_user_list(self.list, "users/photos/main_list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])

        return super(UserPhotosList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['list'] = self.list
        context['is_user_can_see_photo_section'] = self.is_user_can_see_photo_section
        context['is_user_can_see_photo_list'] = self.is_user_can_see_photo_list
        context['is_user_can_create_photos'] = self.is_user_can_create_photos
        return context

    def get_queryset(self):
        return self.list.get_items()

class UserPhotosAlbumList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_template_user_list, get_template_anon_user_list

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.list = PhotoList.objects.get(pk=self.kwargs["list_pk"])
        if self.user.pk == request.user.pk:
            if request.user.pk == self.list.creator.pk:
                self.is_user_can_see_photo_section = True
                self.is_user_can_see_photo_list = True
                self.is_user_can_create_photos = True
            else:
                self.is_user_can_see_photo_section = True
                self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
                self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
        else:
            self.is_user_can_see_photo_section = self.user.is_user_can_see_photo(request.user.pk)
            self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
            self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
        if request.user.is_anonymous:
            self.template_name = get_template_anon_user_list(self.list, "users/photos/list/anon_photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
            self.is_user_can_see_photo_section = self.user.is_anon_user_can_see_photo()
            self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
        else:
            self.template_name = get_template_user_list(self.list, "users/photos/list/", "photo_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPhotosAlbumList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPhotosAlbumList,self).get_context_data(**kwargs)
        context['user'] = self.user
        #context['list'] = self.list
        context['is_user_can_see_photo_section'] = self.is_user_can_see_photo_section
        context['is_user_can_see_photo_list'] = self.is_user_can_see_photo_list
        context['is_user_can_create_photos'] = self.is_user_can_create_photos
        return context

    def get_queryset(self):
        return self.list.get_items()

class UserCommentPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import PostComment
        from common.templates import get_template_user_item, get_template_anon_user_item

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.photo, "gallery/u_photo/comment_photo/", "photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.photo, "gallery/u_photo/comment_photo/anon_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCommentPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCommentPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user"] = self.request.user
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context


class GetUserPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            self.template_name = get_detect_platform_template("gallery/u_photo/preview/my_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GetUserPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GetUserPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
