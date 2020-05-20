from django.views.generic.base import TemplateView
from users.models import User
from django.shortcuts import render_to_response
from django.views.generic import ListView
from music.models import SoundcloudParsing
from communities.models import Community


class UserItemView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from main.models import Item
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.items = self.user.get_posts()
        self.template_name = self.user.get_template_list_user(folder="lenta/", template="item.html", request=request)
        self.next = self.items.filter(pk__gt=self.item.pk).order_by('pk').first()
        self.prev = self.items.filter(pk__lt=self.item.pk).order_by('-pk').first()
        return super(UserItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserItemView,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["user"] = self.user
        context["next"] = self.next
        context["prev"] = self.prev
        return context

class UserCommunities(ListView):
    template_name = None
    model = Community
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="user_community/", template="communities.html", request=request)
        if self.user.is_staffed_user() and self.user == request.user:
            self.template_name = "user_community/my_staffed_communities.html"
        return super(UserCommunities,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCommunities, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        communities_list = Community.objects.filter(memberships__user__id=self.user.pk)
        return communities_list

class UserStaffCommunities(ListView):
    template_name = None
    model = Community
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_staffed_user() and self.user == request.user:
            self.template_name = "user_community/staffed_communities.html"
        return super(UserStaffCommunities,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserStaffCommunities, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context

    def get_queryset(self):
        communities_list = self.user.get_staffed_communities()
        return communities_list


class UserMobStaffed(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user == request.user:
            self.template_name = "mob_user_community/staffed.html"
        return super(UserMobStaffed,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserMobStaffed, self).get_context_data(**kwargs)
        context['user'] = self.user
        return context


class UserMusic(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_template_user(folder="user_music/", template="music.html", request=request)
		return super(UserMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusic,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		music_list = self.user.get_music()
		return music_list


class UserVideo(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_template_user(folder="user_video/", template="video.html", request=request)
		return super(UserVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideo,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		video_list = self.user.get_video()
		return video_list


class ProfileUserView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.communities=self.user.get_pop_communities()
        self.template_name = self.user.get_template_user(folder="account/", template="user.html", request=request)
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['communities'] = self.communities
        if self.request.user.is_authenticated:
            context['common_frends'] = self.user.get_common_friends_of_user(self.request.user)[0:5]
        return context
