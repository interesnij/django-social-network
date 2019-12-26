from django.views.generic.base import TemplateView
from article.forms import ArticleForm
from users.models import User
from django.template.loader import render_to_string
from article.models import Article
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from communities.models import Community


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

class ArticleDetailView(TemplateView):
    model=Article
    template_name="article_detail.html"

    def get(self,request,*args,**kwargs):
        self.article = Article.objects.get(uuid=self.kwargs["uuid"])
        self.article.views += 1
        self.article.save()
        return super(ArticleDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleDetailView,self).get_context_data(**kwargs)
        context["object"]=self.article
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
            article.creator=self.request.user
            new_article=article.create_article( creator=article.creator, content=article.content, community=self.community, g_image=article.g_image, comments_enabled=article.comments_enabled, status=article.status, title=article.title,)

            if request.is_ajax():
                 html = render_to_string('item_community/admin_article.html',{'object': new_article,'request': request})
                 return HttpResponse(html)
        else:
           HttpResponseBadRequest()
        return super(ArticleCommunityCreate,self).get(request,*args,**kwargs)


class ArticleCommentCreateView(TemplateView):
    template_name = "generic/posts/article_comment.html"

    def post(self, request, *args, **kwargs):
        comment = self.request.POST.get('text')
        article = Article.objects.get(pk=post_pk)

        new_comment = article.comments.create(creator=request.user, text=comment)
        data = [
                {
                'commenter': new_comment.commenter.get_full_name(),
                "comment": new_comment.text,
                "comment_id": new_comment.pk,
                }
        ]
        return JsonResponse(data, safe=False)

        notification_handler(
            user, article.creator, Notification.ARTICLE_COMMENT, action_object=reply_article,
            id_value=str(post.uuid), key='social_update')
