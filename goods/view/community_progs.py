import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from common.checkers import check_can_get_posts_for_community_with_name
from django.shortcuts import render
from django.views.generic import ListView
from goods.forms import CommentForm
from communities.models import Community
from rest_framework.exceptions import PermissionDenied


class GoodCommunityCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if not self.good.comments_enabled:
            raise PermissionDenied('Комментарии для фотографии отключены')
        elif request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_good_comment/admin_comments.html"
            elif request.user.is_good_manager():
                self.template_name = "c_good_comment/staff_comments.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_good_comment/comments.html"
            else:
                self.template_name = "c_good_comment/comments.html"
        elif request.user.is_anonymous:
            if self.is_public():
                self.template_name = "c_good_comment/anon_comments.html"
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(GoodCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.good
        context['community'] = self.community
        return context

    def get_queryset(self):
        check_can_get_posts_for_community_with_name(self.request.user, self.community.name)
        comments = self.good.get_comments()
        return comments


class GoodCommentCommunityCreate(View):

    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        good = Good.objects.get(uuid=request.POST.get('uuid'))

        if form_post.is_valid() and good.comments_enabled:
            comment=form_post.save(commit=False)

            check_can_get_posts_for_community_with_name(request.user, community.name)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=None, good_comment=good, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != good.creator.pk:
                    new_comment.notification_community_comment(request.user, community)
                return render(request, 'c_good_comment/admin_parent.html',{'comment': new_comment, 'community': community})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class GoodReplyCommunityCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        community = Community.objects.get(pk=request.POST.get('pk'))
        parent = GoodComment.objects.get(pk=request.POST.get('good_comment'))

        if form_post.is_valid() and parent.good_comment.comments_enabled:
            comment = form_post.save(commit=False)

            check_can_get_posts_for_community_with_name(request.user, community.name)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, good_comment=None, text=comment.text)
                get_comment_attach(request, new_comment, "good_comment")
                if request.user.pk != parent.commenter.pk:
                    new_comment.notification_community_reply_comment(request.user, community)
            else:
                return HttpResponseBadRequest()
            return render(request, 'c_good_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
        else:
            return HttpResponseBadRequest()

class GoodCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.good.community
        except:
            community = comment.parent_comment.good.community
        if request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class GoodCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.good.community
        except:
            community = comment.parent_comment.good.community
        if request.user.is_staff_of_community_with_name(community.name):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class CommunityOpenCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.comments_enabled = True
            good.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityCloseCommentGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.comments_enabled = False
            good.save(update_fields=['comments_enabled'])
        return HttpResponse("!")

class CommunityOffVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.votes_on = False
            good.save(update_fields=['votes_on'])
        return HttpResponse("!")

class CommunityOnVotesGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.votes_on = True
            good.save(update_fields=['votes_on'])
        return HttpResponse("!")


class CommunityHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.is_hide = True
            good.save(update_fields=['is_hide'])
        return HttpResponse("!")

class CommunityUnHideGood(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.is_hide = False
            good.save(update_fields=['is_hide'])
        return HttpResponse("!")

class CommunityGoodDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.is_delete = True
            good.save(update_fields=['is_delete'])
        return HttpResponse("!")

class CommunityGoodAbortDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if good.creator == request.user or request.user.is_staff_of_community_with_name(good.community.name):
            good.is_delete = False
            good.save(update_fields=['is_delete'])
        return HttpResponse("!")
