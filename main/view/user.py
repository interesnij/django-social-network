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


class ItemUserCommentList(View):
	model=ItemComment

	def get(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if self.user != request.user and request.user.is_authenticated:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile:
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
			comments = item.get_comments(request.user).order_by('-created')
		elif self.user == request.user:
			comments = item.get_comments(request.user).order_by('-created')
		elif request.user.is_anonymous and self.user.is_closed_profile():
			raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			comments = item.get_comments(request.user).order_by('-created')
		comments_html = render_to_string("item_user/comments.html", {"comments": comments,"parent": item, "form_comment": CommentForm(), "user": self.user})

		return JsonResponse({
	        "comments": comments_html,
	    })


class ItemCommentUserCreate(View):
	def post(self,request,*args,**kwargs):
		self.form_post=CommentForm(request.POST, request.FILES)
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.item = Item.objects.get(uuid=self.kwargs["uuid"])

		if self.form_post.is_valid():
			comment=self.form_post.save(commit=False)
			self.text = comment.text
			if request.user != self.user:
				check_is_not_blocked_with_user_with_id(user=request.user, user_id = self.user.id)
				if user.is_closed_profile:
					check_is_connected_with_user_with_id(user=request.user, user_id = self.user.id)
			if not comment.text and not comment.item_comment_photo:
				raise ValidationError('Для добавления комментария необходимо написать что-то или прикрепить изображение')
			new_comment = comment.create_user_comment(
														commenter=request.user,
														item=self.item,
														item_comment_photo=comment.item_comment_photo,
														item_comment_photo2=comment.item_comment_photo2,
														text=self.text)
			new_comment.notification_user_comment(request.user)
			html = render_to_string('item_user/parent_comment.html',{'comment': new_comment, 'request': request})
			return JsonResponse(html, safe=False)
		else:
			return HttpResponse(comment.item_comment_photo)


def item_reply_comment(request):

    user = request.user
    text = request.POST['text']
    com = request.POST['comment']
    comment = ItemComment.objects.get(pk=com)
    text = text.strip()
    if len(text) > 0:
        new_comment = ItemComment.objects.create(text=text, commenter=request.user,parent_comment=comment)
        html = render_to_string('item_user/reply_comment.html',{'reply': new_comment,'request': request})
        return JsonResponse(html, safe=False)

        notification_handler(
            user, parent.creator, Notification.ARTICLE_REPLY_COMMENT, action_object=reply_article,
            id_value=str(com.id), key='social_update')

    else:
        return HttpResponseBadRequest()


def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Item.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


def user_fixed(request, pk, item_uuid):
	item = Item.objects.get(pk=pk)
	current_user = User.objects.get(uuid=item_uuid)
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
