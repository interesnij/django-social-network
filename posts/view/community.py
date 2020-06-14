from django.views.generic.base import TemplateView
from django.views.generic import ListView
from communities.models import Community
from posts.models import Post, PostComment
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import CommentForm
from django.views import View
from common.checkers import check_can_get_posts_for_community_with_name
from rest_framework.exceptions import ValidationError
from django.shortcuts import render_to_response


class PostCommunityCommentList(ListView):
    template_name = None
    model = PostComment
    paginate_by = 30

    def get(self,request,*args,**kwargs):
        self.item = Post.objects.get(uuid=self.kwargs["uuid"])
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_template_list(folder="c_post_comment/", template="comments.html", request=request)
        return super(PostCommunityCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostCommunityCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.item
        context['form_comment'] = CommentForm()
        context['form_reply'] = CommentForm()
        context['community'] = self.community
        return context

    def get_queryset(self):
        comments = self.item.get_comments()
        return comments


class PostCommunityCommentCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST, request.FILES)
        community = Community.objects.get(pk=request.POST.get('id'))
        item_uuid = request.POST.get('item')
        item = Post.objects.get(uuid=item_uuid)
        if form_post.is_valid():
            check_can_get_posts_for_community_with_name(request.user,community.name)
            comment=form_post.save(commit=False)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, community=community, parent_comment=None, post=post, text=comment.text)
                get_comment_attach(request, new_comment)
                new_comment.notification_community_comment(request.user)
                return render_to_response('c_post_comment/admin_parent.html',{'comment': new_comment, 'request_user': request.user, 'community': community, "form_reply": CommentForm(), 'request': request})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class PostCommunityReplyCreate(View):
    def post(self,request,*args,**kwargs):
        form_post=CommentForm(request.POST, request.FILES)
        uuid = request.POST.get('uuid')
        pk = request.POST.get('pk')
        community=Community.objects.get(uuid=uuid)
        parent = PostComment.objects.get(pk=pk)

        if form_post.is_valid():
            check_can_get_posts_for_community_with_name(request.user,community.name)
            comment=form_post.save(commit=False)
            if request.POST.get('text') or  request.POST.get('photo') or request.POST.get('video') or request.POST.get('music') or request.POST.get('good') or request.POST.get('article'):
                from common.comment_attacher import get_comment_attach
                new_comment = comment.create_comment(commenter=request.user, parent_comment=parent, text=comment.text)
                get_comment_attach(request, new_comment)
                new_comment.notification_community_reply_comment(request.user)
                return render_to_response('c_post_comment/admin_reply.html',{'reply': new_comment, 'request_user': request.user, 'community': community, 'comment': parent,  "form_reply": CommentForm(), 'request': request})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Post.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)


def community_fixed(request, pk, uuid):
	item = Post.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.get_fixed_for_community(pk)
		return HttpResponse("!")
	else:
		return HttpResponse("Закрепляйте, пожалуйста, свои записи!")

def community_unfixed(request, pk, uuid):
	item = Post.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_fixed=False
		item.save(update_fields=['is_fixed'])
		return HttpResponse("!")
	else:
		return HttpResponse("Открепляйте, пожалуйста, свои записи!")

def community_off_comment(request, pk, uuid):
    item = Post.objects.get(uuid=uuid)
    community = Community.objects.get(pk=pk)
    if request.user.is_staff_of_community_with_name(community.name):
        item.comments_enabled=False
        item.save(update_fields=['comments_enabled'])
        return HttpResponse("!")
    else:
        return HttpResponse("Закрепляйте, пожалуйста, свои записи!")

def community_on_comment(request, pk, uuid):
	item = Post.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.comments_enabled=True
		item.save(update_fields=['comments_enabled'])
		return HttpResponse("!")
	else:
		return HttpResponse("Открепляйте, пожалуйста, свои записи!")

def community_item_delete(request, pk, uuid):
	item = Post.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_deleted=True
		item.save(update_fields=['is_deleted'])
		return HttpResponse("!")
	else:
		return HttpResponse("Удаляйте, пожалуйста, свои записи!")

def community_item_abort_delete(request, pk, uuid):
	item = Post.objects.get(uuid=uuid)
	community = Community.objects.get(pk=pk)
	if request.user.is_staff_of_community_with_name(community.name):
		item.is_deleted=False
		item.save(update_fields=['is_deleted'])
		return HttpResponse("!")
	else:
		return HttpResponse("Удаляйте, пожалуйста, свои записи!")


class PostCommunityDetail(TemplateView):
	template_name = "post_community/detail.html"

	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			check_can_get_posts_for_community_with_name(request.user,self.community.name)
			self.object = self.item
		if request.user.is_anonymous and self.community.is_public:
			self.comments = item.get_comments(request.user)
		if request.user.is_anonymous and (self.community.is_closed or self.community.is_private):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('У Вас недостаточно прав для просмотра информации группы')
        return super(PostCommunityDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(PostCommunityDetail,self).get_context_data(**kwargs)
		context["object"]=self.object
		return context
