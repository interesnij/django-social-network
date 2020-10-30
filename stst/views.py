from django.views.generic.base import TemplateView
from common.utils import get_client_ip, get_location
from users.models import User
from common.template.user import get_detect_platform_template 
from posts.models import Post


class StatItemView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("stst/item_stat.html", request.META['HTTP_USER_AGENT'])
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        return super(StatItemView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(StatItemView,self).get_context_data(**kwargs)
        context["item"] = self.item
        return context
