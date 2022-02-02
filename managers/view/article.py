from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from article.models import Article, ArticleList
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_article import ArticleManageLog


class ArticleCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/article/article_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ArticleCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ArticleCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Article.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        article, form = Article.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=article.pk, type=59)
            moderate_obj.create_close(object=article, description=mod.description, manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=article.pk, manager=request.user.pk, action_type=ArticleManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ArticleCloseDelete(View):
    def get(self,request,*args,**kwargs):
        article = Article.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=article.pk, type=59)
            moderate_obj.delete_close(object=article, manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=article.pk, manager=request.user.pk, action_type=ArticleManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class ArticleRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_moderator():
            article = Article.objects.get(pk=self.kwargs["pk"])
            moderate_obj = Moderated.objects.get(object_id=article.pk, type=59)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=article.pk, manager=request.user.pk, action_type=ArticleManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ArticleUnverify(View):
    def get(self,request,*args,**kwargs):
        article = Article.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=article.pk, type=59)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(article, manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=obj.object_id, manager=request.user.pk, action_type=ArticleManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListArticleRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = ArticleList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=58)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=ArticleManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListArticleUnverify(View):
    def get(self,request,*args,**kwargs):
        list = ArticleList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=58)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=ArticleManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListArticleCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = ArticleList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/article/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListArticleCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListArticleCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = ArticleList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=58)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=ArticleManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListArticleCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = ArticleList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=58)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            ArticleManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=ArticleManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404
