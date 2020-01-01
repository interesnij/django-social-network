import soundcloud
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render_to_response
from django.http import JsonResponse


class AllMusicView(TemplateView):
    template_name="all_music.html"


class AllMusicListView(View):
    template_name = "all_music_list.html"
    def get(self,request,*args,**kwargs):
        page_size = 10
        client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
        all_tracks = client.get('/tracks', order='created_at', limit=page_size,)
        for track in all_tracks:
            return track.title
        all_tracks = client.get('/tracks', order='created_at', limit=page_size, linked_partitioning=1)
        return super(AllMusicListView,self).get(request,*args,**kwargs)
        
    def get_context_data(self,**kwargs):
        context=super(AllMusicListView,self).get_context_data(**kwargs)
        context['request_user'] = request.user
        context['all_tracks'] = all_tracks
        return context


class AllSearchMusicView(View):
    template_name="search_music.html"
    def get(self,request,*args,**kwargs):
        client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
        if request.method == 'GET':
            q = request.GET.get('music_search')
            s_tracks = client.get('/tracks', q=q, license='cc-by-sa')
            response = render(request,'all_music.html',{'tracks_list':s_tracks,'q':q})
            return response
        return super(AllSearchMusicView,self).get(request,*args,**kwargs)
