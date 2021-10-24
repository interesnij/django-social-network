from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from django.http import Http404


class PostUserDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        from common.templates import get_template_user_item, get_template_anon_user_item
        if request.user.is_authenticated:
            self.template_name = get_template_user_item(self.post, "posts/post_user/", "detail.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_user_item(self.post, "posts/post_user/", "anon_detail.html", request.user, request.META['HTTP_USER_AGENT'])
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
