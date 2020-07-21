import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import ListView
from communities.models import Community, CommunityMembership, CommunityCategory
from users.models import User


class CommunityMembersView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if self.community.is_private() and not self.request.user.is_member_of_community_with_name(self.name):
			membersheeps = None
			self.template_name = "c_detail/private_community.html"
		else:
			membersheeps = self.community.get_community_with_name_members(self.community.name)
			self.template_name = "c_detail/members.html"
		if MOBILE_AGENT_RE.match(self.request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return membersheeps


class CommunityFriendsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityFriendsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFriendsView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		if self.community.is_private() and not self.request.user.is_member_of_community_with_name(self.community.name):
			frends = None
			self.template_name = "c_detail/private_community.html"
		else:
			frends = self.request.user.get_common_friends_of_community(self.community.pk)
			self.template_name = "c_detail/friends.html"
		if MOBILE_AGENT_RE.match(self.request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return frends


class AllCommunities(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from common.get_template import get_default_template
		self.template_name = get_default_template(folder="c_list/", template="all_communities.html", request=request)
		return super(AllCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		groups = Community.get_trending_communities()
		return groups

	def get_context_data(self,**kwargs):
		context = super(AllCommunities,self).get_context_data(**kwargs)
		context["communities_categories"] = CommunityCategory.objects.only("pk")
		return context


class CommunityCategoryView(ListView):
	template_name="cat.html"
	paginate_by=15

	def get(self,request,*args,**kwargs):
		self.cat = CommunityCategory.objects.get(pk=self.kwargs["pk"])
		return super(CommunityCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityCategoryView,self).get_context_data(**kwargs)
		context["category"]=self.cat
		context["communities_categories"]=CommunityCategory.objects.only("pk")
		return context

	def get_queryset(self):
		self.cat = CommunityCategory.objects.get(pk=self.kwargs["pk"])
		categories=Community.objects.filter(category__sudcategory = self.cat)
		return categories


class CommunityMusic(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from music.models import SoundList

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.playlist = SoundList.objects.get(community_id=self.community.pk, is_generic=True, name="Основной плейлист")
        except:
            self.playlist = SoundList.objects.get(creator=self.community.creator, community_id=self.community.pk, is_generic=True, name="Основной плейлист")
        self.template_name = self.community.get_template(folder="community_music/", template="music.html", request=request)
        return super(CommunityMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityMusic,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['playlist'] = self.playlist
        return context

    def get_queryset(self):
        music_list = self.community.get_music()
        return music_list


class CommunityVideo(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from video.models import VideoAlbum

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_template(folder="community_video/", template="list.html", request=request)
        try:
            self.album = VideoAlbum.objects.get(community_id=self.community.pk, is_generic=True, title="Все видео")
        except:
            creator = self.community.creator
            self.album = VideoAlbum.objects.create(creator=self.community.creator, community_id=self.community.pk, community=self.community, is_generic=True, title="Все видео")
        if request.user.is_staff_of_community_with_name(self.community.name):
            self.video_list = self.album.get_my_queryset()
        else:
            self.video_list = self.album.get_queryset()
        return super(CommunityVideo,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideo,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


class PostsCommunity(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.fixed = Post.objects.get(community=community, is_fixed=True)
        except:
            self.fixed = None

        if request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_lenta/admin_list.html"
            elif request.user.is_post_manager():
                self.template_name = "c_lenta/staff_list.html"
            elif check_can_get_posts_for_community_with_name(request.user, self.community.name):
                self.template_name = "c_lenta/list.html"
            else:
                self.template_name = "c_lenta/list.html"
        elif request.user.is_anonymous:
            if self.community.is_public():
                self.template_name = "c_lenta/list.html"

        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostsCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostsCommunity,self).get_context_data(**kwargs)
        context['object'] = self.fixed
        context["community"] = self.community
        return context

    def get_queryset(self):
        item_list = self.community.get_posts().order_by('-created')
        return item_list


class PostsDraftCommunity(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if request.user.is_authenticated:
            if request.user.is_staff_of_community_with_name(self.community.name):
                self.template_name = "c_list/draft_list.html"
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostsDraftCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostsDraftCommunity,self).get_context_data(**kwargs)
        context["community"] = self.community
        return context

    def get_queryset(self):
        item_list = self.community.get_draft_posts().order_by('-created')
        return item_list
