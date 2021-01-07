from communities.models import Community
from django.views.generic import ListView
from music.models import SoundList
from common.template.music import get_template_community_music


class CommunityLoadPlaylist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.community, self.playlist = Community.objects.get(pk=self.kwargs["pk"]), SoundList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_template_community_music(self.c, "music/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityLoadPlaylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityLoadPlaylist,self).get_context_data(**kwargs)
		c['community'], c['playlist'] = self.c, self.playlist
		return c

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist
