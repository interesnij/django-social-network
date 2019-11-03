from django.views import View
from follows.models import Follow
from django.views.generic import ListView
from users.models import User
from django.http import HttpResponse


class FollowsListView(ListView):
	template_name="follows.html"
	model=User
	paginate_by=10

	def get_queryset(self):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		followeds_user=Follow.objects.filter(user=self.user)
		return followeds_user


class FollowCreate(View):

	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		new_follow = request.user.follow_user(self.followed_user)
		new_follow.notification_follow(request.user)
		return HttpResponse("!")


class FollowDelete(View):

	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		request.user.unfollow_user(self.followed_user)
		return HttpResponse("!")
