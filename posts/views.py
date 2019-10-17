from django.views.generic.base import TemplateView
from posts.forms import PostCommentForm
from users.models import User
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.helpers import ajax_required, AuthorRequiredMixin
from posts.models import Post, PostComment2
from posts.forms import PostUserForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


class PostsView(TemplateView):
    template_name="posts.html"


class PostDetailView(TemplateView):
    model=Post
    template_name="post.html"

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.post.views += 1
        self.post.save()
        return super(PostDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostDetailView,self).get_context_data(**kwargs)
        context["object"]=self.post
        return context


class PostUserCreate(TemplateView):
    template_name="article_add.html"
    form_post=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form_post=PostUserForm(initial={"creator":request.user})
        return super(PostUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCreate,self).get_context_data(**kwargs)
        context["form_post"]=self.form_post
        return context

    def post(self,request,*args,**kwargs):
        self.form_post=PostUserForm(request.POST, request.FILES)
        if self.form_post.is_valid():
            new_post=self.form_post.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form_post.save()

            if request.is_ajax() :
                 html = render_to_string('new_post.html',{'object': new_post,'request': request})
                 return HttpResponse(html)
        return super(PostUserCreate,self).get(request,*args,**kwargs)


class PostLikeView(TemplateView):
    template_name="post_like_window.html"

    def get(self,request,*args,**kwargs):
        self.post_like = Post.objects.get(pk=self.kwargs["pk"])
        self.post_like.notification_like(request.user)
        return super(PostLikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostLikeView,self).get_context_data(**kwargs)
        context["post_like"]=self.post_like
        return context


class PostCommentLikeView(TemplateView):
    template_name="post_comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.post_comment_like = PostComment2.objects.get(pk=self.kwargs["pk"])
        return super(PostCommentLikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommentLikeView,self).get_context_data(**kwargs)
        context["post_comment_like"]=self.post_comment_like
        return context


class PostDislikeView(TemplateView):
    template_name="post_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.post_dislike = Post.objects.get(pk=self.kwargs["pk"])
        self.post_dislike.notification_dislike(request.user)
        return super(PostDislikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostDislikeView,self).get_context_data(**kwargs)
        context["post_dislike"]=self.post_dislike
        return context


class PostCommentDislikeView(TemplateView):
    template_name="post_comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.post_comment_dislike = PostComment2.objects.get(pk=self.kwargs["pk"])
        return super(PostCommentDislikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommentDislikeView,self).get_context_data(**kwargs)
        context["post_comment_dislike"]=self.post_comment_dislike
        return context


@login_required
@require_http_methods(["POST"])
def post_update_interactions(request):
    data_point = request.POST['id_value']
    post = Post.objects.get(post_uuid=data_point)
    data = {'likes': post.count_likers(), 'dislikes': post.count_dislikers(), 'comments': post.count_thread()}
    return JsonResponse(data)
