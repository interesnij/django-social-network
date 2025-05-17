from django.views.generic.base import TemplateView
from communities.models import Community
from gallery.models import PhotoList, Photo
from django.views.generic import ListView
from django.http import Http404
from django.views import View
from rest_framework.exceptions import PermissionDenied
from common.check.community import check_can_get_lists
from gallery.forms import PhotoDescriptionForm


class GetCommunityPhoto(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_detect_platform_template

        self.photo = Photo.objects.get(pk=self.kwargs["pk"])
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            self.template_name = get_detect_platform_template("gallery/c_photo/preview/admin_photo.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GetCommunityPhoto,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GetCommunityPhoto,self).get_context_data(**kwargs)
        context["object"] = self.photo
        context["user_form"] = PhotoDescriptionForm(instance=self.photo)
        return context
