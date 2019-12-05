import json
from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from common.models import ItemVotes, ItemCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import PermissionDenied


class ItemLikeWindow(TemplateView):
    template_name="item_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(pk=self.kwargs["pk"])
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            self.likes = self.item.get_likes_for_item(request.user)
        elif self.user == request.user:
            self.likes = self.item.get_likes_for_item(request.user)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            self.likes = self.item.get_likes_for_item(request.user)

        return super(ItemLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemLikeWindow,self).get_context_data(**kwargs)
        context["likes"]=self.likes
        return context


class ItemCommentLikeWindow(TemplateView):
    template_name="item_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_like = ItemComment.objects.get(pk=self.kwargs["pk"])
        return super(ItemCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommentLikeWindow,self).get_context_data(**kwargs)
        context["comment_like"]=self.comment_like
        return context


class ItemDislikeWindow(TemplateView):
    template_name="item_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        def get(self,request,*args,**kwargs):
            self.item = Item.objects.get(pk=self.kwargs["pk"])
            self.user = User.objects.get(uuid=self.kwargs["uuid"])
            if self.user != request.user and request.user.is_authenticated:
                check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
                if self.user.is_closed_profile:
                    check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
                self.dislikes = self.item.get_dislikes_for_item(request.user)
            elif self.user == request.user:
                self.dislikes = self.item.get_dislikes_for_item(request.user)
            elif request.user.is_anonymous and self.user.is_closed_profile():
                raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
            elif request.user.is_anonymous and not self.user.is_closed_profile():
                self.dislikes = self.item.get_dislikes_for_item(request.user)

            return super(ItemDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemDislikeWindow,self).get_context_data(**kwargs)
        context["dislikes"]=self.dislikes
        return context


class ItemCommentDislikeWindow(TemplateView):
    template_name="item_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_dislike = ItemComment.objects.get(pk=self.kwargs["pk"])
        return super(ItemCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommentDislikeWindow,self).get_context_data(**kwargs)
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
                item.notification_user_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


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
                item.notification_user_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")

class ItemCommentUserLikeCreate(View):

	def post(self, request, **kwargs):
		comment = ItemComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not ItemCommentVotes.LIKE:
				likedislike.vote = ItemCommentVotes.LIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_user_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except ItemCommentVotes.DoesNotExist:
			ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.LIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class ItemCommentUserDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = ItemComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not ItemCommentVotes.DISLIKE:
				likedislike.vote = ItemCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_user_comment_dislike(request.user)
			else:
				likedislike.delete()
				result = False
		except ItemCommentVotes.DoesNotExist:
			ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.DISLIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class ItemCommunityLikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.LIKE:
                likedislike.vote = ItemVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_community_like(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


class ItemCommunityDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Item.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = ItemVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not ItemVotes.DISLIKE:
                likedislike.vote = ItemVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_community_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except ItemVotes.DoesNotExist:
            ItemVotes.objects.create(parent=item, user=request.user, vote=ItemVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")

class ItemCommentCommunityLikeCreate(View):

	def post(self, request, **kwargs):
		comment = ItemComment.objects.get(pk=self.kwargs["pk"])
		community = Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,community.name)
		try:
			likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not ItemCommentVotes.LIKE:
				likedislike.vote = ItemCommentVotes.LIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_community_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except ItemCommentVotes.DoesNotExist:
			ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.LIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class ItemCommentCommunityDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = ItemComment.objects.get(pk=self.kwargs["pk"])
		community = Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,community.name)
		try:
			likedislike = ItemCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not ItemCommentVotes.DISLIKE:
				likedislike.vote = ItemCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_community_comment_dislike(request.user)
			else:
				likedislike.delete()
				result = False
		except ItemCommentVotes.DoesNotExist:
			ItemCommentVotes.objects.create(item=comment, user=request.user, vote=ItemCommentVotes.DISLIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")
