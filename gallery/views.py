from django.views.generic.base import TemplateView


class GuestbookView(TemplateView):
	template_name="gallery.html"

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		return super(GuestbookView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GuestbookView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context
