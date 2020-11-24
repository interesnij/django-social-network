from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from notify.model.good import GoodNotify, GoodCommunityNotify
from common.template.user import get_settings_template


class GoodNotificationListView(LoginRequiredMixin, ListView):
    model = GoodNotify
    context_object_name = 'notification_list'
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/good/user_notify_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodNotificationListView,self).get(request,*args,**kwargs)

    def get_queryset(self, **kwargs):
        notify = GoodNotify.objects.filter(recipient=self.request.user)
        return notify


class GoodCommunityNotificationListView(LoginRequiredMixin, ListView):
    model = GoodCommunityNotify
    context_object_name = 'notification_list'
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/good/community_notify_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodCommunityNotify,self).get(request,*args,**kwargs)

    def get_queryset(self, **kwargs):
        notify = GoodCommunityNotify.objects.filter(community__creator=self.request.user)
        return notify


class GoodLastNotify(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/good/most_recent.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodLastNotify,self).get(request,*args,**kwargs)

    def get_queryset(self):
        notifications = self.request.user.good_notifications.get_most_recent()
        return notifications
