from django.views.generic.base import TemplateView
from django.views.generic import ListView
from main.models import Item


class MainPageView(TemplateView):
	template_name=None

	def get(self,request,*args,**kwargs):
		from common.utils import is_mobile

		if request.user.is_authenticated:
			if is_mobile(request):
				self.template_name="main/mob_news.html"
			else:
				self.template_name="main/news.html"
		else:
			if is_mobile(request):
				self.template_name="main/mob_auth.html"
			else:
				self.template_name="main/auth.html"
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)
		return context


class NewsListView(ListView):
	from main.models import Item

	template_name="news_list.html"
	model=Item
	paginate_by=30

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = self.request.user.get_timeline_posts().order_by('-created')
		else:
			items=None
		return items


class ComingView(TemplateView):
	template_name="base_coming.html"


class MainPhoneSend(TemplateView):
	template_name="phone_verification.html"

	def get(self,request,*args,**kwargs):
		import json, requests
		from django.http import HttpResponse, HttpResponseBadRequest
		from common.model.other import PhoneCodes

		self.phone = request.POST.get('phone').replace("+","")
		self.response = self.requests.get(url= "https://api.ucaller.ru/v1.0/initCall?service_id=12203&key=GhfrKn0XKAmA1oVnyEzOnMI5uBnFN4ck&phone=" + self.phone)
		self.data = self.response.json()
		if self.data['status'] == 'true' and self.data['phone'] == self.phone:
			PhoneCodes.objects.create(phone=self.data['phone'], code=self.data['code'])
			return HttpResponse("")
		else:
			return HttpResponseBadRequest()
