from django.views.generic.base import TemplateView
from article.forms import ArticleForm
from users.models import User
from django.shortcuts import render_to_response
from article.models import Article
from django.http import HttpResponse, HttpResponseBadRequest
from communities.models import Community
from django.views import View


class ArticleView(TemplateView):
    template_name="articles.html"


class ArticleNewView(TemplateView):
    model=Article
    template_name="article.html"

    def get(self,request,*args,**kwargs):
        self.article = Article.objects.get(uuid=self.kwargs["uuid"])
        return super(ArticleNewView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleNewView,self).get_context_data(**kwargs)
        context["object"]=self.article
        return context

class ArticleUserDetailView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.article = Article.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.user.get_template_list_user(folder="u_article/", template="article.html", request=request)
        return super(ArticleUserDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleUserDetailView,self).get_context_data(**kwargs)
        context["object"]=self.article
        return context


class ArticleCommunityDetailView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community=Community.objects.get(pk=self.kwargs["pk"])
        self.article = Article.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.community.get_template_list(folder="c_article/", template="article.html", request=request)
        return super(ArticleCommunityDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleCommunityDetailView,self).get_context_data(**kwargs)
        context["object"]=self.article
        context["community"]=self.community
        return context


class ArticleUserCreate(View):

    def post(self,request,*args,**kwargs):
        self.form=ArticleForm(request.POST,request.FILES)
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and request.user == self.user:
            article = self.form.save(commit=False)
            new_article = article.create_article(creator=request.user, content=article.content, community=None, g_image=article.g_image, status=article.status, title=article.title,)
            return render_to_response('post_user/my_article.html',{'object': new_article, 'user': request.user, 'request': request})
        else:
           return HttpResponseBadRequest()


class ArticleCommunityCreate(View):

    def post(self,request,*args,**kwargs):
        self.form=ArticleForm(request.POST,request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and request.user.is_staff_of_community_with_name(self.community.name):
            article = self.form.save(commit=False)
            new_article = article.create_article(creator=request.user, content=article.content, community=self.community, g_image=article.g_image, status=article.status, title=article.title,)
            return render_to_response('post_community/admin_article.html',{'object': new_article, 'user': request.user, 'request': request})
        else:
           HttpResponseBadRequest()


class ArticleUserWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="u_article_add/", template="create_article.html", request=request)
        return super(ArticleUserWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ArticleUserWindow,self).get_context_data(**kwargs)
        context['form'] = ArticleForm()
        return context


class ArticleCommunityWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="c_article_add/", template="create_article.html", request=request)
        return super(ArticleCommunityWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ArticleCommunityWindow,self).get_context_data(**kwargs)
        context['form'] = ArticleForm()
        return context
