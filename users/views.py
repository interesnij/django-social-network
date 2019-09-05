from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from generic.mixins import CategoryListMixin
from profiles.models import UserProfile
from datetime import datetime, timedelta
from users.models import User


class AllUsers(TemplateView,CategoryListMixin):
	template_name="all_users.html"


class ProfileUserView(TemplateView, CategoryListMixin):
    template_name = 'user.html'

    def get(self,request,*args,**kwargs):
		user=User.models.get(pk=self.kwargs["pk"])
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context
