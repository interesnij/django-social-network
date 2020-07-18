import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render
from users.models import User
from django.views.generic import ListView
from goods.forms import CommentForm
from rest_framework.exceptions import PermissionDenied


class GoodUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if not self.good.comments_enabled:
            raise PermissionDenied('Комментарии для товара отключены')
        elif request.user.is_authenticated:
            if self.user.pk == request.user.pk:
                self.template_name = "u_good_comment/my_comments.html"
            elif request.user.is_good_manager():
                self.template_name = "u_good_comment/staff_comments.html"
            elif self.user != request.user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
                if self.user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
                self.template_name = "u_good_comment/comments.html"
        elif request.user.is_anonymous:
            if self.user.is_closed_profile():
                raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
            else:
                self.template_name = "u_good_comment/anon_comments.html"
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(GoodUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.good
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.good.get_comments()
        return comments


class GoodCommentUserCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        good = Good.objects.get(uuid=request.POST.get('uuid'))

        if form_post.is_valid() and good.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.pk)
                if user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id = user.pk)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, good_comment=good, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != good.creator.pk:
                    new_comment.notification_user_comment(request.user)
                return render(request, 'u_good_comment/my_parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if form_post.is_valid() and parent.good_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.id)
                if user.is_closed_profile():
                    check_is_connected_with_user_with_id(user=request.user, user_id = user.id)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, good_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_user_reply_comment(request.user)
            else:
                return HttpResponseBadRequest()
            return render(request, 'u_good_comment/my_reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class GoodCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class GoodCommentUserAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == comment.commenter.pk:
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class UserGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.is_deleted = True
            good.save(update_fields=['is_deleted'])
        return HttpResponse("!")

class UserGoodAbortDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.is_deleted = False
            good.save(update_fields=['is_deleted'])
        return HttpResponse("!")


class UserOpenCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.comments_enabled = True
            good.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserCloseCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.comments_enabled = False
            good.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class UserOffVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.votes_on = False
            good.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserOnVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.votes_on = True
            good.save(update_fields=['votes_on'])
        return HttpResponse("!")

class UserUnHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.status = Good.STATUS_PUBLISHED
            good.save(update_fields=['status'])
        return HttpResponse("!")

class UserHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user:
            good.status = Good.STATUS_DRAFT
            good.save(update_fields=['status'])
        return HttpResponse("!")
