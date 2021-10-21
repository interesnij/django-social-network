from music.models import *
from django.views.generic.base import TemplateView
from common.templates import get_settings_template


class TagMusicGet(TemplateView):
    template_name = "desctop/music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list_ = Music.objects.filter(tag_id=self.kwargs["pk"])[0:100]
        self.result = reversed(list(self.list_))
        return super(TagMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(TagMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context

class GenreMusicGet(TemplateView):
    template_name = "desctop/music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list_ = Music.objects.filter(genre_id=self.kwargs["pk"])[0:100]
        self.result = reversed(list(self.list_))
        return super(GenreMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GenreMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.result
        return context

class ListMusicGet(TemplateView):
    template_name = "desctop/music/load_playlist.html"

    def get(self,request,*args,**kwargs):
        self.list = SoundList.objects.get(pk=self.kwargs["pk"])
        return super(ListMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListMusicGet,self).get_context_data(**kwargs)
        context["list"] = self.list.get_items()[0:50]
        return context
