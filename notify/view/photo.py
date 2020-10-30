from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from notify.model.photo import PhotoNotify, PhotoCommunityNotify
from common.template.user import get_settings_template


class PhotoNotificationListView(LoginRequiredMixin, ListView):
    model = PhotoNotify
    context_object_name = 'notification_list'
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/photo/user_notify_list.html", request)
        return super(PhotoNotificationListView,self).get(request,*args,**kwargs)

    def get_queryset(self, **kwargs):
        notify = PhotoNotify.objects.filter(recipient=self.request.user)
        return notify


class PhotoCommunityNotificationListView(LoginRequiredMixin, ListView):
    model = PhotoCommunityNotify
    context_object_name = 'notification_list'
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/photo/community_notify_list.html", request)
        return super(PhotoCommunityNotificationListView,self).get(request,*args,**kwargs)

    def get_queryset(self, **kwargs):
        notify = PhotoCommunityNotify.objects.filter(community__creator=self.request.user)
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


class PhotoLastNotify(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/photo/most_recent.html", request)
        return super(PhotoLastNotify,self).get(request,*args,**kwargs)

    def get_queryset(self):
        notifications = self.request.user.photo_notifications.get_most_recent()
        return notifications
