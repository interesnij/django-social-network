from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db.models import Q
from common.templates import get_default_template


class SearchView(ListView):
    template_name, paginate_by, users, communities, goods, musics, videos = None, 20, None, None, None, None, None

    def get(self,request,*args,**kwargs):
        from users.models import User
        from goods.models import Good
        from music.models import Music
        from video.models import Video
        from communities.models import Community

        if request.user.is_authenticated:
            self.template_name = "search/search.html"
        else:
            self.template_name = "search/anon_search.html"

        self.q = request.GET.get('q').replace("#", "%23")
        self.users = User.objects.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))[:4]
        self.communities = Community.objects.filter(Q(name__icontains=self.q)|Q(description__icontains=self.q))[:4]
        self.goods = Good.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))[:3]
        self.musics = Music.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))[:6]
        self.videos = Video.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))[:2]

        self.template_name = get_default_template("search/", "search.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SearchView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(SearchView,self).get_context_data(**kwargs)
        context["q"] = self.q
        context["users"] = self.users
        context["communities"] = self.communities
        context["goods"] = self.goods
        context["musics"] = self.musics
        context["videos"] = self.videos
        return context

    def get_queryset(self):
        if self.q:
            from posts.models import Post
            query = Q(text__icontains=self.q)
            return Post.objects.filter(query)
