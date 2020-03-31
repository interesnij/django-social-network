from music.models import *
from django.views.generic.base import TemplateView
import json


class TagMusicGet(TemplateView):
    template_name="music/get/tag_music.html"

    def get(self,request,*args,**kwargs):
        self.tag = SoundTags.objects.get(pk=self.kwargs["pk"])
        self.list_ = SoundcloudParsing.objects.filter(tag=self.tag)
        self.result = reversed(list(self.list_))
        return super(TagMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(TagMusicGet,self).get_context_data(**kwargs)
        context["tag"] = self.tag
        context["list"] = self.result
        return context
