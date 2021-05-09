from django.views.generic import ListView
from communities.models import Community, CommunityCategory
from common.template.user import get_default_template, get_detect_platform_template


class CommunityMembersView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_default_template("communities/list/", "members.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		return self.c.get_members(self.c.pk)


class CommunityFriendsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_default_template("communities/detail/", "friends.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityFriendsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityFriendsView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		return self.request.user.get_common_friends_of_community(self.c.pk)


class AllCommunities(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_default_template("communities/list/", "all_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Community.get_trending_communities()

	def get_context_data(self,**kwargs):
		c = super(AllCommunities,self).get_context_data(**kwargs)
		c["communities_categories"], c["count_communities"] = CommunityCategory.objects.only("pk"), Community.objects.all().values("pk").count()
		return c


class TrendCommunities(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_default_template("communities/list/", "trend_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(TrendCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return Community.get_trending_communities()

	def get_context_data(self,**kwargs):
		c = super(TrendCommunities,self).get_context_data(**kwargs)
		c["communities_categories"], c["count_communities"] = CommunityCategory.objects.only("pk"), Community.objects.all().values("pk").count()
		return c


class CommunityCategoryView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.cat, self.template_name = CommunityCategory.objects.get(pk=self.kwargs["pk"]), get_default_template("communities/list/", "cat_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityCategoryView,self).get_context_data(**kwargs)
		c["category"], c["communities_categories"] = self.cat, CommunityCategory.objects.only("pk")
		return c

	def get_queryset(self):
		return Community.objects.filter(category__sudcategory_id = self.kwargs["pk"])


class CommunityDocs(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.templates import get_template_anon_community, get_template_community

		self.c, user = Community.objects.get(pk=self.kwargs["pk"]), request.user
		self.list = DocList.objects.get(community_id=self.c.pk, type=DocList.MAIN)
		if user.is_authenticated and user.is_staff_of_community(self.c.pk):
			self.doc_list = self.list.get_staff_items()
		else:
			self.doc_list = self.list.get_items()
		if request.user.is_anonymous:
			self.template_name = get_template_anon_community(self.list, "communities/docs/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community(self.list, "communities/docs/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		return super(CommunityDocs,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityDocs,self).get_context_data(**kwargs)
		c['community'],c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.doc_list

class CommunityDocsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.templates import get_template_anon_community, get_template_community

		self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.doc_list = self.list.get_staff_items()
		else:
			self.doc_list = self.list.get_items()
		if self.list.type == DocList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/docs/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.list, "communities/docs/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/docs/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.list, "communities/docs/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_doc_manager())
		return super(CommunityDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityDocsList,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.doc_list


class CommunityGoods(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_anon_community, get_template_community

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.list = self.c.get_good_list()
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.goods_list = self.list.get_staff_items()
		else:
			self.goods_list = self.list.get_items()
		if request.user.is_anonymous:
			self.template_name = get_template_anon_community(self.list, "communities/goods/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community(self.list, "communities/goods/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_good_manager())
		return super(CommunityGoods,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityGoods,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.goods_list

class CommunityGoodsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodList
		from common.templates import get_template_anon_community, get_template_community

		self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), GoodList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.goods_list = self.list.get_staff_items()
		else:
			self.goods_list = self.list.get_items()

		if self.list.type == GoodList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/goods/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.list, "communities/goods/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_good_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/goods/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.list, "communities/goods/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_good_manager())
		return super(CommunityGoodsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityGoodsList,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.goods_list


class CommunityMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		from common.templates import get_template_anon_community, get_template_community

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.list = self.c.get_playlist()
		if request.user.is_anonymous:
			self.template_name = get_template_anon_community(self.list, "communities/music/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community(self.list, "communities/music/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		return super(CommunityMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityMusic,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.list.get_items()

class CommunityMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		from common.templates import get_template_anon_community, get_template_community

		self.c, self.play = Community.objects.get(pk=self.kwargs["pk"]), SoundList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.type == SoundList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/music/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.list, "communities/music/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/music/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.playlist, "communities/music/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		return super(CommunityMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityMusicList,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.list.get_items()


class CommunityVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_anon_community, get_template_community

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.list = self.c.get_video_list()
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()
		if request.user.is_anonymous:
			self.template_name = get_template_anon_community(self.list, "communities/video/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community(self.list, "communities/video/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
		return super(CommunityVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityVideo,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.list, self.list
		return c

	def get_queryset(self):
		return self.video_list


class CommunityVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoList
		from common.templates import get_template_anon_community, get_template_community

		self.community,self.list = Community.objects.get(pk=self.kwargs["pk"]), VideoList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()
		if self.list.type == VideoList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/video/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.list, "communities/video/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_community(self.list, "communities/video/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_community(self.playlist, "communities/video/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
		return super(CommunityVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityVideoList,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		return self.video_list


class CommunityPostsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from posts.models import PostList
		from common.template.post import get_permission_community_post

		self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), PostList.objects.get(pk=self.kwargs["list_pk"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.posts_list = self.list.get_staff_items()
			self.post_lists = PostList.get_community_staff_lists(self.kwargs["pk"])
		else:
			self.posts_list = self.list.get_items()
			self.post_lists = PostList.get_community_lists(self.kwargs["pk"])
		self.template_name = get_permission_community_post(self.list, "communities/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityPostsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPostsListView,self).get_context_data(**kwargs)
		c['community'], c['post_lists'], c['list'], c['fix_list'] = self.c, self.post_lists, self.list, self.c.get_fix_list()
		return c

	def get_queryset(self):
		return self.posts_list


class PostsDraftCommunity(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            if request.user.is_staff_of_community(self.c.pk):
                self.template_name = "communities/list/draft_list.html"
        return super(PostsDraftCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostsDraftCommunity,self).get_context_data(**kwargs)
        context["community"] = self.c
        return context

    def get_queryset(self):
        return self.c.get_draft_posts().order_by('-created')

class PostsUserDraftCommunity(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_authenticated:
            if request.user.get_draft_posts_of_community_with_pk(self.c.pk):
                self.template_name = "communities/list/user_draft_list.html"
        return super(PostsUserDraftCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostsUserDraftCommunity,self).get_context_data(**kwargs)
        context["community"] = self.c
        return context

    def get_queryset(self):
        return self.c.get_draft_posts_for_user(self.request.user.pk).order_by('-created')
