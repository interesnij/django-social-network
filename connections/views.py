from django.views.generic.base import TemplateView
from posts.helpers import ajax_required, AuthorRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from users.models import User
from connections.models import Connection


class ConnectionsView(TemplateView):
    template_name="connections.html"


class ConnectionCreate(TemplateView):
    template_name = "connection_add.html"
    success_url = "/"

    def get(self,request,*args,**kwargs):
        self.user=request.user
        self.target_user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.connection = Connection.objects.get(target_user=self.target_user,user=self.user)
        except:
            self.connection = None

        if not self.connection and self.target_user != self.user:
            Connection.objects.create(target_user=self.target_user, user=self.user)
        else:
            return HttpResponse("Пользователь уже с Вами дружит :-)")
        return super(PostUserLiteCreate,self).get(request,*args,**kwargs)
