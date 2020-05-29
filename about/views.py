from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = "about.html"
		else:
			self.template_name = "anon_about.html"
		return super(AboutView,self).get(request,*args,**kwargs)
