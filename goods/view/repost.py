from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from goods.models import Good, GoodAlbum
from users.models import User
from chat.models import Message
from django.shortcuts import render
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.attach.post_attacher import get_post_attach
from common.processing.post import get_post_processing, repost_message_send


class UUCMGoodWindow(TemplateView):
    """
    форма репоста товара пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.good = Good.objects.get(pk=self.kwargs["good_pk"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "good_repost_window/u_ucm_good.html"
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
        self.good = Good.objects.get(pk=self.kwargs["good_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "good_repost_window/c_ucm_good.html"
        else:
            Http404
        return super(CUCMGoodWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMGoodWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.good
        context["community"] = self.community
        return context


class UUCMGoodListWindow(TemplateView):
    """
    форма репоста списка товаров пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
            self.user = User.objects.get(pk=self.kwargs["pk"])
            if self.user != request.user:
                check_user_can_get_list(request.user, self.user)
            self.template_name = "good_repost_window/u_ucm_list_good.html"
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
        self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated and request.is_ajax():
            check_can_get_lists(request.user, self.community)
            self.template_name = "good_repost_window/c_ucm_list_good.html"
        else:
            Http404
        return super(CUCMGoodListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMGoodListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.album
        context["community"] = self.community
        return context


class UUGoodRepost(View):
    """
    создание репоста товара пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=None, status=Post.GOOD_REPOST)
            good.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
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
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=community, status=Post.GOOD_REPOST)
            good.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
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
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=good.creator, community=None, status=Post.GOOD_REPOST)
            good.item.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community(community.pk):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCGoodRepost(View):
    """
    создание репоста товара сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=good.creator, community=community, status=Post.GOOD_REPOST)
            good.item.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMGoodRepost(View):
    """
    создание репоста товара пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=good.creator, community=None, status=Post.GOOD_REPOST)
            good.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_message_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост товара со стены пользователя")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CMGoodRepost(View):
    """
    создание репоста товара сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        good = Good.objects.get(pk=self.kwargs["good_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            connections = request.POST.getlist("user_connections")
            if not connections:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=good.creator, community=community, status=Post.GOOD_REPOST)
            good.item.add(parent)
            for user_id in connections:
                user = User.objects.get(pk=user_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                get_post_attach(request, new_post)
                get_post_message_processing(new_post)
                message = Message.send_message(sender=request.user, recipient=user, message="Репост товара со стены сообщества")
                new_post.post_message.add(message)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UUGoodListRepost(View):
    """
    создание репоста плейлиста пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.GOOD_LIST_REPOST)
            album.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
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
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=album.creator, community=community, status=Post.GOOD_LIST_REPOST)
            album.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
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
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=album.creator, community=None, status=Post.GOOD_LIST_REPOST)
            album.post.add(parent)
            for community_id in communities:
                community = Community.objects.get(pk=community_id)
                if request.user.is_staff_of_community(community.pk):
                    new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=post.comments_enabled, parent=parent, status="PG")
                    get_post_attach(request, new_post)
                    get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CCGoodListRepost(View):
    """
    создание репоста плейлиста сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            post = form_post.save(commit=False)
            communities = request.POST.getlist("staff_communities")
            if not communities:
                return HttpResponseBadRequest()
            parent = Post.create_parent_post(creator=album.creator, community=community, status=Post.GOOD_LIST_REPOST)
            album.post.add(parent)
            for community_id in communities:
                _community = Community.objects.get(pk=community_id)
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=_community, comments_enabled=post.comments_enabled, parent = parent, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UMGoodListRepost(View):
    """
    создание репоста плейлиста пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(album, Post.GOOD_LIST_REPOST, None, request, "Репост списка товаров пользователя")
        return HttpResponse()


class CMGoodListRepost(View):
    """
    создание репоста плейлиста сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(album, Post.GOOD_LIST_REPOST, community, request, "Репост списка товаров сообщества")
        return HttpResponse()
