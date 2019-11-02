from django.views.generic.base import TemplateView
from users.models import User
from django.template.loader import render_to_string
from posts.models import Post
from main.models import Item
from posts.forms import PostForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View


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


class PostUserCreate(View):
    form_post=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form_post=PostForm(initial={"creator":request.user})
        return super(PostUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCreate,self).get_context_data(**kwargs)
        context["form_post"]=self.form_post
        return context

    def post(self,request,*args,**kwargs):
        self.form_post=PostForm(request.POST, request.FILES)
        if self.form_post.is_valid():
            new_post=self.form_post.save(commit=False)
            new_post.creator=self.request.user
            new_post.create_post(creator=new_post.creator, text=new_post.text)

            if request.is_ajax() :
                html = render_to_string('generic/posts/test.html',{
                    'object': new_post,
                    'request': request
                    })
                return HttpResponse(html)
        else:
            return HttpResponseBadRequest()


class PostCommunityCreate(View):
    form_post=None
    success_url="/"

    def get(self,request,*args,**kwargs):
        self.form_post=PostForm(initial={"creator":request.user,'community':request.POST.get('community')})
        return super(PostCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCreate,self).get_context_data(**kwargs)
        context["form_post"]=self.form_post
        return context

    def post(self,request,*args,**kwargs):
        self.form_post=PostForm(request.POST, request.FILES)
        if self.form_post.is_valid():
            new_post=self.form_post.save(commit=False)
            new_post.creator=self.request.user
            new_post.community=request.POST.get('community')
            new_post=self.form_post.save()

            if request.is_ajax() :
                html = render_to_string('new_post.html',{'object': new_post,'request': request})
                return HttpResponse(html)
        else:
            return HttpResponseBadRequest()


class RepostUserUser(View):

    def post(self, request, *args, **kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.form_post=PostForm(request.POST, request.FILES)
        if self.form_post.is_valid():
            new_post=self.form_post.save(commit=False)
            new_post.creator=self.request.user
            new_post.parent=self.item.parent
            new_post.is_repost=True
            if self.item.community:
                new_post.community=self.item.community
            new_post=self.form_post.save()
        if request.is_ajax() :
            return HttpResponse("!")
        else:
            return HttpResponseBadRequest()


class RepostCommunityUser(View):

	def post(self, request, *args, **kwargs):
		self.item = Item.objects.get(pk=self.kwargs["pk"])
		if self.item.parent:
			new_repost = Post.objects.create(creator=request.user, community=self.item.community, parent=self.item.parent, is_repost=True)
			return HttpResponse("репост репоста")
		else:
			new_repost = Post.objects.create(creator=request.user, community=self.item.community, parent=self.item, is_repost=True)
			return HttpResponse("репост item")


class RepostCommunityCommunity(View):
    def post(self, request, *args, **kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.item.parent:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item.parent, is_repost=True)
            return HttpResponse("репост репоста")
        else:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item, is_repost=True)
            return HttpResponse("репост item")


class RepostUserCommunity(View):
    def post(self, request, *args, **kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.item.parent:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item.parent, is_repost=True)
            return HttpResponse("репост репоста")
        else:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item, is_repost=True)
            return HttpResponse("репост item")
