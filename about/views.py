from django.views.generic.base import TemplateView
from common.template.user import get_default_template


class AboutView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_default_template("about/", "about.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AboutView,self).get(request,*args,**kwargs)


class TermsView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_default_template("about/", "terms.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(TermsView,self).get(request,*args,**kwargs)


class PolicyView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_default_template("about/", "policy.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PolicyView,self).get(request,*args,**kwargs)


class LicenceView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_default_template("about/", "licence.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(LicenceView,self).get(request,*args,**kwargs)
