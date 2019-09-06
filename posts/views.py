from django.views.generic.base import TemplateView
from posts.forms import PostHardForm, PostLiteForm, PostMediumForm
from django.http import HttpResponse
from users.models import User


class PostsView(TemplateView):
    template_name="posts.html"


class PostUserHardCreate(TemplateView):
    template_name="post_hard_add.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form=PostHardForm(initial={"creator":request.user})
        return super(PostUserHardCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserHardCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostHardForm(request.POST)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                return HttpResponse ('!')
        else:
            self.form=PostHardForm()
        return super(PostUserHardCreate,self).get(request,*args,**kwargs)

class PostUserMediumCreate(TemplateView):
    template_name="post_medium_add.html"
    form=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form=PostMediumForm(initial={"creator":self.request.user})
        return super(PostUserMediumCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserMediumCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostMediumForm(request.POST)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                return HttpResponse ('!')
        else:
            self.form=PostMediumForm()
        return super(PostUserMediumCreate,self).post(request,*args,**kwargs)

class PostUserLiteCreate(TemplateView):
    template_name="post_lite_add.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form=PostLiteForm(initial={"creator":request.user})
        return super(PostUserLiteCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserLiteCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=PostLiteForm(request.POST,request.FILES)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                return HttpResponse ('!')
        else:
            self.form=PostLiteForm()
        return super(PostUserLiteCreate,self).get(request,*args,**kwargs)
