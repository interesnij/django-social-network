from django.db import models
from django.conf import settings

LIKE = 1
DISLIKE = -1
VOTES = ((DISLIKE, 'Не нравится'),(LIKE, 'Нравится'))

class PostVotes(models.Model):
    vote = models.IntegerField(default=0, verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_votes_creator", on_delete=models.CASCADE, verbose_name="Пользователь")
    parent = models.ForeignKey('posts.Post', related_name="post_votes", on_delete=models.CASCADE)

class PostCommentVotes(models.Model):
    vote = models.IntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_comment_votes_creator", on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey('posts.PostComment', on_delete=models.CASCADE)


class PhotoVotes(models.Model):
    vote = models.IntegerField(default=0, verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    parent = models.ForeignKey('gallery.Photo', on_delete=models.CASCADE)

class PhotoCommentVotes(models.Model):
    vote = models.IntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey('gallery.PhotoComment', on_delete=models.CASCADE)


class GoodVotes(models.Model):
    vote = models.IntegerField(default=0, verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    parent = models.ForeignKey('goods.Good', on_delete=models.CASCADE)

class GoodCommentVotes(models.Model):
    vote = models.IntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey('goods.GoodComment', on_delete=models.CASCADE)


class VideoVotes(models.Model):
    vote = models.IntegerField(default=0, verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    parent = models.ForeignKey('video.Video', on_delete=models.CASCADE)

class VideoCommentVotes(models.Model):
    vote = models.IntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey('video.VideoComment', on_delete=models.CASCADE)
