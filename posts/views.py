from django.views.generic.base import TemplateView


class PostsView(TemplateView):
    template_name="posts.html"

class PostCreate(TemplateView):
    template_name="post_add.html"
    form=None

    def get(self,request,*args,**kwargs):
        self.form=BlogForm(initial={"creator":request.user})
        return super(PostCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCreate,self).get_context_data(**kwargs)
        context["form"]=self.form
        return context

    def post(self,request,*args,**kwargs):
        self.form=BlogForm(request.POST,request.FILES)
        if self.form.is_valid():
            new_post=self.form.save(commit=False)
            new_post.creator=self.request.user
            new_post=self.form.save()

            if request.is_ajax() :
                return HttpResponse ('!')
        return super(PostCreate,self).post(request,*args,**kwargs)
