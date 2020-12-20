from django.views.generic import ListView
from common.template.user import get_settings_template


class UserLoadPhoto(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album

		self.album, self.template_name = Album.objects.get(creator_id=request.user.pk, type=Album.MAIN, community__isnull=True), get_settings_template("users/load/u_photo_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhoto,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhoto,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		photo_list = self.album.get_photos()
		return photo_list


class UserLoadPhotoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album

		self.album, self.template_name = Album.objects.get(uuid=self.kwargs["uuid"]), get_settings_template("users/load/u_photo_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoAlbum,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		photo_list = self.album.get_photos()
		return photo_list

class UserLoadPhotoComment(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album
		self.album, self.template_name = Album.objects.get(creator_id=request.user.pk, type=Album.MAIN, community__isnull=True), get_settings_template("users/load/u_photo_comments_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoComment,self).get(request,*args,**kwargs)

	def get_queryset(self):
		photos_list = self.album.get_photos()
		return photos_list

class UserLoadPhotoAlbumComment(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album

		self.album, self.template_name = Album.objects.get(uuid=self.kwargs["uuid"]), get_settings_template("users/load/u_photo_list_comments_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPhotoAlbumComment,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoAlbumComment,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		photo_list = self.album.get_photos()
		return photo_list


class UserLoadVideo(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.album, self.template_name = VideoAlbum.objects.get(creator_id=request.user.pk, type=VideoAlbum.MAIN, community__isnull=True), get_settings_template("users/load/u_video_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideo,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		videos_list = self.album.get_queryset()
		return videos_list

class UserLoadVideoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.album, self.template_name = VideoAlbum.objects.get(uuid=self.kwargs["uuid"]), get_settings_template("users/load/u_video_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideoAlbum,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		video_list = self.album.get_queryset().order_by('-created')
		return video_list


class UserLoadMusic(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.playlist = SoundList.objects.get(creator_id=request.user.pk, type=SoundList.MAIN, community__isnull=True)
		self.template_name = get_settings_template("users/load/u_music_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusic,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		musics_list = self.playlist.playlist_too().order_by('-created_at')
		return musics_list

class UserLoadMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_music_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusicList,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		musics_list = self.playlist.playlist_too().order_by('-created_at')
		return musics_list


class UserLoadDoc(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(creator_id=request.user.pk, type=DocList.MAIN, community__isnull=True)
		self.template_name = get_settings_template("users/load/u_doc_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDoc,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoc,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		doc_list = self.list.get_docs().order_by('-created')
		return doc_list

class UserLoadDocList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_doc_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		doc_list = self.list.get_docs().order_by('-created')
		return doc_list


class UserLoadArticle(ListView):
	template_name = 'load/u_article_load.html'
	paginate_by = 15

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list

class UserLoadGood(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		self.album = GoodAlbum.objects.get(type=GoodAlbum.MAIN, creator=request.user, community__isnull=True)
		self.template_name = get_settings_template("users/load/u_good_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadGood,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		goods_list = self.album.get_goods()
		return goods_list

class UserLoadGoodList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("users/load/u_good_list_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadGoodList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadGoodList,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		good_list = self.album.get_goods().order_by('-created')
		return good_list


class CommunityLoadPhoto(ListView):
	template_name = 'users/load/c_photo_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class CommunityLoadPhotoComment(ListView):
	template_name = 'users/load/c_photo_comments_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class CommunityLoadVideo(ListView):
	template_name = 'users/load/c_video_load.html'
	paginate_by = 15

	def get_queryset(self):
		videos_list = self.request.user.get_video().order_by('-created')
		return videos_list

class CommunityLoadMusic(ListView):
	template_name = 'users/load/c_music_load.html'
	paginate_by = 15

	def get_queryset(self):
		musics_list = self.request.user.get_music().order_by('-created_at')
		return musics_list

class CommunityLoadArticle(ListView):
	template_name = 'users/load/c_article_load.html'
	paginate_by = 15

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list


class CommunityLoadGood(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import GoodAlbum
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.album = GoodAlbum.objects.get(type=GoodAlbum.MAIN, community=self.community)
		self.template_name = get_settings_template("users/load/c_good_load.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityLoadGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityLoadGood,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		goods_list = self.album.get_goods()
		return goods_list


class ChatItemsLoad(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/chat_items.html", request.user, request.META['HTTP_USER_AGENT'])
		self.total_list = request.user.get_chats_and_connections()
		return super(ChatItemsLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		total_list = self.total_list
		return total_list


class CommunitiesLoad(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/communities.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = request.user.get_staffed_communities()
		return super(CommunitiesLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		list = self.list
		return list


class FriendsLoad(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/load/friends.html", request.user, request.META['HTTP_USER_AGENT'])
		self.list = request.user.get_all_connection()
		return super(FriendsLoad,self).get(request,*args,**kwargs)

	def get_queryset(self):
		list = self.list
		return list
