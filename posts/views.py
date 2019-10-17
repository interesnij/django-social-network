from django.views.generic.base import TemplateView
from posts.forms import PostCommentForm
from users.models import User
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.helpers import ajax_required, AuthorRequiredMixin
from posts.models import Post, PostComment2
from posts.forms import PostUserForm
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods


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
@require_http_methods(["GET"])
def post_get_comment(request):

    post_id = request.GET['post']
    post = Post.objects.get(uuid=post_id)
    form_comment = PostCommentForm()
    comments = PostComment2.objects.filter(post=post, parent_comment=None).order_by("created")
    posts_html = render_to_string("generic/post.html", {"object": post})
    thread_html = render_to_string(
        "generic/post_comments.html", {"post_comments": comments,"form_comment": form_comment,"parent": post})
    return JsonResponse({
        "uuid": post_id,
        "post": posts_html,
        "comments": thread_html,
    })

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):

    user = request.user
    text = request.POST['text']
    par = request.POST['parent']
    parent = Post.objects.get(pk=par)
    text = text.strip()
    if parent:
        new_comment = PostComment2.objects.create(post=parent, text=text, commenter=request.user)
        html = render_to_string('generic/post_parent_comment.html',{'comment': new_comment,'request': request})
        return JsonResponse(html, safe=False)

        notification_handler(
            user, parent.creator, Notification.POST_COMMENT, action_object=reply_posts,
            id_value=str(parent.uuid), key='social_update')

    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_reply_comment(request):

    user = request.user
    text = request.POST['text']
    post_com = request.POST['comment']
    comment = PostComment2.objects.get(pk=post_com)
    text = text.strip()
    if comment:
        new_comment = PostComment2.objects.create(text=text, commenter=request.user,parent_comment=comment)
        html = render_to_string('generic/post_reply_comment.html',{'reply': new_comment,'request': request})
        return JsonResponse(html, safe=False)

        notification_handler(
            user, parent.creator, Notification.POST_REPLY_COMMENT, action_object=reply_posts,
            id_value=str(com.id), key='social_update')

    else:
        return HttpResponseBadRequest()


@login_required
@require_http_methods(["POST"])
def post_update_interactions(request):
    data_point = request.POST['id_value']
    post = Post.objects.get(post_uuid=data_point)
    data = {'likes': post.count_likers(), 'dislikes': post.count_dislikers(), 'comments': post.count_thread()}
    return JsonResponse(data)
