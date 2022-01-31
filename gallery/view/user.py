from django.views.generic.base import TemplateView
from users.models import User
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from gallery.forms import PhotoDescriptionForm
from common.templates import get_detect_platform_template


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
