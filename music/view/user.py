from users.models import User
from django.views.generic import ListView
from music.models import SoundList
from common.template.music import get_template_user_music


class UserLoadPlaylist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_template_user_music(self.user, "music/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadPlaylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadPlaylist,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['playlist'] = self.playlist
		return context

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist
