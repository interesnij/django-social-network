import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from common.template.post import get_permission_user_post
from django.http import Http404


class PostUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() or not self.item.comments_enabled:
            raise Http404
        self.template_name = get_permission_user_post(self.user, "u_post_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.item
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.item.get_comments()
        return comments

class PostUserDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])

        self.template_name = get_permission_user_post(self.user, "post_user/", "detail.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(PostUserDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserDetail,self).get_context_data(**kwargs)
        context["object"] = self.item
        return context
