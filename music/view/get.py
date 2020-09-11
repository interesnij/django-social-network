from music.models import *
from django.views.generic.base import TemplateView
import json
from common.template.user import get_settings_template


class TagMusicGet(TemplateView):
    template_name="music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.tag = SoundTags.objects.get(pk=self.kwargs["pk"])
        self.list_ = SoundcloudParsing.objects.filter(tag=self.tag)
        self.list_ = self.list_[0:100]
        self.result = reversed(list(self.list_))
        return super(TagMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(TagMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context

class GenreMusicGet(TemplateView):
    template_name="music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.genre = SoundGenres.objects.get(pk=self.kwargs["pk"])
        self.list_ = SoundcloudParsing.objects.filter(genre=self.genre)
        self.list_ = self.list_[0:100]
        self.result = reversed(list(self.list_))
        return super(GenreMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GenreMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context

class ListMusicGet(TemplateView):
    template_name="music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list = SoundList.objects.get(pk=self.kwargs["pk"])
        self.list_ = SoundcloudParsing.objects.filter(list=self.list)
        self.list_ = self.list_[0:100]
        self.result = reversed(list(self.list_))
        return super(ListMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context


class MusicPlaylistPreview(TemplateView):
	template_name = 'load/u_music_load.html'
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.playlist = SoundList.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("music/playlist_preview.html", request)
		return super(MusicPlaylistPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(MusicPlaylistPreview,self).get_context_data(**kwargs)
		context["playlist"] = self.playlist
		return context
