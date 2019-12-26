from django.views.generic.base import TemplateView
from article.forms import ArticleForm
from users.models import User
from django.template.loader import render_to_string
from article.models import Article
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from communities.models import Community
from main.models import Item
from rest_framework.exceptions import PermissionDenied


class ArticleView(TemplateView):
    template_name="articles.html"


class ArticleNewView(TemplateView):
    model=Article
    template_name="article.html"

    def get(self,request,*args,**kwargs):
        self.article = Article.objects.get(uuid=self.kwargs["uuid"])
        self.article.views += 1
        self.article.save()
        return super(ArticleNewView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleNewView,self).get_context_data(**kwargs)
        context["object"]=self.article
        return context

class ArticleUserDetailView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.item.views += 1
        self.item.save()

        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.template_name = "u_article.html"
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif self.user == request.user and request.user.is_authenticated:
            self.template_name = "my_article.html"
        elif not self.user.is_closed_profile() and request.user.is_anonymous:
            self.template_name = "u_article.html"
        else:
            raise PermissionDenied('Ошибка доступа')

        return super(ArticleUserDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleUserDetailView,self).get_context_data(**kwargs)
        context["object"]=self.item
        return context


class ArticleCommunityDetailView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community=Community.objects.get(uuid=self.kwargs["uuid"])
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.item.views += 1
        self.item.save()
        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.community.name):
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "admin_article.html"
            else:
                self.template_name = "c_article.html"
        elif request.user.is_authenticated and self.community.is_public():
            self.template_name = "c_article.html"

        elif request.user.is_anonymous and self.community.is_public():
            self.template_name = "c_article.html"
        else:
            raise PermissionDenied('Ошибка доступа')
        return super(ArticleCommunityDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleCommunityDetailView,self).get_context_data(**kwargs)
        context["object"]=self.item
        context["community"]=self.community
        return context


class ArticleUserCreate(TemplateView):
    template_name="article_add.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.form=ArticleForm(initial={"creator":self.user})
        return super(ArticleUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleUserCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=ArticleForm(request.POST,request.FILES)
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and request.user == self.user:
            article=self.form.save(commit=False)
            new_article=article.create_article(creator=self.user, content=article.content, community=None, g_image=article.g_image, comments_enabled=article.comments_enabled, status=article.status, title=article.title,)
            if request.is_ajax() :
                 html = render_to_string('item_user/my_article.html',{'object': new_article,'request': request})
                 return HttpResponse(html)
        else:
           return HttpResponseBadRequest()
        return super(ArticleUserCreate,self).get(request,*args,**kwargs)


class ArticleCommunityCreate(TemplateView):
    template_name="article_add_community.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form=ArticleForm()
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        return super(ArticleCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleCommunityCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        context["community"]=self.community
        return context

    def post(self,request,*args,**kwargs):
        self.form=ArticleForm(request.POST,request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and request.user.is_staff_of_community_with_name(self.community.name):
            article=self.form.save(commit=False)
            new_article=article.create_article( creator=request.user, content=article.content, community=self.community, g_image=article.g_image, comments_enabled=article.comments_enabled, status=article.status, title=article.title,)

            if request.is_ajax():
                 html = render_to_string('item_community/admin_article.html',{'object': new_article, 'community': self.community, 'request': request})
                 return HttpResponse(html)
        else:
           HttpResponseBadRequest()
        return super(ArticleCommunityCreate,self).get(request,*args,**kwargs)
