from django.views.generic import ListView
from common.templates import get_settings_template, get_community_moders_template
from communities.models import Community
from common.templates import get_default_template


class AllNotifyView(ListView):
    """ Все уведомления пользователя, если он не владеет правами в сообществах """
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/all_notify.html", request.user, request.META['HTTP_USER_AGENT'])
        self.user, self.all_notify = request.user, request.user.get_user_notify()
        return super(AllNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllNotifyView,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

    def get_queryset(self):
        return self.all_notify

class UserNotifyView(ListView):
    """ Все уведомления пользователя, если он владеет правами в сообществах. Будет кнопка "назад" на станницу блоков "Пользователь-сообщество-..." """
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.user, self.template_name, self.all_notify = request.user, get_settings_template("notify/user_notify.html", request.user, request.META['HTTP_USER_AGENT']), request.user.get_user_notify()
        request.user.read_user_notify()
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
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.user, self.template_name, self.all_notify = request.user, get_community_moders_template("notify/community_notify.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT']), self.community.get_community_notify()
        self.community.read_community_notify(self.user.pk)
        return super(CommunityNotifyView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityNotifyView,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["user"] = self.user
        return context

    def get_queryset(self):
        all_notify = self.all_notify
        return all_notify
