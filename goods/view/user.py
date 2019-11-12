from django.views.generic import TemplateView
from goods.models import Good, GoodSubCategory, GoodCategory
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from goods.forms import GoodForm
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from generic.mixins import EmojiListMixin
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response


class UserGoods(TemplateView):
    template_name = "user/goods.html"

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        return super(UserGoods,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(UserGoods,self).get_context_data(**kwargs)
        context["user"]=self.user
        return context


class UserGoodsList(View):
	def get(self,request,**kwargs):
		context = {}
		self.user=User.objects.get(pk=self.kwargs["pk"])
		if self.user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
		goods = self.user.get_goods().order_by('-created')
		current_page = Paginator(goods, 6)
		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['goods_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['goods_list'] = current_page.page(1)
		except EmptyPage:
			context['goods_list'] = current_page.page(current_page.num_pages)
		return render_to_response('user/goods_list.html', context)


class GoodUserCreate(TemplateView):
	template_name="user/add.html"
	form=None
	sub_categories = GoodSubCategory.objects.only("id")
	categories = GoodCategory.objects.only("id")
	success_url="/"

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.form=GoodForm(initial={"creator":self.user})
		return super(GoodUserCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GoodUserCreate,self).get_context_data(**kwargs)
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
				html = render_to_string('user/good.html',{'object': new_good,'request': request})
			return HttpResponse(html)
		else:
			return HttpResponseBadRequest()
		return super(GoodUserCreate,self).get(request,*args,**kwargs)


class UserGood(EmojiListMixin, TemplateView):
	template_name="user/good.html"

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		if self.user != request.user:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
		self.goods = self.user.get_goods()
		self.good = Good.objects.get(pk=self.kwargs["pk"])
		self.next = self.goods.filter(pk__gt=self.good.pk).order_by('pk').first()
		self.prev = self.goods.filter(pk__lt=self.good.pk).order_by('-pk').first()
		self.good.views += 1
		self.good.save()
		return super(UserGood,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(UserGood,self).get_context_data(**kwargs)
		context["object"]=self.good
		context["user"]=self.user
		context["next"]=self.next
		context["prev"]=self.prev
		return context
