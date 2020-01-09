from django.views import View
from django.shortcuts import render_to_response
from music.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


class TagsList(View):
    def get(self, request, *args, **kwargs):
        context = {}
        symbol = SoundSymbol.objects.get(pk=self.kwargs["pk"])
        tag_list = SoundTags.objects.filter(symbol=symbol)
        current_page = Paginator(tag_list, 24)
        page = request.GET.get('page')
        context['symbol'] = symbol
        context['request_user'] = request.user

        try:
            context['tag_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['tag_list'] = current_page.page(1)
        except EmptyPage:
            context['tag_list'] = current_page.page(current_page.num_pages)
        return render_to_response('music/tags_list.html', context)
