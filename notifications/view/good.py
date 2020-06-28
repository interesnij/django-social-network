from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from notifications.model.good import GoodNotification, GoodCommunityNotification


class GoodNotificationListView(LoginRequiredMixin, ListView):
    model = GoodNotification
    context_object_name = 'notification_list'
    template_name = 'not_good/user_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = GoodNotification.objects.filter(recipient=self.request.user)
        return notify


class GoodCommunityNotificationListView(LoginRequiredMixin, ListView):
    model = GoodCommunityNotification
    context_object_name = 'notification_list'
    template_name = 'not_good/community_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = GoodCommunityNotification.objects.filter(community__creator=self.request.user)
        return notify


@login_required
def good_user_all_read(request):
    request.user.good_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('good_user_all_read')

@login_required
def good_community_all_read(request):
    request.user.good_community_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('good_community_all_read')


@login_required
def good_get_latest_notifications(request):
    notifications = request.user.good_notifications.get_most_recent()
    return render(request, 'not_good/most_recent.html', {'notifications': notifications})
