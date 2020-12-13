from django.views.generic.base import TemplateView
from music.models import *
from django.views.generic import ListView
from common.template.user import get_detect_platform_template


class AllMusicView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.rus_simbols, self.angl_simbols, self.number_simbols, self.all_music_count, self.rus_tegs_count, self.angl_tegs_count, self.genres, self.template_name = SoundSymbol.objects.filter(type='RS'), SoundSymbol.objects.filter(type='AS'), SoundSymbol.objects.filter(type='NS'), \
        SoundcloudParsing.objects.only('pk').count(), SoundTags.objects.filter(symbol__type='RS').values('pk').count(), SoundTags.objects.filter(symbol__type='AS').values('pk').count(), SoundTags.objects.filter(symbol__type='NS').values('pk').count(), \
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
        tag_list = SoundcloudParsing.objects.filter(tag__id=self.tag.pk)
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
        genre_list = SoundcloudParsing.objects.filter(genre__id=self.genre.pk)
        return genre_list
