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


class ProfileStatReload(TemplateView):
    template_name="profile/profile_stat.html"

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(ProfileStatReload,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileStatReload, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context
