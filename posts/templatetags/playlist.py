from django import template
register=template.Library()

@register.filter
def playlist_repost(post):
    return post.parent.post_soundlist.all()[0]
