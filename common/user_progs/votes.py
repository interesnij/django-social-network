from common.model.votes import PostVotes, PostCommentVotes
import json
from django.http import HttpResponse
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


def add_item_like(user, request_user, item, model):
    if user != request_user:
        check_user_can_get_list(request_user, user)
    try:
        likedislike = model.objects.get(parent=item, user=request_user)
        if likedislike.vote is not model.LIKE:
            likedislike.vote = model.LIKE
            likedislike.save(update_fields=['vote'])
            result = True
        else:
            likedislike.delete()
            result = False
    except model.DoesNotExist:
        model.objects.create(parent=item, user=request_user, vote=model.LIKE)
        result = True
        if request_user.pk != user.pk:
            item.notification_user_like(request_user)
    likes = item.likes_count()
    dislikes = item.dislikes_count()
    return HttpResponse(json.dumps({"result": result, "like_count": str(likes), "dislike_count": str(dislikes)}), content_type="application/json")

def add_item_dislike(user, request_user, item):
    if user != request_user:
        check_user_can_get_list(request_user, user)
    try:
        likedislike = PostVotes.objects.get(parent=item, user=request_user)
        if likedislike.vote is not PostVotes.LIKE:
            likedislike.vote = PostVotes.LIKE
            likedislike.save(update_fields=['vote'])
            result = True
        else:
            likedislike.delete()
            result = False
    except PostVotes.DoesNotExist:
        PostVotes.objects.create(parent=item, user=request_user, vote=PostVotes.LIKE)
        result = True
        if request_user.pk != user.pk:
            item.notification_user_like(request_user)
    likes = item.likes_count()
    dislikes = item.dislikes_count()
    return HttpResponse(json.dumps({"result": result, "like_count": str(likes), "dislike_count": str(dislikes)}), content_type="application/json")

def add_item_comment_like(user, request_user, comment):
    if user != request_user:
        check_user_can_get_list(request_user, user)
    try:
        likedislike = PostCommentVotes.objects.get(item=comment, user=request_user)
        if likedislike.vote is not PostCommentVotes.LIKE:
            likedislike.vote = PostCommentVotes.LIKE
            likedislike.save(update_fields=['vote'])
            result = True
        else:
            likedislike.delete()
            result = False
    except PostCommentVotes.DoesNotExist:
        PostCommentVotes.objects.create(item=comment, user=request_user, vote=PostCommentVotes.LIKE)
        result = True
        if request_user.pk != user.pk:
            comment.notification_user_comment_like(request_user)
    likes = comment.likes_count()
    dislikes = comment.dislikes_count()
    return HttpResponse(json.dumps({"result": result,"like_count": str(likes),"dislike_count": str(dislikes)}),content_type="application/json")
