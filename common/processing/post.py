
def get_post_processing(post, type):
    post.type = type
    post.save(update_fields=['type'])
    return post
def get_post_offer_processing(post):
    post.type = "_COF"
    post.save(update_fields=['type'])
    return post
def get_post_list_processing(list, type):
    list.type = type
    list.save(update_fields=['type'])
    return list

def repost_message_send(obj, attach, community, request):
    from chat.models import Message, Chat
    from users.models import User
    from posts.forms import PostForm
    from posts.models import Post
    from django.http import HttpResponse

    connections = request.POST.getlist("chat_items")

    form_post = PostForm(request.POST)
    count = 0
    if request.is_ajax() and form_post.is_valid():
        post = form_post.save(commit=False)
        repost = Post.create_parent_post(creator=obj.creator, community=community, attach=attach)
        for object_id in connections:
            if object_id[0] == "c":
                chat = Chat.objects.get(pk=object_id[1:])
                message = Message.send_message(chat=chat, repost=repost, creator=request.user, parent=None, text=post.text)
            elif object_id[0] == "u":
                user = User.objects.get(pk=object_id[1:])
                message = Message.get_or_create_chat_and_send_message(creator=request.user, repost=repost, user=user, text=post.text)

            count += 1
            obj.repost += count
            obj.save(update_fields=["repost"])
