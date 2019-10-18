from django.views.generic.base import TemplateView
from users.models import User
from django.template.loader import render_to_string
from posts.models import Post, PostImage
from posts.forms import PostUserForm
from django.http import HttpResponse
from django.forms.models import inlineformset_factory



class PostsView(TemplateView):
    template_name="posts.html"


class PostDetailView(TemplateView):
    model=Post
    template_name="post.html"

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.post.views += 1
        self.post.save()
        return super(PostDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostDetailView,self).get_context_data(**kwargs)
        context["object"]=self.post
        return context


PostImagesFormset=inlineformset_factory(Post,PostImage,can_order=True, fields='__all__')

class PostUserCreate(TemplateView):
    template_name="article_add.html"
    form_post=None
    success_url="/"
    formset_post=None

    def get(self,request,*args,**kwargs):
        self.form_post=PostUserForm(initial={"creator":request.user})
        self.formset_post=PostImagesFormset()
        return super(PostUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCreate,self).get_context_data(**kwargs)
        context["form_post"]=self.form_post
        context["formset_post"]=self.formset_post
        return context

    def post(self,request,*args,**kwargs):
        self.form_post=PostUserForm(request.POST, request.FILES)
        self.formset_post=PostImagesFormset(request.POST,request.FILES)
        if self.form_post.is_valid():
            new_post=self.form_post.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form_post.save()
            if self.formset_post.is_valid():
                self.formset_post.save()

            if request.is_ajax() :
                 html = render_to_string('new_post.html',{'object': new_post,'request': request})
                 return HttpResponse(html)
        return super(PostUserCreate,self).get(request,*args,**kwargs)
