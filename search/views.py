from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db.models import Q
from common.templates import get_default_template


class SearchView(ListView):
    template_name, paginate_by, users, communities, goods, musics, videos, \
    users_count, communities_count, goods_count, musics_count, videos_count, posts_count = None, 20, None, None, None, None, None, None, None, None, None, None, None

    def get(self,request,*args,**kwargs):
        from users.models import User
        from goods.models import Good
        from music.models import Music
        from video.models import Video
        from communities.models import Community
        from posts.models import Post

        self.q = request.GET.get('q').replace("#", "%23")
        self.sections = request.GET.get('s')

        if self.sections == "all" or not self.sections:
            _users = User.objects.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))
            _communities = Community.objects.filter(Q(name__icontains=self.q)|Q(description__icontains=self.q))
            _goods = Good.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            _musics = Music.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            _videos = Video.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            self.list = Post.objects.filter(text__icontains=self.q)
            if _users:
                users_count = _users.count()
                self.users = _users[:4]
            if _communities:
                communities_count = _communities.count()
                self.communities = _communities[:4]
            if self._goods:
                goods_count = _goods.count()
                self.goods = _goods[:4]
            if self._musics:
                musics_count = _musics.count()
                self.musics = _musics[:4]
            if self._videos:
                videos_count = _videos.count()
                self.videos = _videos[:4]
            if self.list:
                posts_count = self.list.count()
        elif self.sections == "people":
            self.list = User.objects.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))
            if self.list:
                users_count = self.list.count()
        elif self.sections == "news":
            self.list = Post.objects.filter(text__icontains=self.q)
            if self.list:
                posts_count = self.list.count()
        elif self.sections == "communities":
            self.list = Community.objects.filter(Q(name__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                communities_count = self.list.count()
        elif self.sections == "music":
            self.list = Music.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                musics_count = self.list.count()
        elif self.sections == "video":
            self.list = Video.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                videos_count = self.list.count()
        elif self.sections == "goods":
            self.list = Good.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                goods_count = self.list.count()
        self.template_name = get_default_template("search/", "search.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SearchView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(SearchView,self).get_context_data(**kwargs)
        context["q"] = self.q.replace("%23","#")
        context["users"] = self.users
        context["communities"] = self.communities
        context["goods"] = self.goods
        context["musics"] = self.musics
        context["videos"] = self.videos
        context["users_count"] = self.users_count
        context["communities_count"] = self.communities_count
        context["goods_count"] = self.goods_count
        context["musics_count"] = self.musics_count
        context["videos_count"] = self.videos_count
        return context

    def get_queryset(self):
        return self.list
