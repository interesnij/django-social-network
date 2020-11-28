from common.model.votes import PostVotes, PostCommentVotes
import json
from django.http import HttpResponse
from common.check.user import check_user_can_get_list
from common.check.community import check_can_get_lists


def add_item_vote(user, request_user, item):
    if user != request.user:
        check_user_can_get_list(request.user, user)
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
    likes = item.likes_count()
    dislikes = item.dislikes_count()
    return HttpResponse(json.dumps({"result": result, "like_count": str(likes), "dislike_count": str(dislikes)}), content_type="application/json")
