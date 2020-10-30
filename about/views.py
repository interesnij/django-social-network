from django.views.generic.base import TemplateView
from common.template.user import get_settings_template


class AboutView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("about/about.html", request)
        return super(AboutView,self).get(request,*args,**kwargs)


class TermsView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("about/terms.html", request)
        return super(TermsView,self).get(request,*args,**kwargs)


class PolicyView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("about/policy.html", request)
        return super(PolicyView,self).get(request,*args,**kwargs)


class LicenceView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("about/licence.html", request)
        return super(LicenceView,self).get(request,*args,**kwargs)
