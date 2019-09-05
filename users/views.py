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
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]
	    self.online=0
        aaa = datetime.now()
        onl = self.profile.last_activity + timedelta(minutes=1)
        if aaa < onl:
            self.online = 1
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['profile'] = self.profile
        context['online'] = self.online
        return context
