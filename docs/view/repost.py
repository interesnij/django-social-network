from django.views.generic.base import TemplateView
from communities.models import Community
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm
from posts.models import Post
from docs.models import DocsList, Doc
from users.models import User
from django.http import Http404
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists
from common.processing.post import repost_message_send
from common.templates import get_detect_platform_template


class UUCMDocWindow(TemplateView):
    """
    форма репоста документа пользователя к себе на стену, в свои сообщества, в несколько сообщений
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.doc, self.user, self.template_name = Doc.objects.get(pk=self.kwargs["doc_pk"]), User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/u_ucm_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
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
        self.doc, self.community, self.template_name = Doc.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/c_ucm_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.community)
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
        self.list, self.user, self.template_name = DocsList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/u_ucm_list_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.user != request.user:
            check_user_can_get_list(request.user, self.user)
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
        self.list, self.community, self.template_name = DocsList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("docs/repost/c_ucm_list_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        check_can_get_lists(request.user, self.community)
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
        doc, user, form_post, attach = Doc.objects.get(pk=self.kwargs["doc_pk"]), User.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=user, community=None, attach="doc"+str(doc.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUDocRepost(View):
    """
    создание репоста документа сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        doc, community, form_post, attach = Doc.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=request.user, community=community, attach="doc"+str(doc.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent, community=None)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCDocRepost(View):
    """
    создание репоста документа пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        doc, user = Doc.objects.get(pk=self.kwargs["doc_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, attach="doc"+str(doc.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class CCDocRepost(View):
    """
    создание репоста документа сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        doc, community = Doc.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=photo.creator, community=community, attach="doc"+str(doc.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMDocRepost(View):
    """
    создание репоста документа пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        doc, user = Doc.objects.get(pk=self.kwargs["doc_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(doc, "doc"+str(doc.pk), None, request, "Репост документа пользователя")
        return HttpResponse()


class CMDocRepost(View):
    """
    создание репоста документа сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        doc, community = Doc.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(doc, "doc"+str(doc.pk), None, community, "Репост документа сообщества")
        return HttpResponse()


class UUDocListRepost(View):
    """
    создание репоста списка документов пользователя на свою стену
    """
    def post(self, request, *args, **kwargs):
        list, user, form_post, attach = DocsList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        if user != request.user:
            check_user_can_get_list(request.user, user)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=None, attach="ldo"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, is_signature=False, attach=attach, text=post.text, comments_enabled=post.comments_enabled, parent=parent, community=None)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CUDocListRepost(View):
    """
    создание репоста списка документов сообщества на свою стену
    """
    def post(self, request, *args, **kwargs):
        list, community, form_post, attach = DocsList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"]), PostForm(request.POST), request.POST.getlist('attach_items')
        check_can_get_lists(request.user, community)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, community=community, attach="ldo"+str(list.pk))
            new_post = post.create_post(creator=request.user, list=post.list, attach=attach, is_signature=False, text=post.text, comments_enabled=post.comments_enabled, parent=parent,community=None)
            return HttpResponse("")
        else:
            return HttpResponseBadRequest()


class UCDocListRepost(View):
    """
    создание репоста списка документов пользователя на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list, user = DocsList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, attach="ldo"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()

class CCDocListRepost(View):
    """
    создание репоста списка документов сообщества на стены списка сообществ, в которых пользователь - управленец
    """
    def post(self, request, *args, **kwargs):
        list, community = DocsList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        communities = request.POST.getlist("communities")
        attach = request.POST.getlist('attach_items')
        if not communities:
            return HttpResponseBadRequest()
        form_post = PostForm(request.POST)
        if request.is_ajax() and form_post.is_valid():
            post = form_post.save(commit=False)
            parent = Post.create_parent_post(creator=list.creator, attach="ldo"+str(list.pk))
            for community_id in communities:
                if request.user.is_staff_of_community(community_id):
                    new_post = post.create_post(creator=request.user, list=post.list, attach=attach, text=post.text, category=post.category, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, community=Community.objects.get(pk=community_id))
        return HttpResponse()


class UMDocListRepost(View):
    """
    создание репоста списка документов пользователя в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list, user = DocsList.objects.get(pk=self.kwargs["list_pk"]), User.objects.get(pk=self.kwargs["pk"])
        if user != request.user:
            check_user_can_get_list(request.user, user)
        repost_message_send(list, "ldo"+str(list.pk), None, request, "Репост плейлиста пользователя")
        return HttpResponse()


class CMDocListRepost(View):
    """
    создание репоста списка документов сообщества в беседы, в которых состоит пользователь
    """
    def post(self, request, *args, **kwargs):
        list, community = DocsList.objects.get(pk=self.kwargs["list_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        repost_message_send(list, "ldo"+str(list.pk), community, request, "Репост плейлиста сообщества")
        return HttpResponse()
