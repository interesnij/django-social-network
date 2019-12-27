from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from main.models import Item, ItemComment
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from main.forms import CommentForm
from django.template.loader import render_to_string
from django.views import View
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gallery.models import Album, Photo


class ItemCommunityCommentList(View):
	model=ItemComment

	def get(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			comments = item.get_comments(request.user)
			current_page = Paginator(comments, 10)
		if request.user.is_anonymous and self.community.is_public:
			comments = item.get_comments(request.user)
			current_page = Paginator(comments, 10)
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
			raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
		page = request.GET.get('page')
		current_page = Paginator(comments, 10)
		try:
			comment_list = current_page.page(page)
		except PageNotAnInteger:
			comment_list = current_page.page(1)
		except EmptyPage:
			comment_list = current_page.page(current_page.num_pages)
		comments_html = render_to_string("item_community/comments.html", {"comment_list": comment_list, "request_user": request.user, "parent": item, "form_comment": CommentForm(), "form_reply": CommentForm(), "community": self.community})

		return JsonResponse({ "comments": comments_html, })


class ItemCommunityCommentCreate(View):
	form_post = None
	def post(self,request,*args,**kwargs):
		form_post = CommentForm(request.POST, request.FILES)
		community = Community.objects.get(pk=request.POST.get('id'))
		item_uuid = request.POST.get('item')
		item = Item.objects.get(uuid=item_uuid)
		if form_post.is_valid():
			comment=form_post.save(commit=False)
			photo=form_post.cleaned_data['photo']
			photo2=form_post.cleaned_data['photo2']

			if not comment.text and not photo and not photo2:
				raise ValidationError('Напишите что-нибудь или прикрепите изображение')
			check_can_get_posts_for_community_with_name(request.user,community.name)
			new_comment = comment.create_user_comment(commenter=request.user, parent_comment=None, item=item, text=comment.text)
			if photo:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				upload_photo = Photo.objects.create(creator=request.user, file=photo, community=community, is_public=True, album=album)
				upload_photo.item_comment.add(new_comment)
			if photo2:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				upload_photo2 = Photo.objects.create(creator=request.user, file=photo2, community=community, is_public=True, album=album)
				upload_photo2.item_comment.add(new_comment)
			new_comment.notification_community_comment(request.user)
			html = render_to_string('item_community/parent_comment.html',{'comment': new_comment, 'request_user': request.user, "form_reply": CommentForm(), 'request': request})
			return JsonResponse(html, safe=False)
		else:
			return HttpResponseBadRequest()


class ItemCommunityReplyCreate(View):
	def post(self,request,*args,**kwargs):
		form_post=CommentForm(request.POST, request.FILES)
		community=Community.objects.get(uuid=self.kwargs["uuid"])
		parent = ItemComment.objects.get(pk=self.kwargs["pk"])

		if form_post.is_valid():
			comment=form_post.save(commit=False)
			photo=form_post.cleaned_data['photo']
			photo2=form_post.cleaned_data['photo2']
			if not comment.text and not photo and not photo2:
				raise ValidationError('Для добавления комментария необходимо написать что-то или прикрепить изображение')
			check_can_get_posts_for_community_with_name(request.user,community.name)
			new_comment = comment.create_user_comment(commenter=request.user, text=comment.text, parent_comment=parent)
			if photo:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				upload_photo = Photo.objects.create(creator=request.user, file=photo, community=community, album=album)
				upload_photo.item_comment.add(new_comment)
			if photo2:
				album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				upload_photo2 = Photo.objects.create(creator=request.user, file=photo2, community=community, album=album)
				upload_photo2.item_comment.add(new_comment)
			new_comment.notification_user_reply_comment(request.user)
			html = render_to_string('item_community/reply_comment.html',{'reply': new_comment, 'request_user': request.user, "form_reply": CommentForm(), 'request': request})
			return JsonResponse(html, safe=False)
		else:
			return HttpResponseBadRequest()


def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Item.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


def community_fixed(request, pk, uuid):
	item = Item.objects.get(pk=pk)
	community = Community.objects.get(uuid=uuid)
	if request.user.is_staff_of_community_with_name(community.name):
		item.get_fixed_for_community(uuid)
		return HttpResponse("!")
	else:
		return HttpResponse("Закрепляйте, пожалуйста, свои записи!")


def community_unfixed(request, pk, uuid):
	item = Item.objects.get(pk=pk)
	community = Community.objects.get(uuid=uuid)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_fixed=False
		item.save(update_fields=['is_fixed'])
		return HttpResponse("!")
	else:
		return HttpResponse("Открепляйте, пожалуйста, свои записи!")

def community_item_delete(request, pk, uuid):
	item = Item.objects.get(pk=pk)
	community = Community.objects.get(uuid=uuid)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_deleted=True
		item.save(update_fields=['is_deleted'])
		return HttpResponse("!")
	else:
		return HttpResponse("Удаляйте, пожалуйста, свои записи!")


class ItemCommunityDetail(TemplateView):
	template_name = "item_community/detail.html"

	def get(self,request,*args,**kwargs):
		self.item = Item.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			self.object = self.item
		if request.user.is_anonymous and self.community.is_public:
			comments = item.get_comments(request.user)
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
			raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
		return super(ItemCommunityDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ItemCommunityDetail,self).get_context_data(**kwargs)
		context["object"]=self.object
		return context
