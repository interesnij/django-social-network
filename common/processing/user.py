from posts.models import PostList


def create_user_models(user):
    PostList.objects.create(creator=user, type=PostList.MAIN, name="Основной список", order=1)
