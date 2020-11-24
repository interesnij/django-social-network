from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from notify.model.post import PostNotify, PostCommunityNotify
from common.template.user import get_settings_template


class PostNotificationListView(LoginRequiredMixin, ListView):
    model = PostNotify
    context_object_name = 'notification_list'
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/post/user_notify_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostNotificationListView,self).get(request,*args,**kwargs)

    def get_queryset(self, **kwargs):
        notify = PostNotify.objects.filter(recipient=self.request.user)
        return notify


class PostCommunityNotificationListView(LoginRequiredMixin, ListView):
    model = PostCommunityNotify
    context_object_name = 'notification_list'
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/post/community_notify_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommunityNotificationListView,self).get(request,*args,**kwargs)

    def get_queryset(self, **kwargs):
        notify = PostCommunityNotify.objects.filter(community__creator=self.request.user)
        return notify


class PostLastNotify(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("notify/post/most_recent.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostLastNotify,self).get(request,*args,**kwargs)

    def get_queryset(self):
        notifications = self.request.user.post_notifications.get_most_recent()
        return notifications
