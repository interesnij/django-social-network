from posts.models import PostsList, Post
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class PostsView(ListView):
	template_name = "posts.html"

	def get_queryset(self):
		return Post.objects.only("pk")


class LoadPostsList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = PostsList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				if request.user.is_administrator_of_community(self.community.pk):
					self.posts = self.list.get_staff_items()
				else:
					self.posts = self.list.get_items()
				self.template_name = get_template_community_list(self.list, "posts/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.posts = self.list.get_items()
				self.template_name = get_template_anon_community_list(self.list, "posts/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.pk == self.list.creator.pk:
				self.posts = self.list.get_staff_items()
			else:
				self.posts = self.list.get_items()
			if request.user.is_authenticated:
				self.template_name = get_template_user_list(self.list, "posts/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_list(self.list, "posts/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadPostsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPostsList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.posts


class LoadPost(TemplateView):
	template_name, community, user_wall, community_wall, featured_wall, feed_wall, search_wall, chat_wall = None, None, None, None, None, None, None, None

	def get(self,request,*args,**kwargs):
		self.post = Post.objects.get(uuid=self.kwargs["uuid"])
		self.list = self.post.list
		if request.GET.get("user_wall"):
			self.owner_wall = "пользователь"
		elif request.GET.get("community_wall"):
			self.owner_wall = "сообщество"
		elif request.GET.get("feed_wall"):
			self.owner_wall = "новости"
		elif request.GET.get("chat_wall"):
			self.owner_wall = "сообщения"
		elif request.GET.get("search_wall"):
			self.owner_wall = "поиск"
		elif request.GET.get("featured_wall"):
			self.owner_wall = "рекомендации"
		else:
			self.owner_wall = "прямой переход"

		if self.list.community:
			if request.user.is_authenticated:
				if request.user.is_administrator_of_community(self.list.pk):
					self.posts = self.list.get_staff_items()
				else:
					self.posts = self.list.get_items()
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
		c = super(LoadPost,self).get_context_data(**kwargs)
		c["object"] = self.post
		c["community"] = self.community
		if self.posts.filter(order=self.post.order + 1).exists():
			c["next"] = self.posts.filter(order=self.post.order + 1)[0]
		if self.posts.filter(order=self.post.order - 1).exists():
			c["prev"] = self.posts.filter(order=self.post.order - 1)[0]
		c["owner_wall"] = self.owner_wall
		return c


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
		c["object"] = self.post
		c["community"] = self.community
		if self.posts.filter(order=self.post.order + 1).exists():
			c["next"] = self.posts.filter(order=self.post.order + 1)[0]
		if self.posts.filter(order=self.post.order - 1).exists():
			c["prev"] = self.posts.filter(order=self.post.order - 1)[0]
		return c


class LoadPostsList(ListView):
	template_name, community, paginate_by = None, None, 10

	def get(self,request,*args,**kwargs):
		self.list = PostsList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_list(self.list, "posts/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_list(self.list, "posts/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_list(self.list, "posts/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_list(self.list, "posts/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadPostsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPostsList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()
