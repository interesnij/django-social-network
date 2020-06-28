from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from notifications.model.photo import PhotoNotification, PhotoCommunityNotification


class PhotoNotificationListView(LoginRequiredMixin, ListView):
    model = PhotoNotification
    context_object_name = 'notification_list'
    template_name = 'not_photo/user_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = PhotoNotification.objects.filter(recipient=self.request.user)
        return notify


class PhotoCommunityNotificationListView(LoginRequiredMixin, ListView):
    model = PhotoCommunityNotification
    context_object_name = 'notification_list'
    template_name = 'not_photo/community_notify_list.html'

    def get_queryset(self, **kwargs):
        notify = PhotoCommunityNotification.objects.filter(community__creator=self.request.user)
        return notify


@login_required
def photo_user_all_read(request):
    request.user.photo_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('photo_user_all_read')

@login_required
def photo_community_all_read(request):
    request.user.photo_community_notifications.mark_all_as_read()
    _next = request.GET.get('next')
    if _next:
        return redirect(_next)
    return redirect('photo_community_all_read')


@login_required
def photo_get_latest_notifications(request):
    notifications = request.user.photo_notifications.get_most_recent()
    return render(request, 'not_photo/most_recent.html', {'notifications': notifications})
