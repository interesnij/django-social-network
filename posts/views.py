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
		self.posts = self.list.get_items()
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_list(self.list, "posts/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.posts = self.list.get_items()
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
		return self.posts


class LoadPost(TemplateView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.post = Post.objects.get(pk=self.kwargs["pk"])
		self.list = self.post.list
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
		return c


class LoadFixPost(TemplateView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.post = Post.objects.get(pk=self.kwargs["pk"])

		if self.post.community:
			self.community = self.post.community
			self.posts = self.community.get_fixed_posts()
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.post, "communities/lenta/", "fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.post, "communities/lenta/anon_fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.posts = self.post.creator.get_fixed_posts()
			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.post, "users/lenta/", "fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.post, "users/lenta/anon_fix_post_detail.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadFixPost,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(LoadFixPost,self).get_context_data(**kwargs)
		c["object"] = self.post
		c["community"] = self.community
		c["next"] = self.posts.filter(pk__gt=self.post.pk).order_by('pk').first()
		c["prev"] = self.posts.filter(pk__lt=self.post.pk).order_by('-pk').first()
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


class PostListLoadIncludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		from posts.models import PostsList
		from common.templates import get_detect_platform_template

		self.list = PostsList.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_see_el":
			self.users = self.list.get_can_see_el_include_users()
			self.text = "видит записи"
		elif self.type == "can_see_comment":
			self.users = self.list.get_can_see_comment_include_users()
			self.text = "видит комментарии"
		elif self.type == "create_el":
			self.users = self.list.get_create_el_include_users()
			self.text = "создает записи и потом с ними работает"
		elif self.type == "create_comment":
			self.users = self.list.get_create_comment_include_users()
			self.text = "пишет комментарии"
		elif self.type == "copy_el":
			self.users = self.list.get_copy_el_include_users()
			self.text = "может копировать записи и список"
		if self.list.community and request.user.is_administrator_of_community(self.list.community.pk):
			self.template_name = get_detect_platform_template("posts/include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		elif request.user.pk == self.list.creator.pk:
			self.template_name = get_detect_platform_template("posts/include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostListLoadIncludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostListLoadIncludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["list"] = self.list
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		return self.request.user.get_all_friends()

	def post(self,request,*args,**kwargs):
		from posts.models import PostsList
		from django.http import HttpResponse

		if request.is_ajax():
			self.list = PostsList.objects.get(pk=self.kwargs["pk"])
			self.list.post_include_users(request.POST.getlist("users"), request.POST.get("type"))
		return HttpResponse()

class PostListLoadExcludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		from posts.models import PostsList
		from common.templates import get_detect_platform_template

		self.list = PostsList.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_see_el":
			self.users = self.list.get_can_see_el_exclude_users()
			self.text = "видит записи"
		elif self.type == "can_see_comment":
			self.users = self.list.get_can_see_comment_exclude_users()
			self.text = "видит комментарии"
		elif self.type == "create_el":
			self.users = self.list.get_create_el_exclude_users()
			self.text = "создает записи и потом с ними работает"
		elif self.type == "create_comment":
			self.users = self.list.get_create_comment_exclude_users()
			self.text = "пишет комментарии"
		elif self.type == "copy_el":
			self.users = self.list.get_copy_el_exclude_users()
			self.text = "может копировать записи и список"
		if self.list.community and request.user.is_administrator_of_community(self.list.community.pk):
			self.template_name = get_detect_platform_template("posts/exclude_users.html", request.user, request.META['HTTP_USER_AGENT'])
		elif request.user.pk == self.list.creator.pk:
			self.template_name = get_detect_platform_template("posts/exclude_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostListLoadExcludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostListLoadExcludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["list"] = self.list
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		if self.list.community:
			return self.list.community.get_members()
		else:
			return self.request.user.get_all_friends()

	def post(self,request,*args,**kwargs):
		from posts.models import PostsList
		from django.http import HttpResponse

		if request.is_ajax():
			self.list = PostsList.objects.get(pk=self.kwargs["pk"])
			self.list.post_exclude_users(request.POST.getlist("users"), request.POST.get("type"))
		return HttpResponse()

class PostListLoadIncludeUsers(ListView):
	template_name, users = None, []

	def get(self,request,*args,**kwargs):
		from posts.models import PostsList
		from common.templates import get_detect_platform_template

		self.list = PostsList.objects.get(pk=self.kwargs["pk"])
		self.type = request.GET.get("action")
		if self.type == "can_see_el":
			self.users = self.list.get_can_see_el_include_users()
			self.text = "видит записи"
		elif self.type == "can_see_comment":
			self.users = self.list.get_can_see_comment_include_users()
			self.text = "видит комментарии"
		elif self.type == "create_el":
			self.users = self.list.get_create_el_include_users()
			self.text = "создает записи и потом с ними работает"
		elif self.type == "create_comment":
			self.users = self.list.get_create_comment_include_users()
			self.text = "пишет комментарии"
		elif self.type == "copy_el":
			self.users = self.list.get_copy_el_include_users()
			self.text = "может копировать записи и список"
		if self.list.community and request.user.is_administrator_of_community(self.list.community.pk):
			self.template_name = get_detect_platform_template("posts/include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		elif request.user.pk == self.list.creator.pk:
			self.template_name = get_detect_platform_template("posts/include_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostListLoadIncludeUsers,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostListLoadIncludeUsers,self).get_context_data(**kwargs)
		context["users"] = self.users
		context["list"] = self.list
		context["text"] = self.text
		context["type"] = self.type
		return context

	def get_queryset(self):
		if self.list.community:
			return self.list.community.get_members()
		else:
			return self.request.user.get_all_friends()

	def post(self,request,*args,**kwargs):
		from posts.models import PostsList
		from django.http import HttpResponse

		if request.is_ajax():
			self.list = PostsList.objects.get(pk=self.kwargs["pk"])
			self.list.post_include_users(request.POST.getlist("users"), request.POST.get("type"))
		return HttpResponse()


class LoadPostsList(ListView):
	template_name, community, paginate_by, is_user_can_see_post_list, \
	is_user_can_see_post_section, is_user_can_create_postspost_lists,  = \
	None, None, 15, None, None, None, None

	def get(self,request,*args,**kwargs):
		if request.GET.get("user"):
			from users.models import User
			self.item = User.objects.get(pk=request.GET.get("user"))
			self.post_lists = PostsList.get_user_lists(self.item.pk)
			self.get_fixed_posts = self.item.get_fixed_posts()
			self.list = PostsList.objects.get(pk=self.item.get_selected_post_list_pk())
		elif request.GET.get("community"):
			from communities.models import Community
			self.item = Community.objects.get(pk=request.GET.get("community"))
			self.post_lists = PostsList.get_community_lists(self.item.pk)
			self.get_fixed_posts = self.item.get_fixed_posts()
			self.community = self.item
			self.list = PostsList.objects.get(pk=self.item.get_selected_post_list_pk())
		if request.GET.get("list"):
			self.list = PostsList.objects.get(pk=request.GET.get("list"))
		if request.user.is_anonymous:
			self.is_user_can_see_post_list = self.list.is_anon_user_can_see_el()
			if self.list.community:
				self.community = self.list.community
				self.template_name = get_template_anon_community_list(self.list, "communities/lenta/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_post_section = self.community.is_anon_user_can_see_post()
			else:
				self.template_name = get_template_anon_user_list(self.list, "users/lenta/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_post_section = self.list.creator.is_anon_user_can_see_post()
		else:
			self.is_user_can_see_post_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_posts = self.list.is_user_can_create_el(request.user.pk)
			if self.list.community:
				self.community = self.list.community
				self.template_name = get_template_community_list(self.list, "communities/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_post_section = self.community.is_user_can_see_post(request.user.pk)
			else:
				self.template_name = get_template_user_list(self.list, "users/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_post_section = self.list.creator.is_user_can_see_post(request.user.pk)
		return super(LoadPostsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadPostsList,self).get_context_data(**kwargs)
		context['list'] = self.list
		context['community'] = self.community
		context['is_user_can_see_post_section'] = self.is_user_can_see_post_section
		context['is_user_can_see_post_list'] = self.is_user_can_see_post_list
		context['is_user_can_create_posts'] = self.is_user_can_create_posts
		context['post_lists'] = self.post_lists
		context['get_fixed_posts'] = self.get_fixed_posts

		return context

	def get_queryset(self):
		return self.list.get_items()
