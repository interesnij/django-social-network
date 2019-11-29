from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, Comment
from django.http import JsonResponse
from django.views import View
import json
from common.models import LikeDislike


class VotesView(View):
	model = None
	vote_type = None

	def post(self, request, pk):
		obj = self.model.objects.get(pk=pk)

		try:
			likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
			if likedislike.vote is not self.vote_type:
				likedislike.vote = self.vote_type
				likedislike.save(update_fields=['vote'])
				result = True
			else:
				likedislike.delete()
				result = False

		except LikeDislike.DoesNotExist:
			obj.votes.create(user=request.user, vote=self.vote_type)
			result = True

		return HttpResponse(
			json.dumps({
				"result": result,
				"like_count": obj.votes.likes().count(),
				"dislike_count": obj.votes.dislikes().count(),
				"sum_rating": obj.votes.sum_rating()
			}),
			content_type="application/json"
		)


class LikeWindow(TemplateView):
    template_name="like_window.html"

    def get(self,request,*args,**kwargs):
        self.like = Item.objects.get(pk=self.kwargs["pk"])
        self.like.notification_like(request.user)
        return super(LikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(LikeWindow,self).get_context_data(**kwargs)
        context["like"]=self.like
        return context


class CommentLikeWindow(TemplateView):
    template_name="comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_like = Comment.objects.get(pk=self.kwargs["pk"])
        self.comment_like.notification_comment_like(request.user)
        return super(CommentLikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentLikeWindow,self).get_context_data(**kwargs)
        context["comment_like"]=self.comment_like
        return context


class DislikeWindow(TemplateView):
    template_name="dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.dislike = Item.objects.get(pk=self.kwargs["pk"])
        self.dislike.notification_dislike(request.user)
        return super(DislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(DislikeWindow,self).get_context_data(**kwargs)
        context["dislike"]=self.dislike
        return context


class CommentDislikeWindow(TemplateView):
    template_name="comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_dislike = Comment.objects.get(pk=self.kwargs["pk"])
        self.comment_dislike.notification_comment_dislike(request.user)
        return super(CommentDislikeWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentDislikeWindow,self).get_context_data(**kwargs)
        context["comment_dislike"]=self.comment_dislike
        return context
