
def get_post_processing(post):
    post.status = "P"
    post.save(update_fields=['status'])
    return post

def get_post_offer_processing(post):
    post.status = "D"
    post.save(update_fields=['status'])
    return post
