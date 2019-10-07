from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from users.models import User
from django.views import View
from django.contrib.contenttypes.models import ContentType
from main.models import LikeDislike
from django.http import HttpResponse
import json


class MainPageView(TemplateView,CategoryListMixin):
	template_name=None
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name="main/mainpage.html"
		else:
			self.template_name="main/auth.html"
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)
		return context

class ComingView(TemplateView):
	template_name="main/coming.html"


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
