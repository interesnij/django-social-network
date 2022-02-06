from music.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import TrackForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import get_settings_template, render_for_platform
from common.check.user import check_user_can_get_list


class UserTrackRemove(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator.pk == request.user.pk:
            track.delete_track(None)
            return HttpResponse()
        else:
            raise Http404
class UserTrackAbortRemove(View):
    def get(self,request,*args,**kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator == request.user:
            track.restore_track(None)
            return HttpResponse()
        else:
            raise Http404

class UserTrackEdit(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("music/music_create/u_edit_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserTrackEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserTrackEdit,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm(instance=self.track)
        context["track"] = self.track
        return context

    def post(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["pk"])
        form_post = TrackForm(request.POST, request.FILES, instance=self.track)

        if request.is_ajax() and form_post.is_valid():
            _track = form_post.save(commit=False)
            new_doc = self.track.edit_track(title=_track.title, file=_track.file, lists=request.POST.getlist("list"))
            return render_for_platform(request, 'music/music_create/u_new_track.html',{'object': self.track})
        else:
            return HttpResponseBadRequest()
