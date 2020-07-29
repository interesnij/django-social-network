import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from users.models import User
from posts.models import Post, PostComment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.check.user import check_user_can_get_list, check_anon_user_can_get_list
from posts.forms import CommentForm
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from common.template.post import get_permission_user_post 


class PostUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])

        self.template_name = get_permission_user_post(self.user, "u_post_comment/", "comments.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.item
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.item.get_comments()
        return comments


class PostCommentUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST, request.FILES)
        user = User.objects.get(pk=request.POST.get('pk'))
        post = Post.objects.get(uuid=request.POST.get('uuid'))

        if form_post.is_valid() and post.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, post=post, text=comment.text)
                get_comment_attach(request, new_comment, "item_comment")
                if request.user.pk != post.creator.pk:
                    new_comment.notification_user_comment(request.user)
                return render(request, 'u_post_comment/my_parent.html', {'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostReplyUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST, request.FILES)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = PostComment.objects.get(pk=request.POST.get('post_comment'))

        if form_post.is_valid() and parent.post.comments_enabled:
            comment=form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, post=None, text=comment.text)
                get_comment_attach(request, new_comment, "item_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_user_reply_comment(request.user)
            else:
                return HttpResponseBadRequest()
            return render(request, 'u_post_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class PostCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PostCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class PostWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PostWallCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PostUserFixed(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user == item.creator:
            item.is_fixed = True
            item.save(update_fields=['is_fixed'])
        return HttpResponse("")

class PostUserUnFixed(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user == item.creator:
            item.is_fixed = False
            item.save(update_fields=['is_fixed'])
            return HttpResponse("")
        else:
            return HttpResponse("")


class PostUserOffComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user == item.creator:
            item.comments_enabled = False
            item.save(update_fields=['comments_enabled'])
        return HttpResponse("")

class PostUserOnComment(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user == item.creator:
            item.comments_enabled = True
            item.save(update_fields=['comments_enabled'])
        return HttpResponse("")


class PostUserDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.pk == item.creator.pk:
            item.is_deleted = True
            item.save(update_fields=['is_deleted'])
        return HttpResponse("")


class PostWallUserDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            item.is_deleted = True
            item.save(update_fields=['is_deleted'])
        return HttpResponse("")

class PostUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.pk == item.creator.pk:
            item.is_deleted = False
            item.save(update_fields=['is_deleted'])
        return HttpResponse("")


class PostWallUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        item = Post.objects.get(uuid=self.kwargs["uuid"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            item.is_deleted = False
            item.save(update_fields=['is_deleted'])
        return HttpResponse("")


class PostUserDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])

        self.template_name = self.user.get_template_user("post_user/", "detail.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(PostUserDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostUserDetail,self).get_context_data(**kwargs)
        context["object"] = self.item
        return context


class UserOnVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if post.creator == request.user:
            post.votes_on = True
            post.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOffVotesPost(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if post.creator == request.user:
            post.votes_on = False
            post.save(update_fields=['votes_on'])
        return HttpResponse("!")


def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Post.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)
