from django.views.generic.base import TemplateView
from users.models import User
import re


class MainManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.template_name = "managers.html"
        return super(MainManagersView,self).get(request,*args,**kwargs)

class ManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_user_administrator() or self.user.is_community_administrator() or self.user.is_post_administrator() or self.user.is_good_administrator() or self.user.is_photo_administrator() or self.user.is_audio_administrator() or self.user.is_video_administrator():
            self.template_name = "manager/admins.html"
        elif self.user.is_user_advertiser() or self.user.is_community_advertiser():
            self.template_name = "manager/advertisers.html"
        elif self.user.is_user_editor() or self.user.is_community_editor() or self.user.is_post_editor() or self.user.is_good_editor() or self.user.is_photo_editor() or self.user.is_audio_editor() or self.user.is_video_editor():
            self.template_name = "manager/editors.html"
        elif self.user.is_user_moderator() or self.user.is_community_moderator() or self.user.is_post_moderator() or self.user.is_good_moderator() or self.user.is_photo_moderator() or self.user.is_audio_moderator() or self.user.is_video_moderator():
            self.template_name = "manager/moderators.html"
        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_supermanager:
            self.template_name = "manager/supermanager.html"
        else:
            self.template_name = "about.html"
        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name += "mob_"
        return super(SuperManagersView,self).get(request,*args,**kwargs)
