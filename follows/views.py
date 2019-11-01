from django.views import View
from follows.models import Follow
from django.views.generic import ListView
from users.models import User
from django.http import HttpResponse


class FollowsListView(ListView):
	template_name="follows.html"
	model=User

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.follow_user=Follow.objects.filter(user=self.user)
		self.followeds_user=Follow.objects.filter(followed_user=self.user)
		return super(FollowsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FollowsListView,self).get_context_data(**kwargs)
		context["follow_user"]=self.follow_user
		context['followeds_user'] = self.followeds_user
		context['user'] = self.user
		return context


class FollowCreate(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		follow_user_with_id(self.followed_user.pk)
		new_follow.notification_follow(request.user)
		return HttpResponse("!")


class FollowDelete(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.follows = Follow.objects.get(followed_user=self.followed_user,user=request.user)
		except:
			self.follows = None
		if self.follows:
			follow = Follow.objects.get(followed_user=self.followed_user, user=request.user)
			follow.delete()
		else:
			return HttpResponse("Подписка не найдена!")
		return HttpResponse("!")
