from django import template
register=template.Library()


@register.filter
def is_community_draft_exists(request_user, community_id):
    if request_user.get_draft_posts_of_community_with_pk(community_id):
        return True
    else:
        return False

@register.filter
def count_draft_posts_for_user(community, request_user_pk):
    return community.get_count_draft_posts_for_user(request_user_pk)
