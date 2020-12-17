from django.views.generic import ListView
from communities.models import Community, CommunityCategory
from common.template.user import get_default_template


class CommunityMembersView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_default_template("communities/detail/", "members.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"] = self.c
		return context

	def get_queryset(self):
		membersheeps = self.c.get_members(self.c.pk)
		return membersheeps


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
		frends = self.request.user.get_common_friends_of_community(self.c.pk)
		return frends


class AllCommunities(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_default_template("communities/list/", "all_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		groups = Community.get_trending_communities()
		return groups

	def get_context_data(self,**kwargs):
		context = super(AllCommunities,self).get_context_data(**kwargs)
		context["communities_categories"] = CommunityCategory.objects.only("pk")
		context["count_communities"] = Community.objects.all().values("pk").count()
		return context


class TrendCommunities(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_default_template("communities/list/", "trend_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(TrendCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		groups = Community.get_trending_communities()
		return groups

	def get_context_data(self,**kwargs):
		context = super(TrendCommunities,self).get_context_data(**kwargs)
		context["communities_categories"] = CommunityCategory.objects.only("pk")
		context["count_communities"] = Community.objects.all().values("pk").count()
		return context


class CommunityCategoryView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.cat, self.template_name = CommunityCategory.objects.get(pk=self.kwargs["pk"]), get_default_template("communities/list/", "cat_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityCategoryView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityCategoryView,self).get_context_data(**kwargs)
		context["category"]=self.cat
		context["communities_categories"] = CommunityCategory.objects.only("pk")
		return context

	def get_queryset(self):
		return Community.objects.filter(category__sudcategory_id = self.kwargs["pk"])


class CommunityDocs(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.template.doc import get_template_community_doc

		self.c, user = Community.objects.get(pk=self.kwargs["pk"]), request.user

		try:
			self.list = DocList.objects.get(community_id=self.c.pk, type=DocList.MAIN)
		except:
			self.list = DocList.objects.create(community_id=self.c.pk, creator=self.c.creator, type=DocList.MAIN, name="Основной список")
		if user.is_authenticated and user.is_staff_of_community(self.c.pk):
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		self.template_name = get_template_community_doc(self.c, "communities/docs/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityDocs,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityDocs,self).get_context_data(**kwargs)
		context['community'] = self.c
		context['list'] = self.list
		return context

	def get_queryset(self):
		doc_list = self.doc_list
		return doc_list

class CommunityDocsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.template.doc import get_template_community_doc

		self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		if self.list.type == DocList.MAIN:
			self.template_name = get_template_community_doc(self.c, "communities/docs/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community_doc(self.c, "communities/docs_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityDocsList,self).get_context_data(**kwargs)
		context['community'] = self.c
		context['list'] = self.list
		return context

	def get_queryset(self):
		doc_list = self.doc_list
		return doc_list


class CommunityGoods(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		from common.template.good import get_template_community_good

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.album = GoodAlbum.objects.get(community=self.c, type=GoodAlbum.MAIN)
		except:
			self.album = GoodAlbum.objects.create(creator=self.c.creator, community=self.c, type=GoodAlbum.MAIN, title="Основной список")
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.goods_list = self.album.get_staff_goods()
		else:
			self.goods_list = self.album.get_goods()
		self.template_name = get_template_community_good(self.c, "communities/goods/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityGoods,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityGoods,self).get_context_data(**kwargs)
		context['community'] = self.c
		context['album'] = self.album
		return context

	def get_queryset(self):
		goods_list = self.goods_list
		return goods_list

class CommunityGoodsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		from common.template.good import get_template_community_good

		self.c, self.album = Community.objects.get(pk=self.kwargs["pk"]), GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.goods_list = self.album.get_staff_goods()
		else:
			self.goods_list = self.album.get_goods()

		if self.album.type == GoodAlbum.MAIN:
			self.template_name = get_template_community_good(self.c, "communities/goods/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community_good(self.c, "communities/goods_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityGoodsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityGoodsList,self).get_context_data(**kwargs)
		context['community'] = self.c
		context['album'] = self.album
		return context

	def get_queryset(self):
		goods_list = self.goods_list
		return goods_list


class CommunityMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		from common.template.music import get_template_community_music

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.playlist, self.template_name = SoundList.objects.get(community_id=self.c.pk, type=SoundList.MAIN), get_template_community_music(self.c, "communities/music/", "list.html", request.user, request.META['HTTP_USER_AGENT'])

	def get_context_data(self,**kwargs):
		c = super(CommunityMusic,self).get_context_data(**kwargs)
		c['community'], c['playlist'] = self.c, self.playlist
		return c

	def get_queryset(self):
		music_list = self.c.get_music()
		return music_list

class CommunityMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		from common.template.music import get_template_community_music

		self.community, self.playlist = Community.objects.get(pk=self.kwargs["pk"]), SoundList.objects.get(uuid=self.kwargs["uuid"])
		if self.playlist.type == SoundList.MAIN:
			self.template_name = get_template_community_music(self.c, "communities/music/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community_music(self.c, "communities/music_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityMusicList,self).get_context_data(**kwargs)
		c['community'], c['playlist'] = self.c, self.playlist
		return c

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist


class CommunityVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum
		from common.template.video import get_template_community_video

		self.c = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_template_community_video(self.c, "communities/video/", "list.html", request.user, request.META['HTTP_USER_AGENT'])

		self.album = VideoAlbum.objects.get(community_id=self.c.pk, type=VideoAlbum.MAIN)
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.video_list = self.album.get_my_queryset()
		else:
			self.video_list = self.album.get_queryset()
		return super(CommunityVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideo,self).get_context_data(**kwargs)
		context['community'] = self.c
		context['album'] = self.album
		return context

	def get_queryset(self):
		video_list = self.video_list
		return video_list


class CommunityVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum
		from common.template.video import get_template_community_video

		self.community, self.album = Community.objects.get(pk=self.kwargs["pk"]), VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated and request.user.is_staff_of_community(self.c.pk):
			self.video_list = self.album.get_my_queryset()
		else:
			self.video_list = self.album.get_queryset()
		if self.album.type == VideoAlbum.MAIN:
			self.template_name = get_template_community_video(self.c, "communities/video/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_community_video(self.c, "communities/video_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideoList,self).get_context_data(**kwargs)
		context['community'] = self.c
		context['album'] = self.album
		return context

	def get_queryset(self):
		video_list = self.video_list
		return video_list


class CommunityPostsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from posts.models import PostList
		from django.http import Http404
		from common.template.post import get_permission_community_post

		self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), PostList.objects.get(pk=self.kwargs["list_pk"])
		if self.list.is_private_list():
			if request.user.is_anonymous or not request.user.is_staff_of_community(self.c.pk):
				raise Http404
			else:
				self.posts_list = self.list.get_posts()
		else:
			self.posts_list = self.list.get_posts()
		self.template_name = get_permission_community_post(self.c, "communities/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityPostsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityPostsListView,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		posts_list = self.posts_list
		return posts_list


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
        item_list = self.c.get_draft_posts().order_by('-created')
        return item_list

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
        item_list = self.c.get_draft_posts_for_user(self.request.user.pk).order_by('-created')
        return item_list
