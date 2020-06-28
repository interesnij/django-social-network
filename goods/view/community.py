from django.views.generic import TemplateView
from goods.models import Good, GoodSubCategory, GoodCategory
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from goods.forms import GoodForm
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from common.checkers import check_can_get_posts_for_community_with_name
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response
from communities.models import Community


class CommunityGoods(TemplateView):
    template_name = "good_community/goods.html"

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        return super(CommunityGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommunityGoods,self).get_context_data(**kwargs)
        context["community"]=self.community
        return context


class CommunityGoodsList(View):
	def get(self,request,**kwargs):
		context = {}
		self.community=Community.objects.get(pk=self.kwargs["pk"])
		check_can_get_posts_for_community_with_name(request.user,self.community.name)
		goods = self.community.get_goods().order_by('-created')
		current_page = Paginator(goods, 10)
		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['goods_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['goods_list'] = current_page.page(1)
		except EmptyPage:
			context['goods_list'] = current_page.page(current_page.num_pages)
		return render_to_response('good_community/goods_list.html', context)


class CommunityUserCreate(TemplateView):
	template_name="good_community/add.html"
	form=None
	sub_categories = GoodSubCategory.objects.only("id")
	categories = GoodCategory.objects.only("id")
	success_url="/"

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.form=GoodForm(initial={"creator":self.user})
		return super(CommunityUserCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityUserCreate,self).get_context_data(**kwargs)
		context["form"]=self.form
		context["sub_categories"]=self.sub_categories
		context["categories"]=self.categories
		context["user"]=self.user
		return context

	def post(self,request,*args,**kwargs):
		self.form=GoodForm(request.POST,request.FILES)
		self.user=User.objects.get(pk=self.kwargs["pk"])
		if self.form.is_valid():
			new_good=self.form.save(commit=False)
			new_good.creator=self.user
			new_good=self.form.save()
			if request.is_ajax() :
				html = render_to_string('good_community/good.html',{'object': new_good,'request': request})
			return HttpResponse(html)
		else:
			return HttpResponseBadRequest()
		return super(CommunityUserCreate,self).get(request,*args,**kwargs)


class CommunityGood(TemplateView):
	template_name="good_community/good.html"

	def get(self,request,*args,**kwargs):
		self.community=Community.objects.get(uuid=self.kwargs["uuid"])
		check_can_get_posts_for_community_with_name(request.user,self.community.name)
		self.goods = self.community.get_goods()
		self.good = Good.objects.get(pk=self.kwargs["pk"])
		self.next = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
		self.prev = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
		self.good.views += 1
		self.good.save()
		return super(CommunityGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunityGood,self).get_context_data(**kwargs)
		context["object"]=self.good
		context["user"]=self.user
		context["next"]=self.next
		context["prev"]=self.prev
		return context
