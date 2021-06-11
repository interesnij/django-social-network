from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from common.template.post import get_permission_user_post_2
from django.http import Http404


class PostUserCommentList(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        from common.templates import get_permission_user_post_2
        self.item, self.user = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if not request.is_ajax() or not self.item.comments_enabled:
            raise Http404
        self.template_name = get_template_user_comments(self.item, "posts/u_post_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
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
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_permission_user_post_2(self.post.creator, "posts/post_user/", "detail.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostUserDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserDetail,self).get_context_data(**kwargs)
        context["object"] = Post.objects.get(uuid=self.kwargs["uuid"])
        return context


class PostLoadView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_permission_user_post_2(self.post.creator, "posts/post_user/", "post.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostLoadView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostLoadView,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context
