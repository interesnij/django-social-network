from django.views.generic.base import TemplateView


class LogsView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.template_name = "logs.html"
        return super(LogsView,self).get(request,*args,**kwargs)
