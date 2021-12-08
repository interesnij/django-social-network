from django.views.generic import ListView
from common.templates import get_settings_template


class UserLoadPhoto(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList

		self.list, self.template_name = request.user.get_photo_list(), get_settings_template("users/load/u_photo_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = PhotoList.get_user_lists(request.user.pk)
		return super(UserLoadPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhoto,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadPhotoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList

		self.list, self.template_name = PhotoList.objects.get(uuid=self.kwargs["uuid"]), get_settings_template("users/load/u_photo_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadPhotoComment(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList
		self.list, self.template_name = request.user.get_photo_list(), get_settings_template("users/load/u_photo_comments_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = PhotoList.get_user_lists(request.user.pk)
		return super(UserLoadPhotoComment,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoComment,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadPhotoMessage(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList
		self.list, self.template_name = request.user.get_photo_list(), get_settings_template("users/load/u_photo_message_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = PhotoList.get_user_lists(request.user.pk)
		return super(UserLoadPhotoMessage,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoMessage,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoList

		self.list, self.template_name = request.user.get_video_list(), get_settings_template("users/load/u_video_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = VideoList.get_user_lists(request.user.pk)
		return super(UserLoadVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideo,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoList

		self.list, self.template_name = VideoList.objects.get(uuid=self.kwargs["uuid"]), get_settings_template("users/load/u_video_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import MusicList
		self.list = request.user.get_playlist()
		self.template_name = get_settings_template("users/load/u_music_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = MusicList.get_user_lists(request.user.pk)
		return super(UserLoadMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusic,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items().order_by('-created')

class UserLoadMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import MusicList
		self.playlist = MusicList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_music_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusicList,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		return self.playlist.get_items()


class UserLoadDoc(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocsList

		self.list = request.user.get_doc_list()
		self.template_name = get_settings_template("users/load/u_doc_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = DocsList.get_user_lists(request.user.pk)
		return super(UserLoadDoc,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoc,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadDocList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocsList
		self.list = DocsList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_doc_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadArticle(ListView):
	template_name = 'load/u_article_load.html'
	paginate_by = 15

	def get_queryset(self):
		return self.request.user.get_articles()

class UserLoadSurvey(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from survey.models import SurveyList
		self.list = request.user.get_survey_list()
		self.template_name = get_settings_template("users/load/u_survey_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = SurveyList.get_user_lists(request.user.pk)
		return super(UserLoadSurvey,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadSurvey,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadSurveyList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocsList
		self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_survey_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserSurveyDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadSurveyList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserLoadGood(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodList

		self.list = request.user.get_good_list()
		self.template_name = get_settings_template("users/load/u_good_load.html", request.user, request.META['HTTP_USER_AGENT'])
		self.get_lists = GoodList.get_user_lists(request.user.pk)
		return super(UserLoadGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadGood,self).get_context_data(**kwargs)
		context["list"], context["get_lists"] = self.list, self.get_lists
		return context

	def get_queryset(self):
		return self.list.get_items()

class UserLoadGoodList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodList
		self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_good_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadGoodList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadGoodList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class ChatItemsLoad(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/chat_items.html", request.user, request.META['HTTP_USER_AGENT'])
		self.total_list = request.user.get_chats_and_connections()
		return super(ChatItemsLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.total_list


class CommunitiesLoad(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/communities.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = request.user.get_staffed_communities()
		return super(CommunitiesLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.list


class FriendsLoad(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/friends.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = request.user.get_all_connection()
		return super(FriendsLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.list


from django.views.generic.base import TemplateView

class SmilesStickersLoad(TemplateView):
	template_name, populate_smiles, populate_stickers = None, None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/smiles_stickers.html", request.user, request.META['HTTP_USER_AGENT'])
		self.is_have_populate_smiles = request.user.is_have_populate_smiles()
		if self.is_have_populate_smiles:
			self.populate_smiles = request.user.get_populate_smiles()
		self.is_have_populate_stickers = request.user.is_have_populate_stickers()
		if self.is_have_populate_stickers:
			self.populate_stickers = request.user.get_populate_stickers()
		return super(SmilesStickersLoad,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from common.model.other import SmileCategory, StickerCategory
		context = super(SmilesStickersLoad,self).get_context_data(**kwargs)
		context["smiles_category"] = SmileCategory.objects.only("pk")
		context["stickers_category"] = StickerCategory.objects.only("pk")
		context["populate_smiles"] = self.populate_smiles
		context["populate_stickers"] = self.populate_stickers
		context["is_have_populate_smiles"] = self.is_have_populate_smiles
		context["is_have_populate_stickers"] = self.is_have_populate_stickers
		return context

class SmilesLoad(TemplateView):
	template_name, populate_smiles = None, None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/smiles.html", request.user, request.META['HTTP_USER_AGENT'])
		self.is_have_populate_smiles = request.user.is_have_populate_smiles()
		if self.is_have_populate_smiles:
			self.populate_smiles = request.user.get_populate_smiles()
		return super(SmilesLoad,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from common.model.other import SmileCategory, StickerCategory
		context = super(SmilesLoad,self).get_context_data(**kwargs)
		context["smiles_category"] = SmileCategory.objects.only("pk")
		context["populate_smiles"] = self.populate_smiles
		context["is_have_populate_smiles"] = self.is_have_populate_smiles
		return context


class ChatsLoad(ListView):
	template_name, paginate_by = None, 20

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/chats.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = request.user.get_all_chats()
		return super(ChatsLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.list


class LoadListExcludeUsers(ListView):
	template_name, users = None, None

	def get(self,request,*args,**kwargs):
		from common.templates import get_detect_platform_template

		self.type = request.GET.get("action")
		self.target = request.GET.get("target")
		self.community_pk = request.GET.get("community_pk")
		data = request.GET.get("list")
		if self.type == "can_see_el":
			self.text = "видеть записи"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_exclude_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_exclude_users()
			elif data[:3] == "doc":
				from docs.models import DocsList
				list = DocsList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_exclude_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_exclude_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_exclude_users()
			elif data[:3] == "mus":
				from music.models import MusicList
				list = MusicList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_exclude_users()
		elif self.type == "can_see_comment":
			self.text = "видеть комментарии"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_exclude_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_exclude_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_exclude_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_exclude_users()
		elif self.type == "create_el":
			self.text = "создавать записи"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_create_el_exclude_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_create_el_exclude_users()
			elif data[:3] == "doc":
				from docs.models import DocsList
				list = DocsList.objects.get(pk=data[3:])
				self.users = list.get_create_el_exclude_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_create_el_exclude_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_create_el_exclude_users()
			elif data[:3] == "mus":
				from music.models import MusicList
				list = MusicList.objects.get(pk=data[3:])
				self.users = list.get_create_el_exclude_users()
		elif self.type == "create_comment":
			self.text = "создавать комментарии"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_exclude_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_exclude_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_exclude_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_exclude_users()
		elif self.type == "copy_el":
			self.text = "копировать записи и список"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_exclude_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_exclude_users()
			elif data[:3] == "doc":
				from docs.models import DocsList
				list = DocsList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_exclude_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_exclude_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_exclude_users()
			elif data[:3] == "mus":
				from music.models import MusicList
				list = MusicList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_exclude_users()

		if self.community_pk and request.user.is_administrator_of_community(self.community_pk):
			self.template_name = get_detect_platform_template("users/load/list_exclude_users.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.target == "user":
			self.template_name = get_detect_platform_template("users/load/list_exclude_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadListExcludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadListExcludeUsers,self).get_context_data(**kwargs)
		context["text"] = self.text
		context["type"] = self.type
		context["users"] = self.users
		return context

	def get_queryset(self):
		if self.target == "user":
			return self.request.user.get_all_connection()
		elif self.community_pk:
			from communities.models import Community
			community = Community.objects.get(pk=self.community_pk)
			return community.get_members()

class LoadListIncludeUsers(ListView):
	template_name, users = None, None

	def get(self,request,*args,**kwargs):
		from common.templates import get_detect_platform_template

		self.type = request.GET.get("action")
		self.target = request.GET.get("target")
		self.community_pk = request.GET.get("community_pk")
		data = request.GET.get("list")
		if self.type == "can_see_el":
			self.text = "видеть записи"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_include_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_include_users()
			elif data[:3] == "doc":
				from docs.models import DocsList
				list = DocsList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_include_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_include_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_include_users()
			elif data[:3] == "mus":
				from music.models import MusicList
				list = MusicList.objects.get(pk=data[3:])
				self.users = list.get_can_see_el_include_users()
		elif self.type == "can_see_comment":
			self.text = "видеть комментарии"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_include_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_include_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_include_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_can_see_comment_include_users()
		elif self.type == "create_el":
			self.text = "создавать записи"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_create_el_include_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_create_el_include_users()
			elif data[:3] == "doc":
				from docs.models import DocsList
				list = DocsList.objects.get(pk=data[3:])
				self.users = list.get_create_el_include_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_create_el_include_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_create_el_include_users()
			elif data[:3] == "mus":
				from music.models import MusicList
				list = MusicList.objects.get(pk=data[3:])
				self.users = list.get_create_el_include_users()
		elif self.type == "create_comment":
			self.text = "создавать комментарии"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_include_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_include_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_include_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_create_comment_include_users()
		elif self.type == "copy_el":
			self.text = "копировать записи и список"
			if data[:3] == "pos":
				from posts.models import PostsList
				list = PostsList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_include_users()
			elif data[:3] == "pho":
				from gallery.models import PhotoList
				list = PhotoList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_include_users()
			elif data[:3] == "doc":
				from docs.models import DocsList
				list = DocsList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_include_users()
			elif data[:3] == "goo":
				from goods.models import GoodList
				list = GoodList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_include_users()
			elif data[:3] == "vid":
				from video.models import VideoList
				list = VideoList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_include_users()
			elif data[:3] == "mus":
				from music.models import MusicList
				list = MusicList.objects.get(pk=data[3:])
				self.users = list.get_copy_el_include_users()
		if self.community_pk and request.user.is_administrator_of_community(self.community_pk):
			self.template_name = get_detect_platform_template("users/load/list_include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		elif self.target == "user":
			self.template_name = get_detect_platform_template("users/load/list_include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadListIncludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadListIncludeUsers,self).get_context_data(**kwargs)
		context["text"] = self.text
		context["type"] = self.type
		context["users"] = self.users
		return context

	def get_queryset(self):
		if self.target == "user":
			return self.request.user.get_all_connection()
		elif self.community_pk:
			from communities.models import Community
			community = Community.objects.get(pk=self.community_pk)
			return community.get_members()
