
from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from docs.models import DocList, Doc2
from users.models import User
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.attach.post_attacher import get_post_attach
from common.processing.post import get_post_processing, repost_message_send, repost_community_send
from common.template.user import get_detect_platform_template


class UUCMDocWindow(TemplateView):
    """
    форма репоста документа пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("docs/doc_repost_window/u_ucm_doc.html", request.META['HTTP_USER_AGENT'])
        return super(UUCMDocWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMDocWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.doc
        context["user"] = self.user
        return context

class CUCMDocWindow(TemplateView):
    """
    форма репоста документа сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("docs/doc_repost_window/c_ucm_doc.html", request.META['HTTP_USER_AGENT'])
        return super(CUCMDocWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMDocWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.doc
        context["community"] = self.community
        return context

class UUCMDocListWindow(TemplateView):
    """
    форма репоста списка документов пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
        self.template_name = get_detect_platform_template("docs/doc_repost_window/u_ucm_list_doc.html", request.META['HTTP_USER_AGENT'])
        return super(UUCMDocListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UUCMDocListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["user"] = self.user
        return context

class CUCMDocListWindow(TemplateView):
    """
    форма репоста списка документов сообщества к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, self.community)
        self.template_name = get_detect_platform_template("docs/doc_repost_window/c_ucm_list_doc.html", request.META['HTTP_USER_AGENT'])
        return super(CUCMDocListWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CUCMDocListWindow,self).get_context_data(**kwargs)
        context["form"] = PostForm()
        context["object"] = self.list
        context["community"] = self.community
        return context


class UUDocRepost(View):
    """
    создание репоста документа пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=user, community=None, status=Post.DOC_REPOST)
            doc.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status=Post.STATUS_PROCESSING)
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUDocRepost(View):
    """
    создание репоста документа сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=request.user, community=community, status=Post.DOC_REPOST)
            doc.item.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCDocRepost(View):
    """
    создание репоста документа пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_community_send(doc, Post.DOC_REPOST, None, request)
        return HttpResponse()


class CCDocRepost(View):
    """
    создание репоста документа сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_community_send(doc, Post.DOC_REPOST, community, request)
        return HttpResponse()


class UMDocRepost(View):
    """
    создание репоста документа пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(doc, Post.DOC_REPOST, None, request, "Репост документа пользователя")
        return HttpResponse()


class CMDocRepost(View):
    """
    создание репоста документа сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(doc, Post.DOC_REPOST, None, community, "Репост документа сообщества")
        return HttpResponse()


class UUDocListRepost(View):
    """
    создание репоста списка документов пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, status=Post.DOC_LIST_REPOST)
            list.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUDocListRepost(View):
    """
    создание репоста списка документов сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        form_post = PostForm(request.POST)
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, status=Post.DOC_LIST_REPOST)
            list.post.add(parent)
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_processing(new_post)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCDocListRepost(View):
    """
    создание репоста списка документов пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_community_send(list, Post.DOC_LIST_REPOST, None, request)
        return HttpResponse()

class CCDocListRepost(View):
    """
    создание репоста списка документов сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_community_send(list, Post.DOC_LIST_REPOST, community, request)
        return HttpResponse()


class UMDocListRepost(View):
    """
    создание репоста списка документов пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, Post.DOC_LIST_REPOST, None, request, "Репост плейлиста пользователя")
        return HttpResponse()


class CMDocListRepost(View):
    """
    создание репоста списка документов сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(list, Post.DOC_LIST_REPOST, community, request, "Репост плейлиста сообщества")
        return HttpResponse()
