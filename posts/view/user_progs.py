from users.models import User
from django.shortcuts import render
from posts.models import Post
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from posts.forms import PostForm
from common.post_attacher import get_post_attach
from common.processing.post import get_post_processing
from common.check.user import check_user_can_get_list, check_anon_user_can_get_list
from django.http import Http404


class PostUserCreate(View):
    def post(self,request,*args,**kwargs):
        self.form_post = PostForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid():
            post = self.form_post.save(commit=False)

            if request.POST.get('text') or request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=None, comments_enabled=post.comments_enabled, status="PG")
                get_post_attach(request, new_post)
                get_post_processing(new_post)
                return render(request, 'post_user/my_post.html', {'object': new_post})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class UserPostView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import PostNumbers

        if request.is_ajax() and request.user.is_authenticated:
            post = Post.objects.get(uuid=self.kwargs["uuid"])
            if PostNumbers.objects.filter(user=request.user.pk, post=post.pk).exists():
                return HttpResponse('')
            else:
                PostNumbers.objects.create(user=request.user.pk, post=post.pk)
                return HttpResponse('')
        else:
            return HttpResponse('')

class UserAdPostView(View):
    def get(self,request,*args,**kwargs):
        from stst.models import PostAdNumbers

        if request.is_ajax() and request.user.is_authenticated:
            post = Post.objects.get(uuid=self.kwargs["uuid"])
            if PostNumbers.objects.filter(user=request.user.pk, post=post.pk).exists():
                return HttpResponse()
            else:
                PostAdNumbers.objects.get(user=request.user.pk, post=post.pk)
                return HttpResponse()
        else:
            raise Http404
