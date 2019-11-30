from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
from common.models import ItemVotes, ItemCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.contrib.contenttypes.models import ContentType


class LikeWindow(TemplateView):
    template_name="votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.like = Item.objects.get(pk=self.kwargs["pk"])
        self.like.notification_like(request.user)
        return super(LikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(LikeWindow,self).get_context_data(**kwargs)
        context["like"]=self.like
        return context


class CommentLikeWindow(TemplateView):
    template_name="votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_like = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.comment_like.notification_comment_like(request.user)
        return super(CommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentLikeWindow,self).get_context_data(**kwargs)
        context["comment_like"]=self.comment_like
        return context


class DislikeWindow(TemplateView):
    template_name="votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.dislike = Item.objects.get(pk=self.kwargs["pk"])
        self.dislike.notification_dislike(request.user)
        return super(DislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(DislikeWindow,self).get_context_data(**kwargs)
        context["dislike"]=self.dislike
        return context


class CommentDislikeWindow(TemplateView):
    template_name="votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_dislike = ItemComment.objects.get(pk=self.kwargs["pk"])
        self.comment_dislike.notification_comment_dislike(request.user)
        return super(CommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentDislikeWindow,self).get_context_data(**kwargs)
        context["comment_dislike"]=self.comment_dislike
        return context


class ItemUserLikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.LIKE:
                likedislike.vote = ItemVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes.count(),"dislike_count": item.dislikes.count()}),content_type="application/json")


class ItemUserDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.DISLIKE:
                likedislike.vote = ItemVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes.count(),"dislike_count": item.dislikes.count()}),content_type="application/json")

class ItemCommentUserLikeCreate(View):

	def post(self, request, **kwargs):
		comment = ItemComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = ItemCommentVotes.objects.get(parent=comment, user=request.user)
			if likedislike.vote is not ItemCommentVotes.LIKE:
				likedislike.vote = ItemCommentVotes.LIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except ItemCommentVotes.DoesNotExist:
			ItemCommentVotes.objects.create(parent=item, user=request.user, vote=ItemCommentVotes.LIKE)
			result = True
		likes = ItemCommentVotes.objects.filter(parent=item, vote__gt=0)
		dislikes = ItemCommentVotes.objects.filter(parent=item, vote__lt=0)
		return HttpResponse(json.dumps({"result": result,"like_count": likes.count(),"dislike_count": dislikes.count()}),content_type="application/json")


class ItemCommentUserDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = ItemComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = ItemCommentVotes.objects.get(parent=comment, user=request.user)
			if likedislike.vote is not ItemCommentVotes.DISLIKE:
				likedislike.vote = ItemCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except ItemCommentVotes.DoesNotExist:
			ItemCommentVotes.objects.create(parent=item, user=request.user, vote=ItemCommentVotes.DISLIKE)
			result = True
		likes = ItemCommentVotes.objects.filter(parent=item, vote__gt=0)
		dislikes = ItemCommentVotes.objects.filter(parent=item, vote__lt=0)
		return HttpResponse(json.dumps({"result": result,"like_count": likes.count(),"dislike_count": dislikes.count()}),content_type="application/json")
