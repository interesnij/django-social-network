from django.views.generic import ListView
from common.template.user import get_settings_template


class UserLoadPhoto(ListView):
	template_name = 'load/u_photo_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class UserLoadPhotoComment(ListView):
	template_name = 'load/u_photo_comments_load.html'
	paginate_by = 15

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class UserLoadVideo(ListView):
	template_name = 'load/u_video_load.html'
	paginate_by = 15

	def get_queryset(self):
		videos_list = self.request.user.get_video().order_by('-created')
		return videos_list

class UserLoadMusic(ListView):
	template_name = 'load/u_music_load.html'
	paginate_by = 15

	def get_queryset(self):
		musics_list = self.request.user.get_music().order_by('-created_at')
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

class UserLoadArticle(ListView):
	template_name = 'load/u_article_load.html'
	paginate_by = 15

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list

class UserLoadGood(ListView):
	template_name = 'load/u_good_load.html'
	paginate_by = 15

	def get_queryset(self):
		goods_list = self.request.user.get_goods()
		return goods_list


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

	def get_queryset(self):
		goods_list = self.request.user.get_goods()
		return goods_list
