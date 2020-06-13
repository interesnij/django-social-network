from django.views.generic.base import TemplateView
from common.utils import get_client_ip, get_location
from users.models import User


class StatView(TemplateView):
    template_name="stat.html"

    def get(self,request,*args,**kwargs):
        self.ip = get_client_ip(request)
        get_location(request)
        return super(StatView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(StatView,self).get_context_data(**kwargs)
        context["ip"]=self.ip
        return context

class StatItemView(TemplateView):
    template_name="item_stat.html"

    def get(self,request,*args,**kwargs):
        from posts.models import Post

        self.item=Post.objects.get(uuid=self.kwargs["uuid"])
        return super(StatItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(StatItemView,self).get_context_data(**kwargs)
        context["item"]=self.item
        return context
