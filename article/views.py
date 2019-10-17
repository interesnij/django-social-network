from django.views.generic.base import TemplateView
from article.forms import (
                            ArticleForm,
                            ArticleCommentForm
                        )
from users.models import User
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from article.helpers import ajax_required, AuthorRequiredMixin
from article.models import Article, ArticleComment
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView


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


class ArticleLikeView(TemplateView):
    template_name="article_like_window.html"

    def get(self,request,*args,**kwargs):
        self.article_like = Article.objects.get(pk=self.kwargs["pk"])
        self.article_like.notification_like(request.user)
        return super(ArticleLikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleLikeView,self).get_context_data(**kwargs)
        context["article_like"]=self.article_like
        return context


class ArticleCommentLikeView(TemplateView):
    template_name="article_comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.article_comment_like = ArticleComment.objects.get(pk=self.kwargs["pk"])
        return super(ArticleCommentLikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleCommentLikeView,self).get_context_data(**kwargs)
        context["article_comment_like"]=self.article_comment_like
        return context


class ArticleDislikeView(TemplateView):
    template_name="article_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.article_dislike = Article.objects.get(pk=self.kwargs["pk"])
        self.article_dislike.notification_dislike(request.user)
        return super(ArticleDislikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleDislikeView,self).get_context_data(**kwargs)
        context["article_dislike"]=self.article_dislike
        return context


class ArticleCommentDislikeView(TemplateView):
    template_name="article_comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.article_comment_dislike = ArticleComment.objects.get(pk=self.kwargs["pk"])
        return super(ArticleCommentDislikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ArticleCommentDislikeView,self).get_context_data(**kwargs)
        context["article_comment_dislike"]=self.article_comment_dislike
        return context


@login_required
@require_http_methods(["GET"])
def article_get_comment(request):

    article_id = request.GET['article']
    article = Article.objects.get(uuid=article_id)
    form_comment = ArticleCommentForm()
    comments = ArticleComment.objects.filter(article=article, parent_comment=None).order_by("created")
    article_html = render_to_string("generic/article.html", {"object": article})
    thread_html = render_to_string(
        "generic/article_comments.html", {"art_comments": comments,"form_comment": form_comment,"parent": article})
    return JsonResponse({
        "uuid": article_id,
        "article": article_html,
        "comments": thread_html,
    })

@login_required
@ajax_required
@require_http_methods(["POST"])
def article_comment(request):

    user = request.user
    text = request.POST['text']
    par = request.POST['parent']
    article = Article.objects.get(pk=par)
    text = text.strip()
    if article:
        new_comment = ArticleComment.objects.create(article=article, text=text, commenter=request.user)
        html = render_to_string('generic/article_parent_comment.html',{'comment': new_comment,'request': request})
        return JsonResponse(html, safe=False)
    else:
        return HttpResponse("parent не найден")


@login_required
@ajax_required
@require_http_methods(["POST"])
def article_reply_comment(request):

    user = request.user
    text = request.POST['text']
    art_com = request.POST['comment']
    comment = ArticleComment.objects.get(pk=art_com)
    text = text.strip()
    if comment:
        new_comment = ArticleComment.objects.create(text=text, commenter=request.user,parent_comment=comment)
        html = render_to_string('generic/article_reply_comment.html',{'reply': new_comment,'request': request})
        return JsonResponse(html, safe=False)

        notification_handler(
            user, parent.creator, Notification.ARTICLE_REPLY_COMMENT, action_object=reply_article,
            id_value=str(com.id), key='social_update')

    else:
        return HttpResponseBadRequest()


class ArticleCommentCreateView(TemplateView):
    template_name = "generic/article_comment.html"

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



@login_required
@require_http_methods(["POST"])
def article_update_interactions(request):
    data_point = request.POST['id_value']
    article = Article.objects.get(uuid=data_point)
    data = {'likes': article.count_likers(), 'dislikes': article.count_dislikers(), 'comments': article.count_thread()}
    return JsonResponse(data)
