from chat.models import Message, Chat
from common.attach.post_attacher import get_post_attach
from posts.forms import PostForm
from posts.models import Post
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest


def get_post_processing(post):
    post.status = "P"
    post.save(update_fields=['status'])
    return post

def get_post_message_processing(post):
    post.status = "MP"
    post.save(update_fields=['status'])
    return post

def get_post_offer_processing(post):
    post.status = "D"
    post.save(update_fields=['status'])
    return post

def repost_message_send(parent, community, request):
    connections = request.POST.getlist("chat_items")
    if not connections:
        return HttpResponseBadRequest()
    form_post = PostForm(request.POST)

    if request.is_ajax() and form_post.is_valid():
        post = form_post.save(commit=False)
        if parent.parent:
            parent = parent.parent
        else:
            parent = parent
        for object_id in connections:
            new_post = post.create_post(creator=request.user, is_signature=False, text=post.text, community=community, comments_enabled=None, parent=parent, status="PG")
            get_post_attach(request, new_post)
            get_post_message_processing(new_post)
            if object_id[0] == "c":
                chat = Chat.objects.get(pk=object_id[1:])
                message = Message.send_message(chat=chat, creator=request.user, post=new_post, parent=None, text="Репост записи сообщества")
            elif object_id[0] == "u":
                user = User.objects.get(pk=object_id[1:])
                message = Message.get_or_create_chat_and_send_message(creator=request.user, user=user, post=new_post, text="Репост записи сообщества")
            else:
                return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
