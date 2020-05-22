from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoAlbum
from django.http import HttpResponse
from django.views import View
from video.forms import AlbumForm


class UserVideoListCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = AlbumForm()
        return context

    def post(self,request,*args,**kwargs):
        from posts.forms import PostForm

        form_post = AlbumForm(request.POST)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user == user:
            new_album = form_post.save(commit=False)
            new_album.creator = request.user
            new_album.save()
            return HttpResponse("")
