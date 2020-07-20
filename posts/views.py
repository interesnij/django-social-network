from django.views.generic.base import TemplateView
from users.models import User
from django.shortcuts import render
from posts.models import Post
from django.http import HttpResponseBadRequest
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id


class PostsView(TemplateView):
    template_name = "posts.html"


class PostDetailView(TemplateView):
    model = Post
    template_name = "post.html"

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        self.post.views += 1
        self.post.save()
        return super(PostDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

class RepostUserUser(View):

    def post(self, request, *args, **kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.user = self.item.creator
        if self.user != request.user:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile:
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)

            self.text = request.POST.get('text')
            self.creator = self.request.user
            self.comm_enabled = request.POST.get('comments_enabled')
            if self.comm_enabled == 'on':
                self.comments_enabled = True
            self.status = request.POST.get('status')
            if self.item.parent:
                self.parent = self.item.parent
            else:
                self.parent = self.item
            new_post = Post.objects.create(creator=self.creator, text=self.text, comments_enabled=self.comments_enabled, status = self.status, parent = self.parent, )
            if request.is_ajax() :
                return HttpResponse("!")


class RepostCommunityUser(View):

	def post(self, request, *args, **kwargs):
		self.item = Post.objects.get(pk=self.kwargs["pk"])
		if self.item.parent:
			new_repost = Post.objects.create(creator=request.user, community=self.item.community, parent=self.item.parent)
			return HttpResponse("репост репоста")
		else:
			new_repost = Post.objects.create(creator=request.user, community=self.item.community, parent=self.item)
			return HttpResponse("репост item")


class RepostCommunityCommunity(View):
    def post(self, request, *args, **kwargs):
        from communities.models import Community

        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.item.parent:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item.parent)
        else:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item)
            return HttpResponse("репост item")


class RepostUserCommunity(View):
    def post(self, request, *args, **kwargs):
        from communities.models import Community

        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if self.item.parent:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item.parent)
            return HttpResponse("репост репоста")
        else:
            new_repost = Post.objects.create(creator=request.user, community=self.community, parent=self.item)
            return HttpResponse("репост item")
