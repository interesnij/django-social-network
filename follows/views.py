from django.views.generic.base import TemplateView
from follows.models import Follow
from django.views.generic import ListView
from users.models import User
from django.http import HttpResponse


class FollowsListView(ListView):
	template_name="frends.html"
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


class FollowCreate(TemplateView):
    template_name = "follow_add.html"
    success_url = "/"

    def get(self,request,*args,**kwargs):
        self.user=request.user
        self.followed_user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.follows = Follow.objects.get(followed_user=self.followed_user,user=self.user)
        except:
            self.follows = None

        if not self.follows and self.followed_user != self.user:
            Follow.objects.create(followed_user=self.followed_user, user=self.user)
        else:
            return HttpResponse("Подписка уже есть :-)")
        return super(FollowCreate,self).get(request,*args,**kwargs)

class FollowDelete(TemplateView):
    template_name = "follow_delete.html"
    success_url = "/"

    def get(self,request,*args,**kwargs):
        self.user=request.user
        self.followed_user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.follows = Follow.objects.get(followed_user=self.followed_user,user=self.user)
        except:
            self.follows = None

        if self.follows and self.followed_user != self.user:
            Follow.objects.delete(followed_user=self.followed_user, user=self.user)
        else:
            return HttpResponse("Подписка не найдена!")
        return super(FollowDelete,self).get(request,*args,**kwargs)
