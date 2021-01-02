from posts.models import Post
from django.http import HttpResponse, HttpResponseBadRequest
from posts.forms import PostForm


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

def repost_community_send(list, status, community, request):
    from common.attach.post_attach import post_attach

    communities = request.POST.getlist("communities")
    lists = request.POST.getlist("lists")
    if not communities:
        return HttpResponseBadRequest()
    form_post = PostForm(request.POST)
    if request.is_ajax() and form_post.is_valid():
        post = form_post.save(commit=False)
        parent = Post.create_parent_post(creator=list.creator, community=community, status=status)
        list.post.add(parent)
        for community_id in communities:
            if request.user.is_staff_of_community(community_id):
                new_post = post.create_post(creator=request.user, text=post.text, category=post.category, lists=lists, community_id=community_id, parent=parent, comments_enabled=post.comments_enabled, is_signature=post.is_signature, votes_on=post.votes_on, status="PG")
                get_post_processing(new_post)
                post_attach(request.POST.getlist('attach_items'), new_post)

def repost_message_send(list, status, community, request, text):
    from chat.models import Message, Chat
    from common.attach.message_attach import message_attach
    from users.models import User

    connections = request.POST.getlist("chat_items")
    if not connections:
        return HttpResponseBadRequest()

    form_post = PostForm(request.POST)
    if request.is_ajax() and form_post.is_valid():
        post = form_post.save(commit=False)
        repost = Post.create_parent_post(creator=list.creator, community=community, status=status)
        list.post.add(parent)
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
