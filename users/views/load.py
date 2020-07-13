from users.models import User
from django.views.generic import ListView


class UserPhotosList(ListView):
	template_name = 'load/u_photos_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(UserPhotosList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list
class UserPhotosCommentList(ListView):
	template_name = 'load/u_photos_comments_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(UserPhotosCommentList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list
class UserVideosList(ListView):
	template_name = 'load/u_videos_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(UserVideosList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		videos_list = self.request.user.get_video().order_by('-created')
		return videos_list
class UserMusicsList(ListView):
	template_name = 'load/u_musics_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(UserMusicsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		musics_list = self.request.user.get_music().order_by('-created_at')
		return musics_list
class UserArticlesList(ListView):
	template_name = 'load/u_articles_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(UserArticlesList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list
class UserGoodsList(ListView):
	template_name = 'load/u_goods_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(UserGoodsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		goods_list = self.request.user.get_goods()
		return goods_list


class CommunityPhotosList(ListView):
	template_name = 'load/c_photos_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(CommentPhotosList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class CommunityPhotosCommentList(ListView):
	template_name = 'load/c_photos_comments_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(CommentPhotosCommentList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		photos_list = self.request.user.get_photos().order_by('-created')
		return photos_list

class CommunityVideosList(ListView):
	template_name = 'load/c_videos_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(CommentVideosList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		videos_list = self.request.user.get_video().order_by('-created')
		return videos_list

class CommunityMusicsList(ListView):
	template_name = 'load/c_musics_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(CommentMusicsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		musics_list = self.request.user.get_music().order_by('-created_at')
		return musics_list

class CommunityArticlesList(ListView):
	template_name = 'load/c_articles_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(CommentArticlesList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		articles_list = self.request.user.get_articles().order_by('-created')
		return articles_list

class CommunityGoodsList(ListView):
	template_name = 'load/c_goods_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		return super(CommentGoodsList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		goods_list = self.request.user.get_goods()
		return goods_list
