from django.views.generic.base import TemplateView
from users.models import User
from posts.models import Post
from connections.models import Connection
from communities.models import Community
from posts.forms import PostHardForm, PostLiteForm, PostMediumForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse,Http404
from users.forms import IdentiteForm
from django.views.generic.edit import UpdateView


class AllUsers(TemplateView):
	template_name="all_users.html"


class ProfileUserView(TemplateView):
	template_name = 'user.html'
	form = PostMediumForm

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends=Connection.objects.filter(target_connection__user=self.user)
		self.frends2=Connection.objects.filter(target_connection__target_user=self.user)
		self.communities=Community.objects.get(memberships__user=self.user)
		self.posts=Post.objects.filter(creator=self.user)
		return super(ProfileUserView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(ProfileUserView, self).get_context_data(**kwargs)
		context['user'] = self.user
		context['posts'] = self.posts
		context['frends'] = self.frends
		context['frends2'] = self.frends2
		context['form'] = self.form
		context['communities'] = self.communities
		return context

class ProfileIdentite(LoginRequiredMixin, UpdateView):
    template_name = "identity_form.html"
    form_class = IdentiteForm
    success_url = reverse_lazy("profile-home")

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset

    def form_valid(self, form, **kwargs):
        super(ProfileIdentite, self).form_valid(form)
        profile = form.save(commit=False)
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        profile.email = form.cleaned_data['email']
        profile.avatar = form.cleaned_data['avatar']
        profile.save()
        return HttpResponseRedirect(self.get_success_url())
