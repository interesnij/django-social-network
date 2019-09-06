from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import IdentiteForm
from generic.mixins import CategoryListMixin
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.base import ContextMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post



class ProfileHomeView(LoginRequiredMixin, ListView):
    template_name = 'user_profile.html'
    paginate_by = 15
    model=Post
    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]

        return context


class ProfileIdentite(LoginRequiredMixin, UpdateView, CategoryListMixin):
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
