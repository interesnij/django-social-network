import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic import ListView
from communities.models import Community, CommunityMembership, CommunityCategory
from users.models import User
from common.check.community import check_can_get_lists
from common.template.post import get_template_community_post, get_permission_community_post
from common.template.music import get_template_community_music
from common.template.video import get_template_community_video
from common.template.good import get_template_community_good
from common.template.doc import get_template_community_doc
from django.http import Http404
from common.template.user import get_default_template


class CommunityMembersView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_default_template(folder="c_list/", template="members.html", request=request)
		return super(CommunityMembersView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMembersView,self).get_context_data(**kwargs)
		context["community"] = self.community
		return context

	def get_queryset(self):
		membersheeps = self.community.get_community_with_name_members(self.community.name)
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
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.cat = CommunityCategory.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_default_template(folder="c_list/", template="cat_communities.html", request=request)
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
        self.playlist = SoundList.objects.get(community_id=self.community.pk, type=SoundList.MAIN)
        self.template_name = get_template_community_music(self.community, "c_music/", "list.html", request.user)
        return super(CommunityMusic,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityMusic,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['playlist'] = self.playlist
        return context

    def get_queryset(self):
        music_list = self.community.get_music()
        return music_list

class CommunityDocs(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		try:
			self.list = DocList.objects.get(community_id=self.community.id, type=DocList.MAIN)
		except:
			self.list = DocList.objects.create(community_id=self.community.id, creator=self.community.creator, type=DocList.MAIN, name="Основной список")
		if request.user.is_staff_of_community_with_name(self.community.name):
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		self.template_name = get_template_community_doc(self.community, "c_docs/", "list.html", request.user)
		return super(CommunityDocs,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityDocs,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['list'] = self.list
		return context

	def get_queryset(self):
		doc_list = self.doc_list
		return doc_list

class CommunityDocsList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_staff_of_community_with_name(self.community.name):
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()

		self.template_name = get_template_community_doc(self.community, "c_docs_list/", "list.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return super(CommunityDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityDocsList,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['list'] = self.list
		return context

	def get_queryset(self):
		doc_list = self.doc_list
		return doc_list


class CommunityGoods(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        from goods.models import GoodAlbum

        self.community = Community.objects.get(pk=self.kwargs["pk"])
        try:
            self.album = GoodAlbum.objects.get(community=self.community, type=GoodAlbum.MAIN)
        except:
            self.album = GoodAlbum.objects.create(creator=self.community.creator, community=self.community, type=GoodAlbum.MAIN, title="Основной список")
        if request.user.is_staff_of_community_with_name(self.community.name):
            self.goods_list = self.album.get_staff_goods()
        else:
            self.goods_list = self.album.get_goods()

        self.template_name = get_template_community_good(self.community, "c_goods/", "list.html", request.user)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + self.template_name
        return super(CommunityGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityGoods,self).get_context_data(**kwargs)
        context['community'] = self.community
        context['album'] = self.album
        return context

    def get_queryset(self):
        goods_list = self.goods_list
        return goods_list

class CommunityGoodsList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.goods_list = self.album.get_staff_goods()
		else:
			self.goods_list = self.album.get_goods()

		self.template_name = get_template_community_good(self.community, "c_goods_list/", "list.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return super(CommunityGoodsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityGoodsList,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['album'] = self.album
		return context

	def get_queryset(self):
		goods_list = self.goods_list
		return goods_list


class CommunityMusicList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])

		self.template_name = get_template_community_music(self.community, "c_music_list/", "list.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return super(CommunityMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityMusicList,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['playlist'] = self.playlist
		return context

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist


class CommunityVideo(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_template_community_video(self.community, "c_video/", "list.html", request.user)

		self.album = VideoAlbum.objects.get(community_id=self.community.pk, type=VideoAlbum.MAIN)
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


class CommunityVideoList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.video_list = self.album.get_my_queryset()
		else:
			self.video_list = self.album.get_queryset()

		self.template_name = get_template_community_video(self.community, "c_video_list/", "list.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return super(CommunityVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideoList,self).get_context_data(**kwargs)
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
		if request.is_ajax():
			self.template_name = get_permission_community_post(self.community, "c_lenta/", "list.html", request.user)
		else:
			raise Http404
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

class PostsUserDraftCommunity(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if request.user.is_authenticated:
            if request.user.get_draft_posts_of_community_with_pk(self.community.pk):
                self.template_name = "c_list/user_draft_list.html"
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            self.template_name = "mob_" + template_name
        return super(PostsUserDraftCommunity,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostsUserDraftCommunity,self).get_context_data(**kwargs)
        context["community"] = self.community
        return context

    def get_queryset(self):
        item_list = self.community.get_draft_posts_for_user(self.request.user.pk).order_by('-created')
        return item_list
