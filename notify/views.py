from django.views import View
from music.models import *
from django.views.generic import ListView
from common.template.user import get_settings_template
from common.template.community import get_community_moders_template


class AllNotifyView(ListView):
    """ Все уведомления пользователя, если он не владеет правами в сообществах """
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        self.template_name = get_settings_template("notify/all_notify.html", self.user, request.META['HTTP_USER_AGENT'])
        self.all_notify = self.user.get_user_notify()
        if not self.user.is_staffed_user():
            self.user.read_user_notify()
        return super(AllNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllNotifyView,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        all_notify = self.all_notify
        return all_notify

class UserNotifyView(ListView):
    """ Все уведомления пользователя, если он владеет правами в сообществах. Будет кнопка "назад" на станницу блоков "Пользователь-сообщество-..." """
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.user = request.user
        self.template_name = get_settings_template("notify/user_notify.html", self.user, request.META['HTTP_USER_AGENT'])
        self.all_notify = self.user.get_user_notify()
        self.user.read_user_notify()
        return super(UserNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserNotifyView,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        all_notify = self.all_notify
        return all_notify


class CommunityNotifyView(ListView):
    """ Все уведомления сообщества, если текущий пользователь владеет правами в сообществах. Будет кнопка "назад" на станницу блоков "Пользователь-сообщество-..." """
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.user = request.user
        self.template_name = get_community_moders_template("notify/community_notify.html", self.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        self.all_notify = self.community.get_community_notify()
        return super(CommunityNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityNotifyView,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["user"] = self.user
        return context

    def get_queryset(self):
        all_notify = self.all_notify
        return all_notify
