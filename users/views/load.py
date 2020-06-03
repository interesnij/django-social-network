from users.models import User
from django.views.generic import ListView


class UserImagesList(ListView):
	template_name = 'photos_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserImagesList,self).get(request,*args,**kwargs)

	def get_queryset(self): 
		photos = self.request.user.get_photos()
		return photos


class UserVideoList(ListView):
	template_name = 'videos_load.html'
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_queryset(self):
		video_list = self.request.user.get_video()
		return video_list
