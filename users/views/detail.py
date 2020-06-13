from django.views.generic.base import TemplateView
from users.models import User
from django.shortcuts import render_to_response
from django.views.generic import ListView
from music.models import SoundcloudParsing
from communities.models import Community


class UserPostView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from posts.models import Post
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.posts = self.user.get_posts()
        self.template_name = self.user.get_template_list_user(folder="lenta/", template="post.html", request=request)
        self.next = self.posts.filter(pk__gt=self.post.pk).order_by('pk').first()
        self.prev = self.posts.filter(pk__lt=self.post.pk).order_by('-pk').first()
        return super(UserPostView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserPostView,self).get_context_data(**kwargs)
        context["object"] = self.post
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
		from video.models import VideoAlbum

		self.template_name = request.user.get_template_user(folder="user_video_list/", template="list.html", request=request)
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.album = VideoAlbum.objects.get(creator_id=self.pk, community=None, is_generic=True, title="Все видео") 
		if self.user == request.user:
			self.video_list = self.album.get_my_queryset()
		else:
			self.video_list = self.album.get_queryset()
		return super(UserVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideo,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['album'] = self.album
		return context

	def get_queryset(self):
		video_list = self.video_list
		return video_list


class ProfileUserView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        import re
        from stst.models import UserNumbers

        self.user=User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_template_user(folder="account/", template="user.html", request=request)

        if request.user.is_authenticated and request.user.pk != self.user.pk:
            MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
            if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                UserNumbers.objects.create(visitor=request.user.pk, target=self.user.pk, platform=1)
            else:
                UserNumbers.objects.create(visitor=request.user.pk, target=self.user.pk, platform=0)
        return super(ProfileUserView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileUserView, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['communities'] = self.user.get_pop_communities()
        if self.request.user.is_authenticated:
            context['common_frends'] = self.user.get_common_friends_of_user(self.request.user)[0:5]
        return context
