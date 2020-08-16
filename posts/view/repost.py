from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from users.models import User
from django.shortcuts import render
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.post_attacher import get_post_attach
from common.processing.post import get_post_processing


class UUCMPostWindow(TemplateView):
    """
    форма репоста записи пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = "repost_window/u_ucm_post.html"
        return super(UUCMPostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMPostWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.post
        return context

class CUCMPostWindow(TemplateView):
    """
    форма репоста записи сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_authenticated and request.is_ajax():
            self.template_name = "repost_window/c_ucm_post.html"
        else:
            Http404
        return super(CUCMPostWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMPostWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.post
        return context

class UUPostRepost(View):
    """
    создание репоста записи пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        self.parent = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = self.parent.creator
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
            self.form_post = PostForm(request.POST)
            if request.is_ajax() and self.form_post.is_valid():
                post = self.form_post.save(commit=False)
                if self.parent.parent:
                    self.parent = self.parent.parent
                else:
                    self.parent = self.parent
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent = self.parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                return HttpResponse()
            else:
                return HttpResponseBadRequest()

class CUPostRepost(View):
    """
    создание репоста записи сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        self.parent = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = self.parent.creator
        self.form_post = PostForm(request.POST)
        check_can_get_lists(request.user, self.user)
        if request.is_ajax() and self.form_post.is_valid():
            post = self.form_post.save(commit=False)
            if self.parent.parent:
                self.parent = self.parent.parent
            else:
                self.parent = self.parent
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent = self.parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCPostRepost(View):
    """
    создание репоста записи пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        self.parent = Post.objects.get(uuid=self.kwargs["uuid"])
        self.form_post = PostForm(request.POST)
        if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community_with_name(self.parent.community):
            post = self.form_post.save(commit=False)
            if self.parent.parent:
                self.parent = self.parent.parent
            else:
                self.parent = self.parent
            communities = form_post.cleaned_data.getlist("staff_communities")
            if not communities:
                return HttpResponse("no staff_communities")
            for community in communities:
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community_id=community, comments_enabled=post.comments_enabled, parent = self.parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCPostRepost(View):
    """
    создание репоста записи сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        self.parent = Post.objects.get(uuid=self.kwargs["uuid"])
        self.form_post = PostForm(request.POST)
        if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community_with_name(self.parent.community):
            post = self.form_post.save(commit=False)
            if self.parent.parent:
                self.parent = self.parent.parent
            else:
                self.parent = self.parent
            communities = form_post.cleaned_data.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            for community in communities:
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community_id=community, comments_enabled=post.comments_enabled, parent = self.parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
