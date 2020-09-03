import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from communities.models import Community
from posts.models import Post, PostComment
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import CommentForm
from django.views import View
from common.check.community import check_can_get_lists
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from common.template.post import get_permission_community_post
from django.http import Http404


class PostCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() or not self.item.comments_enabled:
            raise Http404

        self.template_name = get_permission_community_post(self.community, "c_post_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.item
        context['community'] = self.community
        return context

    def get_queryset(self):
        comments = self.item.get_comments()
        return comments


class PostCommunityDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(uuid=self.kwargs["uuid"])

        self.template_name = get_permission_community_post(self.community, "post_community/", "detail.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostCommunityDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommunityDetail,self).get_context_data(**kwargs)
        context["object"] = self.object
        return context
