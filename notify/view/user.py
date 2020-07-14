from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from notify.model.user import UserNotify, UserCommunityNotify


class UserNotificationListView(LoginRequiredMixin, ListView):
    model = UserNotify
    context_object_name = 'notification_list'
    template_name = 'not_user/user_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = UserNotify.objects.filter(recipient=self.request.user)
        return notify


class CommunityNotificationListView(LoginRequiredMixin, ListView):
    model = UserCommunityNotify
    context_object_name = 'notification_list'
    template_name = 'not_user/community_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = UserCommunityNotify.objects.filter(community__creator=self.request.user)
        return notify


@login_required
def user_all_read(request):
    request.user.user_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('user_all_read')

@login_required
def community_all_read(request):
    request.user.community_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('community_all_read')


@login_required
def get_latest_notifications(request):
    notifications = request.user.user_notifications.get_most_recent()
    return render(request, 'not_user/most_recent.html', {'notifications': notifications})
