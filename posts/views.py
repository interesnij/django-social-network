from django.views.generic.base import TemplateView
from users.models import User
from django.shortcuts import render_to_response, render
from posts.models import Post
from main.models import Item
from django.http import HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


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

    def get_context_data(self,**kwargs):
        context=super(PostUserCreate,self).get_context_data(**kwargs)
        context["form_post"]=PostForm()
        return context

    def post(self,request,*args,**kwargs):
        from posts.forms import PostForm

        self.form_post=PostForm(request.POST, request.FILES)
        self.user=User.objects.get(pk=self.kwargs["pk"])

        if self.form_post.is_valid() and request.user == self.user:
            post=self.form_post.save(commit=False)
            if request.POST.get('text') or request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                #from common.post_attacher import get_post_attach

                new_post = post.create_post(creator=request.user, text=post.text, community=None, comments_enabled=post.comments_enabled, status=post.status,)
                #get_post_attach(request, new_post)
                return render_to_response('item_user/my_post.html', {'object': new_post,'request': request})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommunityCreate(View):

    def get_context_data(self,**kwargs):
        context=super(PostCommunityCreate,self).get_context_data(**kwargs)
        context["form_post"]=PostCommunityForm()
        return context

    def post(self,request,*args,**kwargs):
        from communities.models import Community
        from posts.forms import PostCommunityForm

        form_post=PostCommunityForm(request.POST, request.FILES)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            post=form_post.save(commit=False)
            new_post = post.create_post(creator=request.user, text=post.text, community=community, comments_enabled=post.comments_enabled, status=post.status,)
            return render_to_response('item_community/admin_post.html',{'object': new_post,'community': community,'request': request})
        else:
            return HttpResponseBadRequest()


class RepostUserUser(View):

    def post(self, request, *args, **kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.user = self.item.creator
        if self.user != request.user:
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
            new_post=Post.objects.create(creator=self.creator, text=self.text, comments_enabled=self.comments_enabled, status = self.status, parent = self.parent, is_repost=True, )
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
        from communities.models import Community

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
        from communities.models import Community

        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.item.parent:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item.parent, is_repost=True)
            return HttpResponse("репост репоста")
        else:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item, is_repost=True)
            return HttpResponse("репост item")
