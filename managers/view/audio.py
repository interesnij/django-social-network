from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from music.models import Music, MusicList
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_audio import AudioManageLog


class AudioCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/audio/audio_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(AudioCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Music.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        audio, form = Music.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=audio.pk, type=26)
            moderate_obj.create_close(object=audio, description=mod.description, manager_id=request.user.pk)
            AudioManageLog.objects.create(item=audio.pk, manager=request.user.pk, action_type=AudioManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AudioCloseDelete(View):
    def get(self,request,*args,**kwargs):
        audio = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=audio.pk, type=26)
            moderate_obj.delete_close(object=audio, manager_id=request.user.pk)
            AudioManageLog.objects.create(item=audio.pk, manager=request.user.pk, action_type=AudioManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class AudioClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.track = Music.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 26, self.track.pk)
        self.template_name = get_staff_template("managers/manage_create/audio/audio_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AudioClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ReportForm

        context = super(AudioClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.track
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        music = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 26, music.pk):
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=26, object_id=music.pk, description=request.POST.get('description'), type=request.POST.get('type'))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AudioRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_moderator():
            music = Music.objects.get(pk=self.kwargs["pk"])
            moderate_obj = Moderated.objects.get(object_id=music.pk, type=26)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            AudioManageLog.objects.create(item=music.pk, manager=request.user.pk, action_type=AudioManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class AudioUnverify(View):
    def get(self,request,*args,**kwargs):
        music = Music.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=music.pk, type=26)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(music, manager_id=request.user.pk)
            AudioManageLog.objects.create(item=obj.object_id, manager=request.user.pk, action_type=AudioManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class ListAudioClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 25, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/audio/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListAudioClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListAudioClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 25, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=25, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListAudioRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=25)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            AudioManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=AudioManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListAudioUnverify(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=25)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            AudioManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=AudioManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListAudioCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/audio/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListAudioCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListAudioCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=25)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            AudioManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=AudioManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListAudioCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=25)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            AudioManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=AudioManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404
