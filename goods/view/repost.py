from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from goods.models import Good, GoodAlbum
from users.models import User
from notify.model.good import *
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.attach.post_attacher import get_post_attach
from common.processing.post import get_post_processing, repost_message_send, repost_community_send
from common.template.user import get_detect_platform_template


class UUCMGoodWindow(TemplateView):
    """
    форма репоста товара пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good, self.user, self.template_name = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/good_repost_window/u_ucm_good.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMGoodWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMGoodWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.good
        context["user"] = self.user
        return context

class CUCMGoodWindow(TemplateView):
    """
    форма репоста товара сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good, self.c, self.template_name = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/good_repost_window/c_ucm_good.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.c)
        return super(CUCMGoodWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMGoodWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.good
        context["community"] = self.c
        return context


class UUCMGoodListWindow(TemplateView):
    """
    форма репоста списка товаров пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.album, self.user, self.template_name = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/good_repost_window/u_ucm_list_good.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        return super(UUCMGoodListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMGoodListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["user"] = self.user
        return context

class CUCMGoodListWindow(TemplateView):
    """
    форма репоста списка товаров сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.album, self.c, self.template_name = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/good_repost_window/c_ucm_list_good.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.c)
        return super(CUCMGoodListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMGoodListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["community"] = self.c
        return context


class UUGoodRepost(View):
    """
    создание репоста товара пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        good, user, form_post, lists = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists")
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=None, status=Post.GOOD_REPOST)
            good.item.add(parent)
            new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUGoodRepost(View):
    """
    создание репоста товара сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        good, c, form_post, lists = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists")
        check_can_get_lists(request.user, c)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=c, status=Post.GOOD_REPOST)
            good.item.add(parent)
            new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCGoodRepost(View):
    """
    создание репоста товара пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        good, user = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_community_send(good, Post.GOOD_REPOST, None, request)
        return HttpResponse()

class CCGoodRepost(View):
    """
    создание репоста товара сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        good, c = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        repost_community_send(good, Post.GOOD_REPOST, c, request)
        return HttpResponse()


class UMGoodRepost(View):
    """
    создание репоста товара пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        good, user = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(photo, Post.GOOD_REPOST, None, request, "Репост товара пользователя")
        return HttpResponse()


class CMGoodRepost(View):
    """
    создание репоста товара сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        good, c = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        repost_message_send(photo, Post.GOOD_REPOST, c, request, "Репост товара сообщества")
        return HttpResponse()


class UUGoodListRepost(View):
    """
    создание репоста плейлиста пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        album, user, lists, form_post = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("lists"), PostForm(request.POST)
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.GOOD_LIST_REPOST)
            album.post.add(parent)
            new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUGoodListRepost(View):
    """
    создание репоста плейлиста сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        album, c, form_post, lists = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists")
        check_can_get_lists(request.user, c)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=c, status=Post.GOOD_LIST_REPOST)
            album.post.add(parent)
            new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community=None, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCGoodListRepost(View):
    """
    создание репоста плейлиста пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album, user = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_community_send(album, Post.GOOD_LIST_REPOST, None, request)
        return HttpResponse()

class CCGoodListRepost(View):
    """
    создание репоста плейлиста сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album, c = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        repost_community_send(album, Post.GOOD_LIST_REPOST, c, request)
        return HttpResponse()


class UMGoodListRepost(View):
    """
    создание репоста плейлиста пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album, user = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(album, Post.GOOD_LIST_REPOST, None, request, "Репост списка товаров пользователя")
        return HttpResponse()


class CMGoodListRepost(View):
    """
    создание репоста плейлиста сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album, c = GoodAlbum.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        repost_message_send(album, Post.GOOD_LIST_REPOST, c, request, "Репост списка товаров сообщества")
        return HttpResponse()
