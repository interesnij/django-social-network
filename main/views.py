from django.views.generic.base import TemplateView
from users.models import User
from main.models import Item, ItemComment
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from main.forms import CommentForm
from main.helpers import ajax_required
from django.template.loader import render_to_string


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


class LikeView(TemplateView):
    template_name="like_window.html"

    def get(self,request,*args,**kwargs):
        self.like = Item.objects.get(pk=self.kwargs["pk"])
        self.like.notification_like(request.user)
        return super(LikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(LikeView,self).get_context_data(**kwargs)
        context["like"]=self.like
        return context


class CommentLikeView(TemplateView):
    template_name="comment_like_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_like = ItemComment.objects.get(pk=self.kwargs["pk"])
        return super(CommentLikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentLikeView,self).get_context_data(**kwargs)
        context["comment_like"]=self.comment_like
        return context


class DislikeView(TemplateView):
    template_name="dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.dislike = Item.objects.get(pk=self.kwargs["pk"])
        self.dislike.notification_dislike(request.user)
        return super(DislikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(DislikeView,self).get_context_data(**kwargs)
        context["dislike"]=self.dislike
        return context


class CommentDislikeView(TemplateView):
    template_name="comment_dislike_window.html"

    def get(self,request,*args,**kwargs):
        self.comment_dislike = ItemComment.objects.get(pk=self.kwargs["pk"])
        return super(CommentDislikeView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(CommentDislikeView,self).get_context_data(**kwargs)
        context["comment_dislike"]=self.comment_dislike
        return context


@login_required
@require_http_methods(["GET"])
def get_comment(request):

    item_id = request.GET['item']
    item = Item.objects.get(uuid=item_id)
    form_comment = CommentForm()
    comments = ItemComment.objects.filter(item=item, parent_comment=None).order_by("created")
    comments_html = render_to_string(
        "generic/comments.html", {"comments": comments,"form_comment": form_comment,"parent": item})
    return JsonResponse({
        "uuid": item_id,
        "comments": comments_html,
    })

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):

    user = request.user
    text = request.POST['text']
    par = request.POST['parent']
    item = Item.objects.get(pk=par)
    text = text.strip()
    if item:
        new_comment = ItemComment.objects.create(item=item, text=text, commenter=request.user)
        html = render_to_string('generic/parent_comment.html',{'comment': new_comment,'request': request})
        return JsonResponse(html, safe=False)
    else:
        return HttpResponse("parent не найден")


@login_required
@ajax_required
@require_http_methods(["POST"])
def reply_comment(request):

    user = request.user
    text = request.POST['text']
    com = request.POST['comment']
    comment = Comment.objects.get(pk=com)
    text = text.strip()
    if comment:
        new_comment = ItemComment.objects.create(text=text, commenter=request.user,parent_comment=comment)
        html = render_to_string('generic/reply_comment.html',{'reply': new_comment,'request': request})
        return JsonResponse(html, safe=False)

        notification_handler(
            user, parent.creator, Notification.ARTICLE_REPLY_COMMENT, action_object=reply_article,
            id_value=str(com.id), key='social_update')

    else:
        return HttpResponseBadRequest()


@login_required
@require_http_methods(["POST"])
def post_update_interactions(request):
    data_point = request.POST['id_value']
    item = Item.objects.get(uuid=data_point)
    data = {'likes': item.count_likers(), 'dislikes': item.count_dislikers(), 'comments': item.count_thread()}
    return JsonResponse(data)
