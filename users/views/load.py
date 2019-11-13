from django.views.generic.base import TemplateView
from users.models import User
from posts.models import Post
from main.models import Item
from frends.models import Connect
from follows.models import Follow
from goods.models import Good
from communities.models import Community
from users.forms import AvatarUserForm
from main.forms import CommentForm


class AvatarReload(TemplateView):
    template_name="profile/avatar_reload.html"


class ProfileReload(TemplateView):
    template_name = 'user_reload.html'

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]
        return super(ProfileReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['form_avatar'] = AvatarUserForm()
        context['form_comment'] = CommentForm()
        context['communities'] = self.communities
        return context


class ProfileButtonReload(TemplateView):
    template_name="profile_button.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        try:
            self.connect = Connect.objects.get(user=self.request.user,target_user=self.user)
        except:
            self.connect = None
        try:
            self.follow = Follow.objects.get(followed_user=self.user,user=self.request.user)
        except:
            self.follow = None
        try:
            self.follow2 = Follow.objects.get(followed_user=self.request.user,user=self.user)
        except:
            self.follow2 = None

        try:
            self.is_blocked = request.user.has_blocked_user_with_id(self.user)
        except:
            self.is_blocked = None

        return super(ProfileButtonReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileButtonReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['connect'] = self.connect
        context['follow'] = self.follow
        context['follow2'] = self.follow2
        context['is_blocked'] = self.is_blocked
        return context


class ProfileStatReload(TemplateView):
    template_name="profile_stat.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(ProfileStatReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStatReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context
