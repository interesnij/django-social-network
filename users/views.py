from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from generic.mixins import CategoryListMixin
from profiles.models import UserProfile
from datetime import datetime, timedelta
from users.models import User
from posts.models import Post
from posts.forms import PostHardForm, PostLiteForm, PostMediumForm 


class AllUsers(TemplateView,CategoryListMixin):
	template_name="all_users.html"


class ProfileUserView(TemplateView, CategoryListMixin):
	template_name = 'user.html'
	post_form=PostForm

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.posts=Post.objects.filter(creator=self.user)
		return super(ProfileUserView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProfileUserView, self).get_context_data(**kwargs)
		context['user'] = self.user
		context['posts'] = self.posts
		context['post_form'] = self.post_form
		return context
