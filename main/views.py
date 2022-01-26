import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from common.templates import get_detect_main_template, get_default_template
from communities.models import Community
from users.models import User
from django.http import Http404


class SignupView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			if request.user.is_authenticated:
				self.template_name = "mobile/main/news_list/posts/posts.html"
			else:
				self.template_name = "mobile/main/auth/signup.html"
		else:
			if request.user.is_authenticated:
				self.template_name = "desctop/main/news_list/posts/posts.html"
			else:
				self.template_name = "mobile/main/auth/signup.html"
		return super(SignupView,self).get(request,*args,**kwargs)


class MainServicesView(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			if request.user.is_authenticated:
				self.template_name = "mobile/main/services.html"
			else:
				raise Http404
		else:
			if request.user.is_authenticated:
				self.template_name = "mobile/main/services.html"
			else:
				raise Http404
		return super(MainServicesView,self).get(request,*args,**kwargs)


class MainPhoneSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = "desctop/main/phone_verification.html"
		return super(MainPhoneSend,self).get(request,*args,**kwargs)

class LoadCustomLink(TemplateView):
	template_name, get_buttons_block, common_frends, common_friends_count, user, c = None, None, None, None, None, None

	def get(self,request,*args,**kwargs):
		from common.model.other import CustomLink
		try:
			self.custom_link = CustomLink.objects.get(link=self.kwargs["slug"])
		except:
			raise Http404
		if request.user.is_authenticated:
			if self.custom_link.user:
				from common.templates import get_template_user, get_template_anon_user

				self.user = self.custom_link.user
				self.template_name = get_template_user(self.user, "main/tooltip/user/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
				if request.user.pk != self.user.pk:
					self.get_buttons_block, self.common_frends, self.common_friends_count = request.user.get_buttons_profile(self.user.pk), self.user.get_common_friends_of_user(request.user)[0:5], request.user.get_common_friends_of_user_count_ru(self.user.pk)
			if self.custom_link.community:
				from common.templates import get_template_community, get_template_anon_community

				self.c = self.custom_link.community
				self.template_name = get_template_user(self.c, "main/tooltip/community/", "page.html", request.user, request.META['HTTP_USER_AGENT'])
				self.common_friends, self.common_friends_count = request.user.get_common_friends_of_community(self.c.pk)[0:6], request.user.get_common_friends_of_community_count_ru(self.c.pk)
		return super(LoadCustomLink,self).get(request,*args,**kwargs)


class SwitchView(TemplateView):
	template_name, get_buttons_block, common_frends, common_friends_count, user, c = None, None, None, None, None, None

	def get(self,request,*args,**kwargs):
		from stst.models import UserNumbers, CommunityNumbers
		from common.model.other import CustomLink

		try:
			self.custom_link = CustomLink.objects.get(link=self.kwargs["slug"])
		except:
			raise Http404

		if self.custom_link.user:
			self.user = self.custom_link.user
			user_agent = request.META['HTTP_USER_AGENT']
			r_user_pk = request.user.pk
			self.post_list_pk = self.user.get_selected_post_list_pk()
			user_pk = int(self.user.pk)
			if request.user.is_authenticated:
				if user_pk == r_user_pk:
					if self.user.is_suspended():
						self.template_name = "generic/u_template/you_suspended.html"
					elif self.user.is_closed():
						self.template_name = "generic/u_template/you_global_block.html"
					elif self.user.is_child():
						self.template_name = "users/account/my_user_child.html"
					else:
						self.template_name = "users/account/my_user.html"
				elif r_user_pk != user_pk:
					self.get_buttons_block, self.common_frends = request.user.get_buttons_profile(user_pk), self.user.get_common_friends_of_user(self.request.user)[0:5]
					if self.user.is_suspended():
						self.template_name = "generic/u_template/user_suspended.html"
					elif self.user.is_closed():
						self.template_name = "generic/u_template/user_global_block.html"
					elif request.user.is_manager() or request.user.is_superuser:
						self.template_name, self.get_buttons_block = "users/account/staff_user.html", request.user.get_staff_buttons_profile(user_pk)
						if request.user.is_connected_with_user_with_id(user_id=user_pk):
							request.user.plus_friend_visited(user_pk)
					elif request.user.is_blocked_with_user_with_id(user_id=user_pk):
						self.template_name = "users/account/block_user.html"
					elif request.user.is_connected_with_user_with_id(user_id=user_pk):
						self.template_name = "users/account/user.html"
						request.user.plus_friend_visited(user_pk)
					elif self.user.is_closed_profile():
						if request.user.is_followers_user_with_id(user_id=user_pk) or request.user.is_connected_with_user_with_id(user_id=user_pk):
							self.template_name = "users/account/user.html"
						else:
							self.template_name = "users/account/close_user.html"
					elif request.user.is_child() and not self.user.is_child_safety():
						self.template_name = "users/account/no_child_safety.html"
					else:
						self.template_name = "users/account/user.html"
					if MOBILE_AGENT_RE.match(user_agent):
						UserNumbers.objects.create(visitor=r_user_pk, target=user_pk, device=UserNumbers.PHONE)
					else:
						UserNumbers.objects.create(visitor=r_user_pk, target=user_pk, device=UserNumbers.DESCTOP)
			elif request.user.is_anonymous:
				if self.user.is_suspended():
					self.template_name = "generic/u_template/anon_user_suspended.html"
				elif self.user.is_closed():
					self.template_name = "generic/u_template/anon_user_global_block.html"
				elif self.user.is_closed_profile():
					self.template_name = "users/account/anon_close_user.html"
				elif not self.user.is_child_safety():
					self.template_name = "users/account/anon_no_child_safety.html"
				else:
					self.template_name = "users/account/anon_user.html"
			self.fix_list, self.photo_list, self.video_list, self.playlist, self.doc_list, self.good_list = self.user.get_fixed_posts(), self.user.get_photo_list(), self.user.get_video_list(), self.user.get_playlist(), self.user.get_doc_list(), self.user.get_good_list()
		elif self.custom_link.community:
			self.c, user_agent, c_pk, u_pk = self.custom_link.community, request.META['HTTP_USER_AGENT'], int(self.kwargs["slug"]), request.user.pk
			c_pk = self.c.pk
			self.post_list_pk = self.c.get_selected_post_list_pk()
			if self.c.is_suspended():
				self.template_name = "communities/detail/community_suspended.html"
			elif self.c.is_blocked():
				self.template_name = "communities/detail/community_blocked.html"
			elif request.user.is_authenticated:
				if request.user.is_member_of_community(c_pk):
					if request.user.is_administrator_of_community(c_pk):
						self.template_name = "communities/detail/admin_community.html"
					elif request.user.is_moderator_of_community(c_pk):
						self.template_name = "communities/detail/moderator_community.html"
					elif request.user.is_editor_of_community(c_pk):
						self.template_name = "communities/detail/editor_community.html"
					elif request.user.is_advertiser_of_community(c_pk):
						self.template_name = "communities/detail/advertiser_community.html"
					elif request.user.is_community_manager():
						self.template_name = "communities/detail/staff_member_community.html"
					else:
						self.template_name = "communities/detail/member_community.html"
					request.user.plus_community_visited(c_pk)
				elif request.user.is_follow_from_community(c_pk):
					self.template_name = "communities/detail/follow_community.html"
				elif request.user.is_community_manager():
					self.template_name = "communities/detail/staff_community.html"
				elif request.user.is_banned_from_community(c_pk):
					self.template_name = "communities/detail/block_community.html"
				elif self.c.is_public():
					if request.user.is_child() and not self.c.is_verified():
						self.template_name = "communities/detail/no_child_safety.html"
					else:
						self.template_name = "communities/detail/public_community.html"
				elif self.c.is_closd():
					self.template_name = "communities/detail/close_community.html"
				elif self.c.is_private():
					self.template_name = "generic/c_template/private_community.html"
				if MOBILE_AGENT_RE.match(user_agent):
					CommunityNumbers.objects.create(user=u_pk, community=c_pk, device=CommunityNumbers.PHONE)
				else:
					CommunityNumbers.objects.create(user=u_pk, community=c_pk, device=CommunityNumbers.DESCTOP)
				self.common_friends, self.common_friends_count = request.user.get_common_friends_of_community(c_pk)[0:6], request.user.get_common_friends_of_community_count_ru(c_pk)
			elif request.user.is_anonymous:
				if self.c.is_public():
					if not self.c.is_verified():
						self.template_name = "communities/detail/anon_no_child_safety.html"
					else:
						self.template_name = "communities/detail/anon_community.html"
				elif self.c.is_close():
					self.template_name = "communities/detail/anon_close_community.html"
				elif self.c.is_private():
					self.template_name = "communities/detail/anon_private_community.html"
			self.fix_list, self.photo_list, self.video_list, self.playlist, self.doc_list, self.good_list = self.c.get_fixed_posts(), self.c.get_photo_list(), self.c.get_video_list(), self.c.get_or_create_playlist(), self.c.get_doc_list(), self.c.get_good_list()

		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mobile/" + self.template_name
		else:
			self.template_name = "mobile/" + self.template_name
		return super(SwitchView,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		c = super(SwitchView, self).get_context_data(**kwargs)
		c['user'], c['custom_link'], c['community'], c['fix_list'], c['photo_list'], c['video_list'],c['playlist'], \
		c['docs_list'], c['good_list'], c['get_buttons_block'], c['common_frends'], c['common_friends_count'], c['post_list_pk'] = self.user, \
		self.custom_link, self.c, self.fix_list, self.photo_list, self.video_list, self.playlist, self.doc_list, \
		self.good_list, self.get_buttons_block, self.common_frends, self.common_friends_count, self.post_list_pk
		return c


class NewsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/lists/news_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(NewsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		from common.user_progs.news import get_news
		if self.request.user.is_authenticated and self.request.user.type[0] != "_":
			return get_news(self.request.user)
		else:
			return []

class FeaturedListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/lists/featured_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		from common.user_progs.news import get_featured_news
		if self.request.user.is_authenticated and self.request.user.type[0] != "_":
			items = get_featured_news(self.request.user)
		else:
			items = []
		return items
