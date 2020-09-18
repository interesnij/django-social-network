from django.views.generic import ListView
from common.template.user import get_settings_template


class UserLoadPhoto(ListView):
	template_name = 'load/u_photo_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class UserLoadPhotoAlbum(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album
		self.album = Album.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("load/u_photo_list_load.html", request)
		return super(UserLoadPhotoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoAlbum,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		photo_list = self.album.get_photos().order_by('-created')
		return photo_list

class UserLoadPhotoComment(ListView):
	template_name = 'load/u_photo_comments_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class UserLoadPhotoAlbumComment(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from gallery.models import Album
		self.album = Album.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("load/u_photo_list_comments_load.html", request)
		return super(UserLoadPhotoAlbumComment,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPhotoAlbumComment,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		photo_list = self.album.get_photos().order_by('-created')
		return photo_list


class UserLoadVideo(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum
		self.album = VideoAlbum.objects.get(creator_id=request.user.pk, type=VideoAlbum.MAIN, community=None)
		self.template_name = get_settings_template("load/u_video_load.html", request)
		return super(UserLoadVideo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideo,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		videos_list = self.request.user.get_video().order_by('-created')
		return videos_list

class UserLoadVideoAlbum(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("load/u_video_list_load.html", request)
		return super(UserLoadVideoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadVideoAlbum,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		video_list = self.album.get_queryset().order_by('-created')
		return video_list


class UserLoadMusic(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.playlist = SoundList.objects.get(creator_id=request.user.pk, type=SoundList.MAIN, community=None)
		self.template_name = get_settings_template("load/u_music_load.html", request)
		return super(UserLoadMusic,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusic,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		musics_list = self.playlist.playlist_too().order_by('-created_at')
		return musics_list

class UserLoadMusicList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("load/u_music_list_load.html", request)
		return super(UserLoadMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadMusicList,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context

	def get_queryset(self):
		musics_list = self.playlist.playlist_too().order_by('-created_at')
		return musics_list


class UserLoadDoc(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(creator_id=request.user.pk, type=DocList.MAIN, community=None)
		self.template_name = get_settings_template("load/u_doc_load.html", request)
		return super(UserLoadDoc,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoc,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		doc_list = self.list.get_docs().order_by('-created_at')
		return doc_list

class UserLoadDocList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("load/u_doc_list_load.html", request)
		return super(UserLoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

	def get_queryset(self):
		doc_list = self.list.get_docs().order_by('-created_at')
		return doc_list


class UserLoadArticle(ListView):
	template_name = 'load/u_article_load.html'
	paginate_by = 15

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list

class UserLoadGood(ListView):
	template_name = 'load/u_good_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		self.album = GoodAlbum.objects.get(type=GoodAlbum.MAIN, creator=request.user, community=None)
		self.template_name = get_settings_template("load/u_good_load.html", request)
		return super(UserLoadGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadGood,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		goods_list = self.album.get_goods()
		return goods_list

class UserLoadGoodList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_settings_template("load/u_good_list_load.html", request)
		return super(UserLoadGoodList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadGoodList,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		good_list = self.album.get_goods().order_by('-created')
		return good_list


class CommunityLoadPhoto(ListView):
	template_name = 'load/c_photo_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class CommunityLoadPhotoComment(ListView):
	template_name = 'load/c_photo_comments_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class CommunityLoadVideo(ListView):
	template_name = 'load/c_video_load.html'
	paginate_by = 15

	def get_queryset(self):
		videos_list = self.request.user.get_video().order_by('-created')
		return videos_list

class CommunityLoadMusic(ListView):
	template_name = 'load/c_music_load.html'
	paginate_by = 15

	def get_queryset(self):
		musics_list = self.request.user.get_music().order_by('-created_at')
		return musics_list

class CommunityLoadArticle(ListView):
	template_name = 'load/c_article_load.html'
	paginate_by = 15

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list


class CommunityLoadGood(ListView):
	template_name = 'load/c_good_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from music.models import GoodAlbum
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.album = GoodAlbum.objects.get(type=GoodAlbum.MAIN, community=self.community)
		self.template_name = get_settings_template("load/c_good_load.html", request)
		return super(CommunityLoadGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityLoadGood,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context

	def get_queryset(self):
		goods_list = self.album.get_goods()
		return goods_list
