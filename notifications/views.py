from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.http import HttpResponse
from notifications.models import Notification, CommunityNotification
from django.views.generic.base import TemplateView


class UserNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notification_list'
    template_name = 'user_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = Notification.objects.filter(recipient=self.request.user)
        return notify

class CommunityNotificationListView(LoginRequiredMixin, ListView):
    model = CommunityNotification
    context_object_name = 'notification_list'
    template_name = 'community_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = CommunityNotification.objects.filter(community__creator=self.request.user)
        return notify


@login_required
def user_all_read(request):
    request.user.notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('unread')

@login_required
def community_all_read(request):
    request.user.community_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('unread')


@login_required
def get_latest_notifications(request):
    notifications = request.user.notifications.get_most_recent()
    return render(request,
                  'most_recent.html',
                  {'notifications': notifications})

class NotificationCleanView(TemplateView):
    template_name = 'notification_clean.html'


    def get(self,request,*args,**kwargs):
        self.notifications = Notification.objects.filter(recipient=request.user)
        self.notifications.mark_all_as_read()
        return HttpResponse("!")
