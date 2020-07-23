import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment, GoodSubCategory, GoodCategory
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render
from users.models import User
from goods.forms import CommentForm, GoodForm
from rest_framework.exceptions import PermissionDenied
from common.processing.good import get_good_processing, get_good_offer_processing


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

class GoodUserCreate(TemplateView):
    template_name = "u_good/add.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.form = GoodForm()
        self.user = User.objects.get(pk=self.kwargs["pk"])
        return super(GoodUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserCreate,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            good = self.form.save(commit=False)
            new_good = good.create_good(title=good.title, image=good.image, sub_category=good.sub_category, creator=self.user, description=good.description, community=None, price=good.price, comments_enabled=good.comments_enabled, votes_on=good.votes_on, status="PG")
            #get_good_offer_processing(new_good)
            return render(request, 'good_base/new_good.html',{'object': new_good})
        else:
            return HttpResponseBadRequest("")
        return super(GoodUserCreate,self).get(request,*args,**kwargs)



class GoodUserCreateAttach(TemplateView):
    template_name = "u_good/add_attach.html"
    form = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.form = GoodForm(initial={"creator":self.user})
        return super(GoodUserCreateAttach,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodUserCreateAttach,self).get_context_data(**kwargs)
        context["form"] = self.form
        context["sub_categories"] = GoodSubCategory.objects.only("id")
        context["categories"] = GoodCategory.objects.only("id")
        context["user"] = self.user
        return context

    def post(self,request,*args,**kwargs):
        self.form = GoodForm(request.POST,request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.form.is_valid():
            new_good = self.form.save(commit=False)
            new_good.creator = self.user
            new_good = self.form.save()
            html = render(request, 'u_good/good.html',{'object': new_good})
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()
        return super(GoodUserCreateAttach,self).get(request,*args,**kwargs)
