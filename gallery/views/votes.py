import json
from django.views.generic.base import TemplateView
from users.models import User
from main.models import Photo, PhotoComment
from communities.models import Community
from django.http import JsonResponse, HttpResponse
from django.views import View
from common.models import PhotoVotes, PhotoCommentVotes
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name


class PhotoLikeWindow(TemplateView):
    template_name="photo_votes/like_window.html"

    def get(self,request,*args,**kwargs):
        self.like = Photo.objects.get(pk=self.kwargs["pk"])
        self.like.notification_like(request.user)
        return super(PhotoLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoLikeWindow,self).get_context_data(**kwargs)
        context["like"]=self.like
        return context


class PhotoCommentLikeWindow(TemplateView):
    template_name="photo_votes/comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_like = PhotoComment.objects.get(pk=self.kwargs["pk"])
        self.comment_like.notification_comment_like(request.user)
        return super(PhotoCommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoCommentLikeWindow,self).get_context_data(**kwargs)
        context["comment_like"]=self.comment_like
        return context


class PhotoDislikeWindow(TemplateView):
    template_name="photo_votes/dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.dislike = Photo.objects.get(pk=self.kwargs["pk"])
        self.dislike.notification_dislike(request.user)
        return super(PhotoDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoDislikeWindow,self).get_context_data(**kwargs)
        context["dislike"]=self.dislike
        return context


class PhotoCommentDislikeWindow(TemplateView):
    template_name="photo_votes/comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_dislike = PhotoComment.objects.get(pk=self.kwargs["pk"])
        self.comment_dislike.notification_comment_dislike(request.user)
        return super(PhotoCommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PhotoCommentDislikeWindow,self).get_context_data(**kwargs)
        context["comment_dislike"]=self.comment_dislike
        return context


class PhotoUserLikeCreate(View):
    def post(self, request, **kwargs):
        item = Photo.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.LIKE:
                likedislike.vote = PhotoVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_like(request.user)
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


class PhotoUserDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Photo.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(uuid=self.kwargs["uuid"])
        if user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
            if user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.DISLIKE:
                likedislike.vote = PhotoVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_dislike(request.user)
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")

class PhotoCommentUserLikeCreate(View):

	def post(self, request, **kwargs):
		comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not PhotoCommentVotes.LIKE:
				likedislike.vote = PhotoCommentVotes.LIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except PhotoCommentVotes.DoesNotExist:
			PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.LIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class PhotoCommentUserDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		if user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=user.id)
			if user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=user.id)
		try:
			likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not PhotoCommentVotes.DISLIKE:
				likedislike.vote = PhotoCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_comment_dislike(request.user)
			else:
				likedislike.delete()
				result = False
		except PhotoCommentVotes.DoesNotExist:
			PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.DISLIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class PhotoCommunityLikeCreate(View):
    def post(self, request, **kwargs):
        item = Photo.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.LIKE:
                likedislike.vote = PhotoVotes.LIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_like(request.user)
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.LIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")


class PhotoCommunityDislikeCreate(View):
    def post(self, request, **kwargs):
        item = Photo.objects.get(pk=self.kwargs["pk"])
        community = Community.objects.get(uuid=self.kwargs["uuid"])
        check_can_get_posts_for_community_with_name(request.user,community.name)
        try:
            likedislike = PhotoVotes.objects.get(parent=item, user=request.user)
            if likedislike.vote is not PhotoVotes.DISLIKE:
                likedislike.vote = PhotoVotes.DISLIKE
                likedislike.save(update_fields=['vote'])
                result = True
                item.notification_like(request.user)
            else:
                likedislike.delete()
                result = False
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=item, user=request.user, vote=PhotoVotes.DISLIKE)
            result = True
        return HttpResponse(json.dumps({"result": result,"like_count": item.likes().count(),"dislike_count": item.dislikes().count()}),content_type="application/json")

class PhotoCommentCommunityLikeCreate(View):

	def post(self, request, **kwargs):
		comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
		community = Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,community.name)
		try:
			likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not PhotoCommentVotes.LIKE:
				likedislike.vote = PhotoCommentVotes.LIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except PhotoCommentVotes.DoesNotExist:
			PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.LIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")


class PhotoCommentCommunityDislikeCreate(View):

	def post(self, request, **kwargs):
		comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
		community = Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,community.name)
		try:
			likedislike = PhotoCommentVotes.objects.get(item=comment, user=request.user)
			if likedislike.vote is not PhotoCommentVotes.DISLIKE:
				likedislike.vote = PhotoCommentVotes.DISLIKE
				likedislike.save(update_fields=['vote'])
				result = True
				comment.notification_comment_like(request.user)
			else:
				likedislike.delete()
				result = False
		except PhotoCommentVotes.DoesNotExist:
			PhotoCommentVotes.objects.create(item=comment, user=request.user, vote=PhotoCommentVotes.DISLIKE)
			result = True
		return HttpResponse(json.dumps({"result": result,"like_count": comment.likes().count(),"dislike_count": comment.dislikes().count()}),content_type="application/json")
