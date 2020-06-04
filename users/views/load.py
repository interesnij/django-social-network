from users.models import User
from django.views.generic import ListView


class UserPhotosList(ListView):
	template_name = 'load/photos_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserPhotosList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		photos_list = self.request.user.get_photos()
		return photos_list


class UserVideosList(ListView):
	template_name = 'load/videos_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserVideosList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		videos_list = self.request.user.get_video()
		return videos_list


class UserMusicsList(ListView):
	template_name = 'load/musics_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserMusicsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		musics_list = self.request.user.get_music()
		return musics_list


class UserArticlesList(ListView):
	template_name = 'load/articles_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserArticlesList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		articles_list = self.request.user.get_articles()
		return articles_list


class UserGoodsList(ListView):
	template_name = 'load/goods_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserGoodsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		goods_list = self.request.user.get_goods()
		return goods_list
