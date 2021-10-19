from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.db.models import Q


class SearchView(ListView):
    template_name, paginate_by = None, 20

    def get(self,request,*args,**kwargs):
        self.q = request.GET.get('q')
        if request.user.is_authenticated:
            self.template_name = "search/search.html"
        else:
            self.template_name = "search/anon_search.html"
        return super(SearchView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(SearchView,self).get_context_data(**kwargs)
        context["q"] = self.q
        return context

    def get_queryset(self):
        if self.q:
            query = Q(title__icontains=self._all)|Q(description__icontains=self._all)
            return query
