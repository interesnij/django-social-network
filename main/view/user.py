from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment, ItemReaction, ItemCommentReaction
from common.models import Emoji
from django.utils import timezone
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from main.forms import CommentForm
from django.template.loader import render_to_string
from django.views import View
from posts.models import Post
from generic.mixins import EmojiListMixin



class RepostUser(View):
	def post(self, request, *args, **kwargs):
		self.item = Item.objects.get(pk=self.kwargs["pk"])
		if self.item.parent:
			new_repost = Post.objects.create(creator=request.user, parent=self.item.parent, is_repost=True)
			return HttpResponse("репост репоста")
		else:
			new_repost = Post.objects.create(creator=request.user, parent=self.item, is_repost=True)
			return HttpResponse("репост item")


class ItemReactWindow(TemplateView):
	template_name="react_window.html"

	def get(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		emoji = Emoji.objects.get(pk=self.kwargs["pk"])
		react = ItemComment.objects.filter(item=item, emoji=emoji)
		return super(ItemReactWindow,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(ItemReactWindow,self).get_context_data(**kwargs)
		context["react"]=self.react
		return context


class ItemCommentReactWindow(TemplateView):
    template_name="comment_react_window.html"

    def get(self,request,*args,**kwargs):
        self.react_like = ItemComment.objects.get(pk=self.kwargs["pk"])
        return super(ItemCommentReactWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ItemCommentReactWindow,self).get_context_data(**kwargs)
        context["react_like"]=self.react_like
        return context


class ItemCommentList(View, EmojiListMixin):
	model=ItemComment

	def get(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		comments = ItemComment.objects.filter(item=item, parent_comment=None).order_by("created")
		comments_html = render_to_string("generic/posts/comments.html", {"comments": comments,"parent": item})

		return JsonResponse({
	        "comments": comments_html,
	    })


class ItemReactUserCreate(View):
	model=ItemReaction

	def post(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		emoji = Emoji.objects.get(pk=self.kwargs["pk"])
		new_react = ItemReaction.objects.create(item=item, created=timezone.now(), emoji=emoji, reactor=request.user)
		new_react.notification_react(request.user)
		html = render_to_string("generic/posts/emoji.html",{'react': new_react,'request': request})
		return JsonResponse(html, safe=False)


class ItemReactUserDelete(View):
	model=ItemReaction

	def post(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		emoji = Emoji.objects.get(pk=self.kwargs["pk"])
		new_react = ItemReaction.objects.get(item=item, emoji=emoji, reactor=request.user)
		new_react.delete()
		html = render_to_string("generic/posts/emoji.html",{'react': new_react,'request': request})
		return JsonResponse(html, safe=False)


class ItemCommentReactUserCreate(View):
	model=ItemReaction

	def post(self,request,*args,**kwargs):
		item_comment = ItemComment.objects.get(item__uuid=self.kwargs["uuid"])
		emoji = Emoji.objects.get(pk=self.kwargs["pk"])
		new_react = ItemCommentReaction.objects.create(item_comment=item_comment, created=timezone.now(), emoji=emoji, reactor=request.user)
		new_react.notification_comment_react(request.user)
		html = render_to_string("generic/posts/comment_emoji.html",{'react': new_react,'request': request})
		return JsonResponse(html, safe=False)


class ItemCommentReactUserDelete(View):
	model=ItemReaction

	def post(self,request,*args,**kwargs):
		item_comment = ItemComment.objects.get(item__uuid=self.kwargs["uuid"])
		emoji = Emoji.objects.get(pk=self.kwargs["pk"])
		react = ItemCommentReaction.objects.get(item_comment=item_comment, emoji=emoji, reactor=request.user)
		react.delete()
		html = render_to_string("generic/posts/comment_emoji.html",{'react': new_react,'request': request})
		return JsonResponse(html, safe=False)


def item_post_comment(request):
	user = request.user
	text = request.POST['text']
	img = "frtyh"
	par = request.POST['parent']
	item = Item.objects.get(pk=par)
	text = text.strip()

	if len(text) > 0:
		new_comment = ItemComment.objects.create(item=item, text=text, commenter=request.user)
		html = render_to_string('generic/posts/parent_comment.html',{'comment': new_comment,'request': request})
		return JsonResponse(html, safe=False)
	else:
		return HttpResponseBadRequest()


def item_reply_comment(request):

    user = request.user
    text = request.POST['text']
    com = request.POST['comment']
    comment = ItemComment.objects.get(pk=com)
    text = text.strip()
    if len(text) > 0:
        new_comment = ItemComment.objects.create(text=text, commenter=request.user,parent_comment=comment)
        html = render_to_string('generic/posts/reply_comment.html',{'reply': new_comment,'request': request})
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


def user_fixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=True
    item.save()
    return HttpResponse("!")


def user_unfixed(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.is_fixed=False
    item.save()
    return HttpResponse("!")

def user_item_delete(request, item_id):
	item = Item.objects.get(pk=item_id)
	if request.user == item.creator:
		item.is_deleted=True
		item.save()
		return HttpResponse("!")
	else:
		return HttpResponse("Удаляйте, пожалуйста, свои записи!")
