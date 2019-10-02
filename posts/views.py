from django.views.generic.base import TemplateView
from posts.forms import (
                            PostHardForm,
                            PostLiteForm,
                            PostMediumForm,
                            PostCommentForm
                        )
from users.models import User
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.helpers import ajax_required, AuthorRequiredMixin
from posts.models import Post, PostComment
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods


class PostsView(TemplateView):
    template_name="posts.html"


class PostUserHardCreate(TemplateView):
    template_name="post_hard_add.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form=PostHardForm(initial={"creator":request.user})
        return super(PostUserHardCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserHardCreate,self).get_context_data(**kwargs)
        context["form_hard"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostHardForm(request.POST)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                 html = render_to_string('generic/post.html',{'object': new_post,'request': request})
                 return HttpResponse(html)
        return super(PostUserHardCreate,self).get(request,*args,**kwargs)

class PostUserMediumCreate(TemplateView):
    template_name="post_medium_add.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form=PostMediumForm(initial={"creator":self.request.user})
        return super(PostUserMediumCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserMediumCreate,self).get_context_data(**kwargs)
        context["form_medium"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostMediumForm(request.POST)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                 html = render_to_string('generic/post.html',{'object': new_post,'request': request})
                 return HttpResponse(html)
        return super(PostUserMediumCreate,self).get(request,*args,**kwargs)

class PostUserLiteCreate(TemplateView):
    template_name="post_lite_add.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form=PostLiteForm(initial={"creator":request.user})
        return super(PostUserLiteCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserLiteCreate,self).get_context_data(**kwargs)
        context["form_lite"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostLiteForm(request.POST)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                 html = render_to_string('generic/post.html',{'object': new_post,'request': request})
                 return HttpResponse(html)
        return super(PostUserLiteCreate,self).get(request,*args,**kwargs)

class PostDeleteView(TemplateView):
    success_url = '/'
    template_name="post_confirm_delete.html"

    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if post.creator == self.request.user:
            post.is_deleted=True
            post.save()
            return HttpResponse("!")
        return super(PostDeleteView,self).get(request,*args,**kwargs)


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


@login_required
@require_http_methods(["GET"])
def get_comment(request):

    post_id = request.GET['post']
    post = Post.objects.get(uuid=post_id)
    form_comment = PostCommentForm()
    comments = post.comments.all().order_by("-created")
    posts_html = render_to_string("generic/post.html", {"object": post})
    thread_html = render_to_string(
        "generic/post_comment.html", {"comments": comments,"form_comment": form_comment})
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
    comment = request.POST['text']
    par = request.POST['parent']
    parent = Post.objects.get(pk=par)
    comment = comment.strip()
    if parent:
        new_comment = parent.comments.create(commenter=request.user, text=comment)
        return JsonResponse({'comments': parent.comments.count()}) 

        notification_handler(
            user, parent.creator, Notification.POST_COMMENT, action_object=reply_posts,
            id_value=str(parent.uuid), key='social_update')

    else:
        return HttpResponseBadRequest()


class CommentCreateView(TemplateView):
    template_name = "generic/post_comment.html"

    def post(self, request, *args, **kwargs):
        comment = self.request.POST.get('text')
        post = Post.objects.get(pk=post_pk)

        new_comment = post.comments.create(creator=request.user, text=comment)
        data = [
                {
                'commenter': new_comment.commenter.get_full_name(),
                "comment": new_comment.text,
                "comment_id": new_comment.pk,
                }
        ]
        return JsonResponse(data, safe=False)

        notification_handler(
            user, post.creator, Notification.POST_COMMENT, action_object=reply_posts,
            id_value=str(post.uuid), key='social_update')



@login_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST['id_value']
    post = Post.objects.get(uuid=data_point)
    data = {'likes': post.count_likers(), 'dislikes': post.count_dislikers(), 'comments': post.count_thread()}
    return JsonResponse(data)
