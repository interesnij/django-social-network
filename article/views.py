""" TemplateView """
from django.views.generic.base import TemplateView


class ArticleUserDetailView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.template.post import get_permission_user_post
        from users.models import User
        from article.models import Article

        self.user, self.article = User.objects.get(pk=self.kwargs["pk"]), Article.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_permission_user_post(self.user, "article/u_article/", "article.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ArticleUserDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleUserDetailView,self).get_context_data(**kwargs)
        context["object"] = self.article
        return context


class ArticleCommunityDetailView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from communities.models import Community
        from common.template.post import get_permission_community_post
        from article.models import Article

        self.community, self.article = Community.objects.get(pk=self.kwargs["pk"]), Article.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_permission_community_post(self.community, "article/c_article/", "article.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ArticleCommunityDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ArticleCommunityDetailView,self).get_context_data(**kwargs)
        context["object"] = self.article
        context["community"] = self.community
        return context


""" View """
from django.views import View

class ArticleUserCreate(View):
    def get(self,request,*args,**kwargs):
        from common.template.user import get_settings_template
        from users.models import User

        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("article/u_article_add/create_article.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ArticleUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from article.forms import ArticleForm

        context = super(ArticleUserCreate,self).get_context_data(**kwargs)
        context['form'] = ArticleForm()
        return context

    def post(self,request,*args,**kwargs):
        from common.template.user import render_for_platform
        from article.forms import ArticleForm

        self.form, self.user = ArticleForm(request.POST,request.FILES), User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and request.user == self.user:
            article = self.form.save(commit=False)
            new_article = article.create_article(creator=request.user, content=article.content, community__isnull=True, g_image=article.g_image, status=article.status, title=article.title,)
            return render_for_platform(request, 'posts/post_user/my_article.html',{'object': new_article, 'user': request.user})
        else:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest()


class ArticleCommunityCreate(View):
    def get(self,request,*args,**kwargs):
        from common.template.user import get_settings_template

        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("article/c_article_add/create_article.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ArticleCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from article.forms import ArticleForm

        context = super(ArticleCommunityCreate,self).get_context_data(**kwargs)
        context['form'] = ArticleForm()
        return context

    def post(self,request,*args,**kwargs):
        from communities.models import Community
        from common.template.user import render_for_platform
        from article.forms import ArticleForm

        self.form, self.community = ArticleForm(request.POST,request.FILES), Community.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid() and request.user.is_staff_of_community(self.community.pk):
            article = self.form.save(commit=False)
            new_article = article.create_article(creator=request.user, content=article.content, community=self.community, g_image=article.g_image, status=article.status, title=article.title,)
            return render_for_platform(request, 'posts/post_community/admin_article.html',{'object': new_article, 'user': request.user})
        else:
            from django.http import HttpResponseBadRequest
            HttpResponseBadRequest()
