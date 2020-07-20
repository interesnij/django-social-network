
def get_post_processing(post):
    post.status = "P"
    post.save(update_fields=['status'])
    return post
