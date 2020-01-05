from django.views import View
from django.shortcuts import render_to_response
from music.models import *



class AllMusicListView(View):

    def get(self,request,*args,**kwargs):
        context = {}
        player = SoundList.objects.get(id=2)
        all_tracks = player.get_json_playlist()
        context['all_tracks'] = all_tracks
        context['player'] = player
        return render_to_response('music/all_music_list2.html', context)


class AllTagListView(View):

    def get(self,request,*args,**kwargs):
        context = {}
        tag=SoundTags.objects.get(pk=self.kwargs["pk"])
        all_tracks = tag.get_json_playlist()
        context['all_tracks'] = all_tracks
        context['tag'] = tag
        return render_to_response('music/tag_music_list.html', context)
