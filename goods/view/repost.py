from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from goods.models import Good, GoodList
from users.models import User
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import repost_message_send
from common.templates import get_detect_platform_template


class UUCMGoodWindow(TemplateView):
    """
    форма репоста товара пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good, self.template_name = Good.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/repost/u_ucm_good.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.good.list.is_user_can_copy_el(request.user.pk)
        if self.good.creator != request.user:
            check_user_can_get_list(request.user, self.good.creator)
        return super(UUCMGoodWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMGoodWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.good
        context["can_copy_item"] = self.can_copy_item
        return context

class CUCMGoodWindow(TemplateView):
    """
    форма репоста товара сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good, self.template_name = Good.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/repost/c_ucm_good.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.good.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.good.community)
        return super(CUCMGoodWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMGoodWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.good
        context["community"] = self.good.community
        context["can_copy_item"] = self.can_copy_item
        return context


class UUCMGoodListWindow(TemplateView):
    """
    форма репоста списка товаров пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list, self.template_name = GoodList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/repost/u_ucm_list_good.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        if self.list.creator != request.user:
            check_user_can_get_list(request.user, self.list.creator)
        return super(UUCMGoodListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMGoodListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["can_copy_item"] = self.can_copy_item
        return context

class CUCMGoodListWindow(TemplateView):
    """
    форма репоста списка товаров сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list, self.template_name = GoodList.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("goods/repost/c_ucm_list_good.html", request.user, request.META['HTTP_USER_AGENT'])
        self.can_copy_item = self.list.is_user_can_copy_el(request.user.pk)
        check_can_get_lists(request.user, self.list.community)
        return super(CUCMGoodListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMGoodListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["community"] = self.list.community
        context["can_copy_item"] = self.can_copy_item
        return context


class UUGoodRepost(View):
    """
    создание репоста товара пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        good, user, form_post, lists, attach = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists"), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=None, attach="goo"+str(good.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUGoodRepost(View):
    """
    создание репоста товара сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        good, c, form_post, lists, attach = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists"), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, c)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=c, attach="goo"+str(good.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
            return HttpResponse()
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
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=community, attach="goo"+str(good.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on,community=Community.objects.get(pk=community_id))
        return HttpResponse()

class CCGoodRepost(View):
    """
    создание репоста товара сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        good, c = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=good.creator, community=community, attach="goo"+str(good.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on,community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMGoodRepost(View):
    """
    создание репоста товара пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        good, user = Good.objects.get(pk=self.kwargs["good_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(photo, "goo"+str(good.pk), None, request, "Репост товара пользователя")
        return HttpResponse()


class CMGoodRepost(View):
    """
    создание репоста товара сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        good, c = Good.objects.get(pk=self.kwargs["good_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        repost_message_send(photo, "goo"+str(good.pk), c, request, "Репост товара сообщества")
        return HttpResponse()


class UUGoodListRepost(View):
    """
    создание репоста плейлиста пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        list, user, lists, form_post, attach = GoodList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"]), request.POST.getlist("lists"), PostForm(request.POST), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="lgo"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on,community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUGoodListRepost(View):
    """
    создание репоста плейлиста сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        list, c, form_post, lists, attach = GoodList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist("lists"), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, c)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=c, attach="lgo"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=False, votes_on=post.votes_on, community=None)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCGoodListRepost(View):
    """
    создание репоста плейлиста пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list, user = GoodList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="lgo"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()

class CCGoodListRepost(View):
    """
    создание репоста плейлиста сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list, c = GoodList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="lgo"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMGoodListRepost(View):
    """
    создание репоста плейлиста пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list, user = GoodList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, "lgo"+str(list.pk), None, request, "Репост списка товаров пользователя")
        return HttpResponse()


class CMGoodListRepost(View):
    """
    создание репоста плейлиста сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list, c = GoodList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, c)
        repost_message_send(list, "lgo"+str(list.pk), c, request, "Репост списка товаров сообщества")
        return HttpResponse()
