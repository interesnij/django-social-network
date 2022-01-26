from django.views.generic import ListView
from users.models import User


class ItemCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_comments
		self.type = request.GET.get('type')
		self.item = request.user.get_item(self.type)
		self.prefix = self.type[:3]
		self.template_name = get_template_comments(self.item, "generic/items/comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		if not request.is_ajax() or not self.item.comments_enabled:
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
		self.type = request.GET.get('type')
		self.comment = request.user.get_comment(self.type)
		if not self.comment.get_item().votes_on:
			raise Http404
		if request.user.is_authenticated:
			if not self.comment.get_item().list.is_user_can_see_el(request.user.pk):
				raise Http404
			self.template_name = get_template_user_item(self.comment.item, "generic/items/comment/", "likes.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if not self.comment.get_item().list.is_anon_user_can_see_el(request.user.pk):
				raise Http404
			self.template_name = get_template_anon_user_item(self.comment.item, "generic/items/comment/anon_likes.html", request.user, request.META['HTTP_USER_AGENT'])
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
		self.type = request.GET.get('type')
		self.comment = request.user.get_comment(self.type)
		if not self.comment.get_item().votes_on:
			raise Http404
		if request.user.is_authenticated:
			if not self.comment.get_item().list.is_user_can_see_el(request.user.pk):
				raise Http404
			self.template_name = get_template_user_item(self.comment.item, "generic/items/comment/", "dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if not self.comment.get_item().list.is_anon_user_can_see_el(request.user.pk):
				raise Http404
			self.template_name = get_template_anon_user_item(self.comment.item, "generic/items/comment/anon_dislikes.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommentDislikes,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommentDislikes,self).get_context_data(**kwargs)
		context['item'] = self.comment
		context['text'] = "Комментарий не одобрили:"
		return context

	def get_queryset(self):
		return User.objects.filter(id__in=self.comment.dislikes().values("user_id"))
