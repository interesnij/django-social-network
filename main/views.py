from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment, ItemReaction, ItemCommentReaction

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from main.forms import CommentForm
from django.template.loader import render_to_string
from django.views import View
from posts.models import Post
from django.views.generic import ListView
from generic.mixins import CategoryListMixin



class MainPageView(TemplateView):
	template_name=None
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name="main/mainpage.html"
		else:
			self.template_name="main/auth.html"
		return super(MainPageView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(MainPageView,self).get_context_data(**kwargs)
		return context


class ComingView(TemplateView):
	template_name="main/coming.html"


class RepostUser(View):

	def post(self, request, *args, **kwargs):
		self.item = Item.objects.get(pk=self.kwargs["pk"])
		if self.item.parent:
			new_repost = Post.objects.create(creator=request.user, parent=self.item.parent, is_repost=True)
			return HttpResponse("репост репоста")
		else:
			new_repost = Post.objects.create(creator=request.user, parent=self.item, is_repost=True)
			return HttpResponse("репост item")


class ReactView(TemplateView):
    template_name="react_window.html"

    def get(self,request,*args,**kwargs):
        self.react = Item.objects.get(pk=self.kwargs["pk"])
        self.react.notification_like(request.user)
        return super(ReactView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(ReactView,self).get_context_data(**kwargs)
        context["like"]=self.like
        return context


class CommentReactView(TemplateView):
    template_name="comment_react_window.html"

    def get(self,request,*args,**kwargs):
        self.react_like = ItemComment.objects.get(pk=self.kwargs["pk"])
        return super(CommentReactView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentReactView,self).get_context_data(**kwargs)
        context["react_like"]=self.react_like
        return context


class CommentListView(ListView, CategoryListMixin):
	template_name="generic/posts/comments.html"
	model=ItemComment
	paginate_by=10

	def get(self,request,*args,**kwargs):
		item = Item.objects.get(uuid=self.kwargs["uuid"])
		comments = ItemComment.objects.filter(item=item, parent_comment=None).order_by("created")
		comments_html = render_to_string(
	        "generic/posts/comments.html", {"comments": comments})

		return JsonResponse({
	        "comments": comments_html,
	    })

	def get_context_data(self, **kwargs):
		context = super(CommentListView, self).get_context_data(**kwargs)
		context['form_comment'] = CommentForm()
		return context


def get_comment(request):

    item_id = request.GET['item']
    item = Item.objects.get(uuid=item_id)
    form_comment = CommentForm()
    comments = ItemComment.objects.filter(item=item, parent_comment=None).order_by("created")
    comments_html = render_to_string(
        "generic/posts/comments.html", {"comments": comments,"form_comment": form_comment,"parent": item})
    return JsonResponse({
        "uuid": item_id,
        "comments": comments_html,
    })


def post_comment(request):

    user = request.user
    text = request.POST['text']
    par = request.POST['parent']
    item = Item.objects.get(pk=par)
    text = text.strip()
    if item:
        new_comment = ItemComment.objects.create(item=item, text=text, commenter=request.user)
        html = render_to_string('generic/posts/new_parent_comment.html',{'comment': new_comment,'request': request})
        return JsonResponse(html, safe=False)
    else:
        return HttpResponse("parent не найден")



def post_react(request):
	react = request.POST['emoji']
	par = request.POST['parent']
	item = Item.objects.get(pk=par)
	if item:
		new_react = ItemReaction.objects.create(item=item, emoji=react, reactor=request.user)
		html = render_to_string('generic/posts/emoji.html',{'react': new_react,'request': request})
		return JsonResponse(html, safe=False)
	else:
		return HttpResponse("react не найден")



def un_react(request):
	un_react = request.POST['emoji']
	par = request.POST['parent']
	item = Item.objects.get(pk=par)
	if item:
		un_react = ItemReaction.objects.get(item=item, emoji=un_react, reactor=request.user)
		un_react.delete()
		html = render_to_string('generic/posts/emoji.html',{'react': un_react,'request': request})
		return JsonResponse(html, safe=False)
	else:
		return HttpResponse("react не найден")



def post_comment_react(request):
	react = request.POST['emoji']
	com = request.POST['comment']
	comment = ItemComment.objects.get(pk=com)
	if comment:
		new_comment_react = ItemCommentReaction.objects.create(comment=comment, emoji=react, reactor=request.user)
		html = render_to_string('generic/posts/comment_emoji.html',{'comment_react': new_comment_react,'request': request})
		return JsonResponse(html, safe=False)
	else:
		return HttpResponse("react не найден")



def comment_un_react(request):
	un_react = request.POST['emoji']
	com = request.POST['comment']
	comment = ItemComment.objects.get(pk=com)
	if comment:
		un_react = ItemCommentReaction.objects.get(comment=comment, emoji=un_react, reactor=request.user)
		html = render_to_string('generic/posts/comment_emoji.html',{'comment_react': un_react,'request': request})
		return JsonResponse(html, safe=False)
	else:
		return HttpResponse("react не найден")


def reply_comment(request):

    user = request.user
    text = request.POST['text']
    com = request.POST['comment']
    comment = ItemComment.objects.get(pk=com)
    text = text.strip()
    if comment:
        new_comment = ItemComment.objects.create(text=text, commenter=request.user,parent_comment=comment)
        html = render_to_string('generic/posts/new_reply_comment.html',{'reply': new_comment,'request': request})
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
