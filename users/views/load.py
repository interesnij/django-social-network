from django.views.generic.base import TemplateView
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response


class AvatarReload(TemplateView):
    template_name="profile/avatar_reload.html"


class UserPlaylistLoad(TemplateView):
    template_name="profile/user_playlist_load.html"
    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        return super(UserPlaylistLoad,self).get(request,*args,**kwargs)


class UserImagesLoad(View):
    def get(self,request,**kwargs):
        context = {}
        photo_list = None
        self.user = User.objects.get(uuid=self.kwargs["uuid"])
        if self.user == request.user:
            photo_list = self.user.get_photos().order_by('-created')
        current_page = Paginator(photo_list, 30)
        page = request.GET.get('page')
        context['user'] = self.user
        try:
            context['photo_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['photo_list'] = current_page.page(1)
        except EmptyPage:
            context['photo_list'] = current_page.page(current_page.num_pages)
        return render_to_response('photos_load.html', context)


class ProfileReload(TemplateView):
    template_name = 'user_reload.html'

    def get(self,request,*args,**kwargs):
        from communities.models import Community

        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.communities=Community.objects.filter(memberships__user__id=self.user.pk)[0:5]
        return super(ProfileReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['communities'] = self.communities
        return context


class ProfileButtonReload(TemplateView):
    template_name = None
    is_blocked = None

    def get(self,request,*args,**kwargs):
        from frends.models import Connect
        from follows.models import Follow

        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.template_name = "button/default_button.html"
        try:
            self.connect = Connect.objects.get(user=self.request.user,target_user=self.user)
            self.template_name = "button/connect_button.html"
        except:
            self.connect = None
        try:
            self.follow = Follow.objects.get(followed_user=self.user,user=self.request.user)
            self.template_name = "button/follow_button.html"
        except:
            self.follow = None
        try:
            self.follow2 = Follow.objects.get(followed_user=self.request.user,user=self.user)
            self.template_name = "button/follow2_button.html"
        except:
            self.follow2 = None
        if request.user.is_authenticated and request.user.has_blocked_user_with_id(self.user):
            self.is_blocked = True
            self.template_name = "button/block_button.html"
        else:
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
    template_name="profile/profile_stat.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(ProfileStatReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStatReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context
