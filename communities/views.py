from django.views.generic import ListView
from users.models import User
from communities.models import Community
from django.views.generic.detail import DetailView



class CommunitiesView(ListView):
	template_name="communities.html"
	model=Community
	paginate_by=10

	def get_queryset(self):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		groups=Community.objects.filter(starrers=self.user)
		return groups

	def get_context_data(self,**kwargs):
		context=super(CommunitiesView,self).get_context_data(**kwargs)

		return context

class CommunityDetailView(DetailView):
	template_name="community_detail.html"
	model=Community


class AllCommunities(ListView):
	template_name="all_communities.html"
	model=Community
	paginate_by=10

	def get_queryset(self):
		groups=Community.objects.all()
		return groups


class CommunityCreate(TemplateView):
    template_name="community_add.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form=CommunityForm(initial={"creator":request.user})
        return super(CommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=CommunityForm(request.POST,request.FILES)
        if self.form.is_valid():
			Community.create_community(name=self.form.name, title=self.form.title, creator=request.user)

            if request.is_ajax() :
                 return HttpResponse("!")
        else:
           return JsonResponse({'error': True, 'errors': self.form.errors})
        return super(CommunityCreate,self).get(request,*args,**kwargs)
