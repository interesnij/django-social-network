from django.views.generic.base import TemplateView
from users.models import User
from posts.models import Post
from connections.models import Connection
from posts.forms import PostHardForm, PostLiteForm, PostMediumForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



class AllUsers(TemplateView):
	template_name="all_users.html"


class ProfileUserView(TemplateView):
	template_name = 'user.html'
	form = PostMediumForm

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends=Connection.objects.filter(target_connection__user=self.user)
		self.frends2=Connection.objects.filter(target_connection__target_user=self.user)

		self.posts=Post.objects.filter(creator=self.user)
		return super(ProfileUserView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProfileUserView, self).get_context_data(**kwargs)
		context['user'] = self.user
		context['posts'] = self.posts
		context['frends'] = self.frends
		context['frends2'] = self.frends2
		context['form'] = self.form

		return context
