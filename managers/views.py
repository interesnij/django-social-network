from django.views.generic.base import TemplateView
from common.templates import get_detect_platform_template
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views import View
from users.models import User


class ManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SuperManagersView,self).get(request,*args,**kwargs)


class SendManagerMessages(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_administrator():
            self.template_name = get_detect_platform_template("managers/manage_create/message/send_messages.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SendManagerMessages,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        from chat.forms import MessageForm

        form = MessageForm(request.POST, request.FILES)

        if request.is_ajax() and form.is_valid() and request.user.is_administrator():
            from chat.models import Message

            form_post = form.save(commit=False)
            Message.get_or_create_manager_chat_and_send_message(
                creator_pk = request.user.pk,
                text = form_post.text,
                voice = request.POST.get('voice'),
                attach = request.POST.getlist('attach_items')
            )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class SanctionCreate(TemplateView):
    template_name, open_suspend, open_warning_banner, is_admin = None, None, None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_item_of_type, get_comment, get_list_of_type

        self._type = request.GET.get('type')
        self._subtype = request.GET.get('subtype')

        if self._subtype and self._subtype == "comment":
            self.item = get_comment(self._type)
        elif _subtype and _subtype == "planner":
            self.item = get_planner(self._type)
        elif _type[0] == "l":
            self.item = get_list_of_type(self._type)
            open_suspend = True
        elif "use" in self._type:
            from users.models import User
            self.item = User.objects.get(pk=self._type[3:])
            open_suspend, open_warning_banner, is_admin = True, True, True
        elif "com" in self._type:
            from communities.models import Community
            self.item = Community.objects.get(pk=self._type[3:])
            open_suspend, open_warning_banner, is_admin = True, True, True
        else:
            self.item = get_item_of_type(self._type)
            open_suspend, open_warning_banner = True, True

        if (is_admin and request.user.is_administrator()) or request.user.is_moderator():
            self.template_name = get_detect_platform_template("generic/sanction.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SanctionCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SanctionCreate,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["type"] = self._type
        context["subtype"] = self._subtype
        context["open_suspend"] = self.open_suspend
        context["open_warning_banner"] = self.open_warning_banner
        return context

    def post(self, request, *args, **kwargs):
        from django.http import HttpResponse, HttpResponseBadRequest
        from managers.models import Moderated, ModerationReport

        _type = request.POST.get('_type')
        _subtype = request.POST.get('_subtype')

        if _type[0] == "l":
            open_suspend = True
            if _type[:3] == "lpo":
                from posts.models import PostsList
                item, t = PostsList.objects.get(pk=_type[3:]), "POL"
            elif _type[:3] == "lph":
                from gallery.models import PhotoList
                item, t =  PhotoList.objects.get(pk=_type[3:]), "PHL"
            elif _type[:3] == "lgo":
                from goods.models import GoodList
                item, t =  GoodList.objects.get(pk=_type[3:]), "GOL"
            elif _type[:3] == "lvi":
                from video.models import VideoList
                item, t =  VideoList.objects.get(pk=_type[3:]), "VIL"
            elif _type[:3] == "ldo":
                from docs.models import DocsList
                item, t =  DocsList.objects.get(pk=_type[3:]), "DOL"
            elif _type[:3] == "lmu":
                from music.models import MusicList
                item, t =  MusicList.objects.get(pk=_type[3:]), "MUL"
            elif _type[:3] == "lsu":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "SUL"
            elif _type[:3] == "lfo":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "FOL"
            elif _type[:3] == "lar":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "ARL"
            elif _type[:3] == "lwi":
                from survey.models import SurveyList
                item, t =  SurveyList.objects.get(pk=_type[3:]), "WIL"

        elif _subtype and _subtype == "comment":
            if _type[:3] == "pos":
                from posts.models import PostComment
                item, t = PostComment.objects.get(pk=_type[3:]), "CPO"
            elif _type[:3] == "pho":
                from gallery.models import PhotoComment
                item, t =  PhotoComment.objects.get(pk=_type[3:]), "CPH"
            elif _type[:3] == "goo":
                from goods.models import GoodComment
                item, t =  GoodComment.objects.get(pk=_type[3:]), "CGO"
            elif _type[:3] == "vid":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CVI"
            elif _type[:3] == "wik":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CWI"
            elif _type[:3] == "CwC":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CwC"

        elif _subtype and _subtype == "planner":
            if _type[:3] == "WrS":
                from posts.models import PostComment
                item, t = PostComment.objects.get(pk=_type[3:]), "WrS"
            elif type[:3] == "BoA":
                from gallery.models import PhotoComment
                item, t =  PhotoComment.objects.get(pk=_type[3:]), "BoA"
            elif _type[:3] == "CoL":
                from goods.models import GoodComment
                item, t =  GoodComment.objects.get(pk=_type[3:]), "CoL"
            elif _type[:3] == "CaR":
                from video.models import VideoComment
                item, t =  VideoComment.objects.get(pk=_type[3:]), "CaR"

        else:
            if _type[:3] == "pos":
                item, t =  Post.objects.get(pk=_type[3:]), "POS"
            elif _type[:3] == "pho":
                from gallery.models import Photo
                item, t =  Photo.objects.get(pk=_type[3:]), "PHO"
            elif _type[:3] == "goo":
                from goods.models import Good
                item, t =  Good.objects.get(pk=_type[3:]), "GOO"
            elif _type[:3] == "vid":
                from video.models import Video
                item, t =  Video.objects.get(pk=_type[3:]), "VID"
            elif _type[:3] == "doc":
                from docs.models import Doc
                item, t =  Doc.objects.get(pk=_type[3:]), "DOC"
            elif _type[:3] == "mus":
                from music.models import Music
                item, t =  Music.objects.get(pk=_type[3:]), "MUS"
            elif _type[:3] == "sur":
                from survey.models import Survey
                item, t =  Survey.objects.get(pk=_type[3:]), "SUR"
            elif _type[:3] == "mes":
                from chat.models import Message
                item, t =  Message.objects.get(pk=_type[3:]), "CHA"

            elif _type[:3] == "use":
                from users.models import User
                item, t =  User.objects.get(pk=_type[3:]), "USE"
                open_suspend, open_warning_banner, is_admin = True, True, True
            elif _type[:3] == "com":
                from communities.models import Community
                item, t =  Community.objects.get(pk=_type[3:]), "COM"
                open_suspend, open_warning_banner, is_admin = True, True, True
            elif _type[:3] == "sit":
                from music.models import Music
                item, t=  Music.objects.get(pk=_type[3:]), "SIT"
            elif type[:3] == "mai":
                from survey.models import Survey
                item, t =  Survey.objects.get(pk=_type[3:]), "MAI"
            elif _type[:3] == "for":
                from survey.models import Survey
                item, t =  Survey.objects.get(pk=_type[3:]), "FOR"
        if not (is_admin and request.user.is_administrator()) or not request.user.is_moderator():
            return HttpResponseBadRequest()
        if request.is_ajax():
            
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=t, object_id=item.pk, description=post.description, type=post.type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
