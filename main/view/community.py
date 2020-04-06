from django.views.generic.base import TemplateView
from django.views.generic import ListView
from communities.models import Community
from main.models import Item, ItemComment
from django.http import HttpResponse, HttpResponseBadRequest
from main.forms import CommentForm
from django.views import View
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import PermissionDenied, ValidationError
from gallery.models import Album, Photo
from django.shortcuts import render_to_response


class ItemCommunityCommentList(ListView):
    template_name = None
    model = ItemComment
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.item = Item.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_template_list(folder="c_item_comment/", template="comments.html", request=request)
        return super(ItemCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ItemCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.item
        context['form_comment'] = CommentForm()
        context['form_reply'] = CommentForm()
        context['community'] = self.community
        return context

    def get_queryset(self):
        comments = self.item.get_comments()
        return comments


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
			new_comment = comment.create_comment(commenter=request.user, parent_comment=None, item=item, text=comment.text)
			if photo:
				try:
					album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				except:
					album=Album.objects.create(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				upload_photo = Photo.objects.create(creator=request.user, file=photo, community=community, is_public=True, album=album)
				upload_photo.item_comment.add(new_comment)
			if photo2:
				try:
					album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				except:
					album=Album.objects.create(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
				upload_photo2 = Photo.objects.create(creator=request.user, file=photo2, community=community, is_public=True, album=album)
				upload_photo2.item_comment.add(new_comment)
			new_comment.notification_community_comment(request.user)
			return render_to_response('c_item_comment/admin_parent.html',{'comment': new_comment, 'request_user': request.user, 'community': community, "form_reply": CommentForm(), 'request': request})
		else:
			return HttpResponseBadRequest()


class ItemCommunityReplyCreate(View):
    def post(self,request,*args,**kwargs):
        form_post=CommentForm(request.POST, request.FILES)
        uuid = request.POST.get('uuid')
        pk = request.POST.get('pk')
        community=Community.objects.get(uuid=uuid)
        parent = ItemComment.objects.get(pk=pk)

        if form_post.is_valid():
            comment=form_post.save(commit=False)
            photo=form_post.cleaned_data['photo']
            photo2=form_post.cleaned_data['photo2']
            if not comment.text and not photo and not photo2:
                raise ValidationError('Для добавления комментария необходимо написать что-то или прикрепить изображение')
            check_can_get_posts_for_community_with_name(request.user,community.name)
            new_comment = comment.create_comment(commenter=request.user, text=comment.text, parent_comment=parent)
            if photo:
                try:
                    album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
                except:
                    album=Album.objects.create(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
                upload_photo = Photo.objects.create(creator=request.user, file=photo, community=community, album=album)
                upload_photo.item_comment.add(new_comment)
            if photo2:
                try:
                    album=Album.objects.get(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
                except:
                    album=Album.objects.create(creator=request.user, title="Сохраненные фото", is_generic=True, community=community)
                upload_photo2 = Photo.objects.create(creator=request.user, file=photo2, community=community, album=album)
            upload_photo2.item_comment.add(new_comment)
            new_comment.notification_community_reply_comment(request.user)
            return render_to_response('c_item_comment/admin_reply.html',{'reply': new_comment, 'request_user': request.user, 'community': community, 'comment': parent,  "form_reply": CommentForm(), 'request': request})
        else:
            return HttpResponseBadRequest()


def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Item.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


def community_fixed(request, pk, uuid):
	item = Item.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.get_fixed_for_community(pk)
		return HttpResponse("!")
	else:
		return HttpResponse("Закрепляйте, пожалуйста, свои записи!")

def community_unfixed(request, pk, uuid):
	item = Item.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_fixed=False
		item.save(update_fields=['is_fixed'])
		return HttpResponse("!")
	else:
		return HttpResponse("Открепляйте, пожалуйста, свои записи!")

def community_off_comment(request, pk, uuid):
    item = Item.objects.get(uuid=uuid)
    community = Community.objects.get(pk=pk)
    if request.user.is_staff_of_community_with_name(community.name):
        item.comments_enabled=False
        item.save(update_fields=['comments_enabled'])
        return HttpResponse("!")
    else:
        return HttpResponse("Закрепляйте, пожалуйста, свои записи!")

def community_on_comment(request, pk, uuid):
	item = Item.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.comments_enabled=True
		item.save(update_fields=['comments_enabled'])
		return HttpResponse("!")
	else:
		return HttpResponse("Открепляйте, пожалуйста, свои записи!")

def community_item_delete(request, pk, uuid):
	item = Item.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_deleted=True
		item.save(update_fields=['is_deleted'])
		return HttpResponse("!")
	else:
		return HttpResponse("Удаляйте, пожалуйста, свои записи!")


class ItemCommunityDetail(TemplateView):
	template_name = "item_community/detail.html"

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			self.object = self.item
		if request.user.is_anonymous and self.community.is_public:
			self.comments = item.get_comments(request.user)
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
			raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
		return super(ItemCommunityDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ItemCommunityDetail,self).get_context_data(**kwargs)
		context["object"]=self.object
		return context
