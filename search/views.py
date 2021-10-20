from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db.models import Q


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

        self.q = request.GET.get('q')
        self.users = User.objects.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))
        self.communities = Community.objects.filter(Q(name__icontains=self.q)|Q(description__icontains=self.q))
        self.goods = Good.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
        self.musics = Music.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
        self.videos = Video.objects.filter(Q(title__icontains=self.q)|Q(description__icontains=self.q))
        return super(SearchView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(SearchView,self).get_context_data(**kwargs)
        context["q"] = self.q
        return context

    def get_queryset(self):
        if self.q:
            from posts.models import Post
            query = Q(text__icontains=self.q)
            return Post.objects.filter(query)
