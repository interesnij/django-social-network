from posts.models import PostList, Post
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from common.templates import get_template_community_item, get_template_anon_community_item, get_template_user_item, get_template_anon_user_item


class PostsView(ListView):
	template_name = "posts.html"

	def get_queryset(self):
		return Post.objects.only("pk")


class LoadPostList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = PostList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_administrator_of_community(self.community.pk):
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.list, "posts/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.list, "posts/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.pk == self.list.creator.pk:
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.list, "posts/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.list, "posts/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadPostList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPostList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.posts


class LoadPost(TemplateView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.post = Post.objects.get(uuid=self.kwargs["uuid"])
		self.list = self.post.list

		if self.list.community:
			if request.user.is_administrator_of_community(self.list.pk):
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()
		else:
			if request.user.pk == self.list.creator.pk:
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()

		if self.post.community:
			self.community = self.post.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.post, "communities/lenta/", "post.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.post, "communities/lenta/anon_post.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.post, "users/lenta/", "post.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.post, "users/lenta/anon_post.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadPost,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPost,self).get_context_data(**kwargs)
		context["object"] = self.object
		context["community"] = self.community
		return context


class LoadFixPost(TemplateView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.post = Post.objects.get(uuid=self.kwargs["uuid"])
		self.list = self.post.list

		if self.list.community:
			if request.user.is_administrator_of_community(self.list.pk):
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()
		else:
			if request.user.pk == self.list.creator.pk:
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()

		if self.post.community:
			self.community = self.post.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.post, "communities/lenta/", "fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.post, "communities/lenta/anon_fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.post, "users/lenta/", "fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.post, "users/lenta/anon_fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadFixPost,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(LoadFixPost,self).get_context_data(**kwargs)
		c["object"] = self.object
		c["community"] = self.community
		c["next"] = self.posts.filter(pk__gt=self.post.pk).order_by('pk').first()
		c["prev"] = self.posts.filter(pk__lt=self.post.pk).order_by('pk').first()
		return c
