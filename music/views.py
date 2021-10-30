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
        self.rus_simbols, self.angl_simbols, self.number_simbols, self.all_music_count, self.rus_tegs_count, self.angl_tegs_count, self.genres, self.template_name = SoundSymbol.objects.filter(type='RS'), SoundSymbol.objects.filter(type='AS'), SoundSymbol.objects.filter(type='NS'), \
        Music.objects.only('pk').count(), SoundTags.objects.filter(symbol__type='RS').values('pk').count(), SoundTags.objects.filter(symbol__type='AS').values('pk').count(), SoundTags.objects.filter(symbol__type='NS').values('pk').count(), \
        SoundGenres.objects.only('id'), get_detect_platform_template("music/all_music.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllMusicView,self).get_context_data(**kwargs)
        context["rus_simbols"] = self.rus_simbols
        context["angl_simbols"] = self.angl_simbols
        context["number_simbols"] = self.number_simbols
        context["all_music_count"] = self.all_music_count
        context["rus_tegs_count"] = self.rus_tegs_count
        context["angl_tegs_count"] = self.angl_tegs_count
        context["number_tegs_count"] = self.number_tegs_count
        context["genres"] = self.genres
        return context


class AllTagsMusicView(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.symbol, self.tags, self.template_name = SoundSymbol.objects.get(pk=self.kwargs["pk"]), SoundTags.objects.filter(symbol=self.symbol), get_detect_platform_template("music/tags_music.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AllTagsMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllTagsMusicView,self).get_context_data(**kwargs)
        context["symbol"] = self.symbol
        context["tags"] = self.tags
        return context

    def get_queryset(self):
        tags_list = SoundTags.objects.filter(symbol=self.symbol)
        return tags_list


class AllTagMusicView(ListView):
    template_name, paginate_by = None, 15

    def get(self,request,*args,**kwargs):
        self.tag, self.template_name = SoundTags.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("music/tag_music.html", request.user, request.META['HTTP_USER_AGENT'])
        if request.user.is_authenticated:
            self.is_tag_playlist = request.user.is_tag_playlist(self.tag)
        return super(AllTagMusicView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AllTagMusicView,self).get_context_data(**kwargs)
        context["tag"] = self.tag
        context["is_tag_playlist"] = self.is_tag_playlist
        return context

    def get_queryset(self):
        tag_list = Music.objects.filter(tag__id=self.tag.pk)
        return tag_list


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
