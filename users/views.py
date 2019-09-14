from django.views.generic.base import TemplateView
from users.models import User, UserProfile
from posts.models import Post
from connections.models import Connection
from communities.models import Community
from posts.forms import PostHardForm, PostLiteForm, PostMediumForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect,HttpResponse,Http404
from users.forms import IdentiteForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic import ListView


class AllUsers(ListView):
	template_name="all_users.html"
	model = User
	paginate_by = 15

	def get_queryset(self, **kwargs):
		users=User.objects.all()
		return users



class ProfileUserView(TemplateView):
	template_name = 'user.html'
	form = PostMediumForm

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends=Connection.objects.filter(target_connection__user=self.user)
		self.frends2=Connection.objects.filter(target_connection__target_user=self.user)
		self.communities=Community.objects.filter(starrers=self.user)
		self.posts=Post.objects.filter(creator=self.user)
		return super(ProfileUserView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProfileUserView, self).get_context_data(**kwargs)
		context['user'] = self.user
		context['posts'] = self.posts
		context['frends'] = self.frends
		context['frends2'] = self.frends2
		context['form_medium'] = self.form
		context['communities'] = self.communities
		return context


class ProfileIdentite(TemplateView):
    template_name = "identity_form.html"
    form_class = IdentiteForm
    success_url = reverse_lazy("profile-home")

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(ProfileIdentite,self).get(request,*args,**kwargs)


class PostUserView(ListView):
	template_name = 'post_list.html'
	model = Post
	paginate_by = 10

	def get_queryset(self, **kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		return Post.objects.filter(creator=self.user)
