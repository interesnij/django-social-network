from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from main.forms import CommentForm
from django.template.loader import render_to_string
from django.views import View
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gallery.models import Album, Photo


class ItemUserCommentList(View):
	model=ItemComment

	def get(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user != request.user and request.user.is_authenticated:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile():
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
			comments = item.get_comments(request.user)
		elif self.user == request.user:
			comments = item.get_comments(request.user)
		elif request.user.is_anonymous and self.user.is_closed_profile():
			raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			comments = item.get_comments(request.user)
		page = request.GET.get('page')
		current_page = Paginator(comments, 6)
		try:
			comment_list = current_page.page(page)
		except PageNotAnInteger:
			comment_list = current_page.page(1)
		except EmptyPage:
			comment_list = current_page.page(current_page.num_pages)
		comments_html = render_to_string("item_user/comments.html", {"comment_list": comment_list, "request_user": request.user, "parent": item, "form_comment": CommentForm(), "form_reply": CommentForm(), "user": self.user})

		return JsonResponse({ "comments": comments_html, })


class ItemCommentUserCreate(View):
	form_post = None
	def post(self,request,*args,**kwargs):
		form_post = CommentForm(request.POST, request.FILES)
		user = User.objects.get(pk=request.POST.get('id'))
		item_uuid = request.POST.get('item')
		item = Item.objects.get(uuid=item_uuid)
		if form_post.is_valid():
			comment=form_post.save(commit=False)
			item_comment_photo=form_post.cleaned_data['item_comment_photo']
			item_comment_photo2=form_post.cleaned_data['item_comment_photo2']

			if not comment.text and not item_comment_photo and not item_comment_photo2:
				raise ValidationError('Для добавления комментария необходимо написать что-то или прикрепить изображение')
			if request.user.pk != user.pk:
				check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.pk)
				if user.is_closed_profile():
					check_is_connected_with_user_with_id(user=request.user, user_id = user.pk)
			new_comment = comment.create_user_comment(commenter=request.user, parent_comment=None, item=item, text=comment.text)
			if item_comment_photo:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=None)
				Photo.objects.create(creator=request.user, file=item_comment_photo,community=None,is_public=True, album=album, item_comment=new_comment)
			if item_comment_photo2:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=None)
				Photo.objects.create(creator=request.user, file=item_comment_photo2,community=None,is_public=True, album=album, item_comment=new_comment)
			new_comment.notification_user_comment(request.user)
			html = render_to_string('item_user/parent_comment.html',{'comment': new_comment, 'request_user': request.user, "form_reply": CommentForm(), 'request': request})
			return JsonResponse(html, safe=False)
		else:
			return HttpResponseBadRequest()


class ItemReplyUserCreate(View):
	def post(self,request,*args,**kwargs):
		form_post=CommentForm(request.POST, request.FILES)
		user=User.objects.get(uuid=self.kwargs["uuid"])
		parent = ItemComment.objects.get(pk=self.kwargs["pk"])

		if form_post.is_valid():
			comment=form_post.save(commit=False)
			item_comment_photo=form_post.cleaned_data['item_comment_photo']
			item_comment_photo2=form_post.cleaned_data['item_comment_photo2']
			if not comment.text and not item_comment_photo and not item_comment_photo2:
				raise ValidationError('Для добавления комментария необходимо написать что-то или прикрепить изображение')
			if request.user != user:
				check_is_not_blocked_with_user_with_id(user=request.user, user_id = user.id)
				if user.is_closed_profile():
					check_is_connected_with_user_with_id(user=request.user, user_id = user.id)

			new_comment = comment.create_user_comment(commenter=request.user, text=comment.text, parent_comment=parent)
			if item_comment_photo:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=None)
				Photo.objects.create(creator=request.user, file=item_comment_photo,community=None,is_public=True, album=album, item_comment=new_comment)
			if item_comment_photo2:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=None)
				Photo.objects.create(creator=request.user, file=item_comment_photo2,community=None,is_public=True, album=album, item_comment=new_comment)
			new_comment.notification_user_reply_comment(request.user)
			html = render_to_string('item_user/reply_comment.html',{'reply': new_comment, 'request_user': request.user, "form_reply": CommentForm(), 'request': request})
			return JsonResponse(html, safe=False)
		else:
			return HttpResponseBadRequest()


def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Item.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


def user_fixed(request, pk, item_uuid):
	item = Item.objects.get(pk=pk)
	current_user = User.objects.get(uuid=user_uuid)
	if request.user == current_user:
		item.is_fixed=True
		item.save()
		return HttpResponse("!")
	else:
		return HttpResponse("Закрепляйте, пожалуйста, свои записи!")


def user_unfixed(request, pk, user_uuid):
	item = Item.objects.get(pk=pk)
	current_user = User.objects.get(uuid=user_uuid)
	if request.user == current_user:
		item.is_fixed=False
		item.save()
		return HttpResponse("!")
	else:
		return HttpResponse("Открепляйте, пожалуйста, свои записи!")

def user_item_delete(request, pk, user_uuid):
	item = Item.objects.get(pk=pk)
	current_user = User.objects.get(uuid=user_uuid)
	if request.user == current_user:
		item.is_deleted=True
		item.save()
		return HttpResponse("!")
	else:
		return HttpResponse("Удаляйте, пожалуйста, свои записи!")
