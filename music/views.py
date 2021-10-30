from django.views.generic.base import TemplateView
from music.models import *
from django.views.generic import ListView
from common.templates import (
								get_detect_platform_template,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class AllMusicView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.genres, self.template_name = SoundGenres.objects.only('id'), get_detect_platform_template("music/all_music.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllMusicView,self).get_context_data(**kwargs)
        context["genres"] = self.genres
        return context


class GenreMusicView(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.genre, self.template_name = SoundGenres.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("music/genre_music.html", request.user, request.META['HTTP_USER_AGENT'])
        if request.user.is_authenticated:
            self.is_genre_playlist = request.user.is_genre_playlist(self.genre)
        return super(GenreMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GenreMusicView,self).get_context_data(**kwargs)
        context["genre"] = self.genre
        context["is_genre_playlist"] = self.is_genre_playlist
        return context

    def get_queryset(self):
        genre_list = Music.objects.filter(genre__id=self.genre.pk)
        return genre_list


class LoadPlaylist(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = MusicList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_list(self.list, "music/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_list(self.list, "music/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_list(self.list, "music/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_list(self.list, "music/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadPlaylist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPlaylist,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()
