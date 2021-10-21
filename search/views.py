from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db.models import Q
from common.templates import get_default_template


class SearchView(ListView):
    template_name, section, paginate_by, users, communities, goods, musics, videos, \
    users_count, communities_count, goods_count, musics_count, videos_count, posts_count = None, "", 20, None, None, None, None, None, None, None, None, None, None, None

    def get(self,request,*args,**kwargs):
        from users.models import User
        from goods.models import Good
        from music.models import Music
        from video.models import Video
        from communities.models import Community
        from posts.models import Post

        if request.GET.get('q'):
            _q = request.GET.get('q').replace("#", "%23")
            if "?stat" in _q:
                self.q = _q[:_q.find("?") - 1:]
            else:
                self.q = _q
        else:
            self.q = ""
        self.sections = request.GET.get('s')

        if self.sections == "all" or not self.sections:
            _users = User.objects.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))
            _communities = Community.objects.filter(Q(name__icontains=self.q)|Q(description__icontains=self.q))
            _goods = Good.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            _musics = Music.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            _videos = Video.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            self.list = Post.objects.filter(text__icontains=self.q)
            if _users:
                self.users_count = _users.count()
                self.users = _users[:4]
            if _communities:
                self.communities_count = _communities.count()
                self.communities = _communities[:4]
            if _goods:
                self.goods_count = _goods.count()
                self.goods = _goods[:2]
            if _musics:
                self.musics_count = _musics.count()
                self.musics = _musics[:6]
            if _videos:
                self.videos_count = _videos.count()
                self.videos = _videos[:2]
            if self.list:
                self.posts_count = self.list.count()
            self.section = "all"
        elif self.sections == "people":
            self.list = User.objects.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))
            if self.list:
                self.users_count = self.list.count()
            self.section = "people"
        elif self.sections == "news":
            self.list = Post.objects.filter(text__icontains=self.q)
            if self.list:
                self.posts_count = self.list.count()
            self.section = "news"
        elif self.sections == "communities":
            self.list = Community.objects.filter(Q(name__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                self.communities_count = self.list.count()
            self.section = "communities"
        elif self.sections == "music":
            self.list = Music.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                self.musics_count = self.list.count()
            self.section = "music"
        elif self.sections == "video":
            self.list = Video.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                self.videos_count = self.list.count()
            self.section = "video"
        elif self.sections == "goods":
            self.list = Good.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
            if self.list:
                self.goods_count = self.list.count()
            self.section = "goods"
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
        context["posts_count"] = self.posts_count
        context["section"] = self.section
        return context

    def get_queryset(self):
        return self.list
