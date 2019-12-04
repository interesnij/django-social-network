from django.views.generic.base import TemplateView
from users.models import User
from django.template.loader import render_to_string
from posts.models import Post
from communities.models import Community
from main.models import Item
from posts.forms import PostForm, PostCommunityForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from django.utils import timezone
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from common.checkers import check_can_get_posts_for_community_with_name
from generic.mixins import FormMixin
from gallery.models import Photo


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
        self.form_post=PostForm()
        self.user=User.objects.get(pk=self.kwargs["pk"])
        return super(PostUserCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostUserCreate,self).get_context_data(**kwargs)
        context["form_post"]=self.form_post
        return context

    def post(self,request,*args,**kwargs):
        self.form_post=PostForm(request.POST, request.FILES)
        self.user=User.objects.get(pk=self.kwargs["pk"])

        if self.form_post.is_valid():
            post=self.form_post.save(commit=False)
            post.creator=self.user
            new_post = post.create_post(
                                    creator=post.creator,
                                    text=post.text,
                                    community=None,
                                    comments_enabled=post.comments_enabled,
                                    status=post.status,
                                )

            if request.is_ajax() :
                html = render_to_string('new_post.html',{
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
        self.form_post=PostCommunityForm()
        return super(PostCommunityCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCreate,self).get_context_data(**kwargs)
        context["form_post"]=self.form_post
        return context

    def post(self,request,*args,**kwargs):
        self.form_post=PostCommunityForm(request.POST, request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.form_post.is_valid():
            new_post=self.form_post.save(commit=False)
            new_post.creator=self.request.user
            new_post.community=self.community
            new_post=self.form_post.save()

            if request.is_ajax() :
                html = render_to_string('new_post.html',{'object': new_post,'request': request})
                return HttpResponse(html)
        else:
            return HttpResponseBadRequest()


class RepostUserUser(View, FormMixin):

    def post(self, request, *args, **kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.user = self.item.creator
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)

            self.text=request.POST.get('text')
            self.creator=self.request.user
            self.comm_enabled=request.POST.get('comments_enabled')
            if self.comm_enabled == 'on':
                self.comments_enabled = True
            self.status=request.POST.get('status')
            if self.item.parent:
                self.parent=self.item.parent
            else:
                self.parent=self.item
            self.is_repost=True
            new_post=Post.objects.create(
                                        creator=self.creator,
                                        text=self.text,
                                        comments_enabled=self.comments_enabled,
                                        status = self.status,
                                        parent = self.parent
                                        )
            if request.is_ajax() :
                return HttpResponse("!")


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
