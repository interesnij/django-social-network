from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from notify.model.item import ItemNotify, ItemCommunityNotify


class ItemNotificationListView(LoginRequiredMixin, ListView):
    model = ItemNotify
    context_object_name = 'notification_list'
    template_name = 'not_item/user_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = ItemNotify.objects.filter(recipient=self.request.user)
        return notify


class ItemCommunityNotificationListView(LoginRequiredMixin, ListView):
    model = ItemCommunityNotify
    context_object_name = 'notification_list'
    template_name = 'not_item/community_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = ItemCommunityNotify.objects.filter(community__creator=self.request.user)
        return notify


@login_required
def item_user_all_read(request):
    request.user.item_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('item_user_all_read')

@login_required
def item_community_all_read(request):
    request.user.item_community_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('item_community_all_read')


@login_required
def item_get_latest_notifications(request):
    notifications = request.user.item_notifications.get_most_recent()
    return render(request, 'not_item/most_recent.html', {'notifications': notifications})
