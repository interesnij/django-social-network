from django.views.generic.base import TemplateView
from posts.forms import PostForm
from django.http import HttpResponse


class PostsView(TemplateView):
    template_name="posts.html"


class PostUserCreate(TemplateView):
    template_name="post_add.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form=PostForm(initial={"creator":request.user})
        return super(PostUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostForm(request.POST)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            return super(PostUserCreate,self).post(request,*args,**kwargs)
        else:
            self.form=PostForm()
        return super(PostUserCreate,self).post(request,*args,**kwargs)
