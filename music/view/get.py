from music.models import *
from django.views.generic.base import TemplateView
from common.template.user import get_settings_template


class TagMusicGet(TemplateView):
    template_name = "music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list_ = SoundcloudParsing.objects.filter(tag_id=self.kwargs["pk"])[0:100]
        self.result = reversed(list(self.list_))
        return super(TagMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(TagMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context

class GenreMusicGet(TemplateView):
    template_name = "music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list_ = SoundcloudParsing.objects.filter(genre_id=self.kwargs["pk"])[0:100]
        self.result = reversed(list(self.list_))
        return super(GenreMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GenreMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context

class ListMusicGet(TemplateView):
    template_name = "music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list = SoundList.objects.get(pk=self.kwargs["pk"])
        return super(ListMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.list.playlist_too()[0:50]
        return context


class MusicPlaylistPreview(TemplateView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.playlist, self.template_name = SoundList.objects.get(pk=self.kwargs["pk"]), get_settings_template("music/playlist_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MusicPlaylistPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MusicPlaylistPreview,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context
