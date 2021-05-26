
def get_post_processing(post, status):
    post.status = status
    post.save(update_fields=['status'])
    return post
def get_post_comment_processing(comment, status):
    comment.status = "PUB"
    comment.save(update_fields=['status'])
def get_post_list_processing(list, status):
    list.type = status
    list.save(update_fields=['type'])
    return list

def repost_message_send(list, attach, community, request, text):
    from chat.models import Message, Chat
    from common.attach.message_attach import message_attach
    from users.models import User
    from posts.forms import PostForm
    from posts.models import Post
    from django.http import HttpResponse, HttpResponseBadRequest

    connections = request.POST.getlist("chat_items")
    if not connections:
        return HttpResponseBadRequest()

    form_post = PostForm(request.POST)
    if request.is_ajax() and form_post.is_valid():
        post = form_post.save(commit=False)
        repost = Post.create_parent_post(creator=list.creator, community=community, attach=attach)
        for object_id in connections:
            if object_id[0] == "c":
                chat = Chat.objects.get(pk=object_id[1:])
                message = Message.send_message(chat=chat, repost=repost, creator=request.user, parent=None, text=text)
                message_attach(request.POST.getlist('attach_items'), message)
            elif object_id[0] == "u":
                user = User.objects.get(pk=object_id[1:])
                message = Message.get_or_create_chat_and_send_message(creator=request.user, repost=repost, user=user, text=text)
                message_attach(request.POST.getlist('attach_items'), message)
            else:
                return HttpResponse("not ok")
