from django.views.generic import ListView
from users.models import User
from django.http import Http404
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								#get_template_community_list,
								#get_template_anon_community_list,
								#get_template_user_list,
								#get_template_anon_user_list,
							)

class ItemCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_comments
		from common.utils import get_item_with_comments

		self.type = request.GET.get('type')
		self.item = get_item_with_comments(self.type)
		self.prefix = self.type[:3]
		self.template_name = get_template_comments(self.item, "generic/items/comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest' or not self.item.comments_enabled:
			raise Http404
		return super(ItemCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(ItemCommentList, self).get_context_data(**kwargs)
		context['item'] = self.item
		context['prefix'] = self.prefix
		context['type'] = self.type
		return context

	def get_queryset(self):
		return self.item.get_comments()


class CommentLikes(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.utils import get_comment

		self.type = request.GET.get('type')
		self.comment = get_comment(self.type)
		item = self.comment.get_item()
		if not item.votes_on:
			raise Http404
		if request.user.is_authenticated:
			if not item.list.is_user_can_see_el(request.user.pk):
				raise Http404
			if item.community:
				self.template_name = get_template_community_item(item, "generic/items/comment/", "likes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_item(item, "generic/items/comment/", "likes.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if not item.list.is_anon_user_can_see_el(request.user.pk):
				raise Http404
			if item.community:
				self.template_name = get_template_anon_community_item(item, "generic/items/comment/anon_likes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(item, "generic/items/comment/anon_likes.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommentLikes,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommentLikes,self).get_context_data(**kwargs)
		context['item'] = self.comment
		context['text'] = "Комментарий одобрили:"
		return context

	def get_queryset(self):
		return User.objects.filter(id__in=self.comment.likes().values("user_id"))

class CommentDislikes(ListView):
	template_name, paginate_by = None, 12

	def get(self,request,*args,**kwargs):
		from common.utils import get_comment

		self.type = request.GET.get('type')
		self.comment = get_comment(self.type)
		item = self.comment.get_item()
		if not item.votes_on:
			raise Http404
		if request.user.is_authenticated:
			if not item.list.is_user_can_see_el(request.user.pk):
				raise Http404
			if item.community:
				self.template_name = get_template_community_item(item, "generic/items/comment/", "dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_item(item, "generic/items/comment/", "dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if not item.list.is_anon_user_can_see_el(request.user.pk):
				raise Http404
			if item.community:
				self.template_name = get_template_anon_community_item(item, "generic/items/comment/anon_dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(item, "generic/items/comment/anon_dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommentDislikes,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommentDislikes,self).get_context_data(**kwargs)
		context['item'] = self.comment
		context['text'] = "Комментарий не одобрили:"
		return context

	def get_queryset(self):
		return User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
