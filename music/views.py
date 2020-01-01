import soundcloud
from django.views.generic.base import TemplateView
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse


class AllMusicView(TemplateView):
    template_name="all_music.html"


class AllMusicListView(View):
    template_name="all_music_list.html"
    client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
    def get(self,request,*args,**kwargs):
        all_tracks = client.get('/tracks', genres='punk')
        html = render_to_string('all_music_list.html',{'all_tracks': all_tracks, 'request_user': request.user, 'request': request})
        return JsonResponse(html, safe=False)


class AllSearchMusicView(View):
    template_name="search_music.html"
    client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
    def get(self,request,*args,**kwargs):
        if request.method == 'GET':
            q = request.GET.get('music_search')
            s_tracks = client.get('/tracks', q=q, license='cc-by-sa')
            response = render(request,'all_music.html',{'tracks_list':s_tracks,'q':q})
            return response
        return super(AllSearchMusicView,self).get(request,*args,**kwargs)
