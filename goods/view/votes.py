import json
from django.views.generic.base import TemplateView
from users.models import User
from goods.models import Good, GoodComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from common.model.votes import GoodVotes, GoodCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied


class GoodLikeWindow(TemplateView):
    template_name = "good_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.like = Good.objects.get(pk=self.kwargs["pk"])
        self.like.notification_like(request.user)
        return super(GoodLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodLikeWindow,self).get_context_data(**kwargs)
        context["like"] = self.like
        return context


class GoodCommentLikeWindow(TemplateView):
    template_name = "good_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_like = GoodComment.objects.get(pk=self.kwargs["pk"])
        return super(GoodCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommentLikeWindow,self).get_context_data(**kwargs)
        context["comment_like"] = self.comment_like
        return context


class GoodDislikeWindow(TemplateView):
    template_name = "good_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.dislike = Good.objects.get(pk=self.kwargs["pk"])
        return super(GoodDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodDislikeWindow,self).get_context_data(**kwargs)
        context["dislike"] = self.dislike
        return context


class GoodCommentDislikeWindow(TemplateView):
    template_name = "good_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_dislike = GoodComment.objects.get(pk=self.kwargs["pk"])
        return super(GoodCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommentDislikeWindow,self).get_context_data(**kwargs)
        context["comment_dislike"]=self.comment_dislike
        return context


class GoodUserLikeCreate(View):
    def post(self, request, **kwargs):
        item = Good.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = GoodVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not GoodVotes.LIKE:
                likedislike.vote = GoodVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_user_like(request.user)
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=item, user=request.user, vote=GoodVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


class GoodUserDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Good.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = GoodVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not GoodVotes.DISLIKE:
                likedislike.vote = GoodVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_user_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=item, user=request.user, vote=GoodVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


class GoodCommentUserLikeCreate(View):
    def post(self, request, **kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
            if likedislike.vote is not GoodCommentVotes.LIKE:
                likedislike.vote = GoodCommentVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                comment.notification_user_comment_like(request.user)
            else:
                likedislike.delete()
                result = False
        except GoodCommentVotes.DoesNotExist:
            GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class GoodCommentUserDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = GoodComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile():
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not GoodCommentVotes.DISLIKE:
				likedislike.vote = GoodCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_user_comment_dislike(request.user)
			else:
				likedislike.delete()
				result = False
		except GoodCommentVotes.DoesNotExist:
			GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.DISLIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class GoodCommunityLikeCreate(View):
    def post(self, request, **kwargs):
        item = Good.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = GoodVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not GoodVotes.LIKE:
                likedislike.vote = GoodVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_community_like(request.user)
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=item, user=request.user, vote=GoodVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


class GoodCommunityDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Good.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        if not item.votes_on:
            raise PermissionDenied('Реакции отключены.')
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = GoodVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not GoodVotes.DISLIKE:
                likedislike.vote = GoodVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_community_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except GoodVotes.DoesNotExist:
            GoodVotes.objects.create(parent=item, user=request.user, vote=GoodVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")

class GoodCommentCommunityLikeCreate(View):

	def post(self, request, **kwargs):
		comment = GoodComment.objects.get(pk=self.kwargs["pk"])
		community = Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,community.name)
		try:
			likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not GoodCommentVotes.LIKE:
				likedislike.vote = GoodCommentVotes.LIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_community_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except GoodCommentVotes.DoesNotExist:
			GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.LIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class GoodCommentCommunityDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = GoodComment.objects.get(pk=self.kwargs["pk"])
		community = Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,community.name)
		try:
			likedislike = GoodCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not GoodCommentVotes.DISLIKE:
				likedislike.vote = GoodCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_community_comment_dislike(request.user)
			else:
				likedislike.delete()
				result = False
		except GoodCommentVotes.DoesNotExist:
			GoodCommentVotes.objects.create(item=comment, user=request.user, vote=GoodCommentVotes.DISLIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")
