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


class LoadMusiclist(ListView):
	template_name, c, paginate_by, is_user_can_see_music_section, is_user_can_see_music_list, is_user_can_create_tracks = None, None, 10, None, None, None

	def get(self,request,*args,**kwargs):
		self.list = Musiclist.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.c = self.list.community
			if request.user.is_authenticated:
				if request.user.is_staff_of_community(self.c.pk):
					self.get_lists = Musiclist.get_community_staff_lists(self.c.pk)
					self.is_user_can_see_music_section = True
					self.is_user_can_create_tracks = True
					self.is_user_can_see_music_list = True
					self.template_name = get_template_community_list(self.list, "music/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				else:
					self.get_lists = Musiclist.get_community_lists(self.c.pk)
					self.is_user_can_see_music_section = self.c.is_user_can_see_music(request.user.pk)
					self.is_user_can_see_music_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_tracks = self.list.is_user_can_create_el(request.user.pk)
			elif request.user.is_anonymous:
				self.template_name = get_template_anon_community_list(self.list, "music/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_music_section = self.c.is_anon_user_can_see_music()
				self.is_user_can_see_music_list = self.list.is_anon_user_can_see_el()
				self.get_lists = Musiclist.get_community_lists(self.c.pk)
		else:
			if request.user.is_authenticated:
				if request.user.pk == self.list.creator.pk:
					user = self.list.creator
					self.is_user_can_see_music_section = True
					self.is_user_can_see_music_list = True
					self.is_user_can_create_tracks = True
				else:
					self.is_user_can_see_music_section = user.is_user_can_see_music(request.user.pk)
					self.is_user_can_see_music_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_tracks = self.list.is_user_can_create_el(request.user.pk)
				self.template_name = get_template_user_list(self.list, "music/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "music/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_music_section = self.user.is_anon_user_can_see_music()
				self.is_user_can_see_dmusic_list = self.list.is_anon_user_can_see_el()
		return super(LoadMusiclist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadMusiclist,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.c
		context['is_user_can_see_music_section'] = self.is_user_can_see_music_section
		context['is_user_can_see_music_list'] = self.is_user_can_see_music_list
		context['is_user_can_create_tracks'] = self.is_user_can_create_tracks
		return context

	def get_queryset(self):
		return self.list.get_items()
