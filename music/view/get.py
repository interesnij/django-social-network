from music.models import *
from django.views.generic.base import TemplateView


class TagMusicGet(TemplateView):
    template_name="music/get/tag_music.html"

    def get(self,request,*args,**kwargs):
        self.tag = SoundTags.objects.get(pk=self.kwargs["pk"])
        return super(TagMusicGet,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(TagMusicGet,self).get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
