from music.models import *
from django.views.generic.base import TemplateView
import json


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
        self.list_ = SoundcloudParsing.objects.filter(players=self.list)
        self.list_ = self.list_[0:100]
        self.result = reversed(list(self.list_))
        return super(ListMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context


class UserCreatePlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music/", template="create_list.html", request=request)
        return super(UserCreatePlaylistWindow,self).get(request,*args,**kwargs)
