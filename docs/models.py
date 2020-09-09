from django.db import models
from django.contrib.postgres.indexes import BrinIndex
import uuid
from django.conf import settings
from docs.helpers import upload_to_doc_directory


class DocList(models.Model):
    MAIN = 'MA'
    LIST = 'LI'
    TYPE = (
        (MAIN, 'Основной список'),
        (LIST, 'Пользовательский список'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_doclist', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_doclist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=LIST, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)
    is_public = models.BooleanField(default=True, verbose_name="Виден другим")

    post = models.ManyToManyField("posts.Post", blank=True, related_name='post_doclist')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    def is_doc_in_list(self, doc_id):
        return self.doc_list.filter(pk=doc_id).values("pk").exists()

    def is_not_empty(self):
        return self.doc_list.filter(list=self).values("pk").exists()

    def get_my_docs(self):
        queryset = self.doc_list.only("pk")
        return queryset

    def get_docs(self):
        queryset = self.doc_list.filter(is_private=True)
        return queryset

    def list_30(self):
        queryset = self.doc_list.only("pk")[:30]
        return queryset

    def count_docs(self):
        return self.doc_list.filter(is_deleted=False).values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
    def is_user_list(self):
        return self.type == self.LIST

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"
        ordering = ['order']


class Doc(models.Model):
    PRIVATE = 'P'
    STUDY = 'S'
    BOOK = 'B'
    OTHER = 'O'
    TYPES = (
        (PRIVATE, 'Личный документ'),
        (STUDY, 'Учебный документ'),
        (BOOK, 'Книга'),
        (OTHER, 'Другой документ'),
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ManyToManyField(DocList, related_name='doc_list', blank="True")
    type = models.CharField(choices=TYPES, default='P', max_length=2)

    item = models.ManyToManyField("posts.Post", blank=True, related_name='item_doc')
    item_comment = models.ManyToManyField("posts.PostComment", blank=True, related_name='comment_doc')
    photo_comment = models.ManyToManyField('gallery.PhotoComment', blank=True, related_name='gallery_comment_doc')
    good_comment = models.ManyToManyField('goods.GoodComment', blank=True, related_name='good_comment_doc')
    video_comment = models.ManyToManyField('video.VideoComment', blank=True, related_name='video_comment_doc')
    message = models.ManyToManyField('chat.Message', blank=True, related_name='message_doc')

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)
