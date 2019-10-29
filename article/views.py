from django.views.generic.base import TemplateView
from article.forms import ArticleForm
from users.models import User
from django.template.loader import render_to_string
from article.models import Article
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import JsonResponse
from generic.mixins import CategoryListMixin


class ArticleView(TemplateView):
    template_name="articles.html"


class ArticleNewView(CategoryListMixin, TemplateView):
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

class ArticleDetailView(CategoryListMixin, TemplateView):
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
        self.form=ArticleForm(initial={"creator":request.user})
        return super(ArticleUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleUserCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=ArticleForm(request.POST,request.FILES)
        if self.form.is_valid():
            new_article=self.form.save(commit=False)
            new_article.creator=self.request.user
            new_article=self.form.save()

            if request.is_ajax() :
                 html = render_to_string('article.html',{'object': new_article,'request': request})
                 return HttpResponse(html)
        else:
           return JsonResponse({'error': True, 'errors': self.form.errors})
        return super(ArticleUserCreate,self).get(request,*args,**kwargs)


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
