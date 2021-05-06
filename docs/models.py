import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from docs.helpers import upload_to_doc_directory, validate_file_extension
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community
from django.db.models import Q


class DocList(models.Model):
    MAIN, LIST, MANAGER, THIS_PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='doc_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doc_lists_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип списка")
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"
        ordering = ['order']

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            DocList.objects.create(community=instance, type=DocList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            DocList.objects.create(creator=instance, type=DocList.MAIN, name="Основной список", order=0)

    def is_item_in_list(self, item_id):
        return self.doc_list.filter(pk=item_id).values("pk").exists()

    def is_not_empty(self):
        return self.doc_list.exclude(status__contains="_").values("pk").exists()

    def get_staff_items(self):
        return self.doc_list.exclude(status__contains="_")
    def get_items(self):
        return self.doc_list.filter(status="PUB")
    def get_manager_items(self):
        return self.doc_list.filter(status="MAN")
    def count_items(self):
        return self.doc_list.exclude(status__contains="_").values("pk").count()

    def get_users_ids(self):
        users = self.users.exclude(type="DE").exclude(type="BL").exclude(type="PV").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(perm="DE").exclude(perm="BL").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()

    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()

    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] != "_"

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.doc import get_doc_list_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_doc_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_doc_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="DOL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_doc_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_doc_list_notify")
        get_doc_list_processing(list, DocList.LIST)
        return list
    def edit_list(self, name, description, order, is_public):
        from common.processing.doc import get_doc_list_processing
        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_doc_list_processing(self, DocList.LIST)
            self.make_publish()
        else:
            get_doc_list_processing(self, DocList.PRIVATE)
            self.make_private()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = DocList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = DocList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocList.THIS_DELETED
        elif self.type == "PRI":
            self.type = DocList.THIS_DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = DocList.THIS_DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_list(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = DocList.LIST
        elif self.type == "_DELP":
            self.type = DocList.PRIVATE
        elif self.type == "_DELM":
            self.type = DocList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocList.THIS_CLOSED
        elif self.type == "MAI":
            self.type = DocList.THIS_CLOSED_MAIN
        elif self.type == "PRI":
            self.type = DocList.THIS_CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = DocList.THIS_CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = DocList.LIST
        elif self.type == "_CLOM":
            self.type = DocList.MAIN
        elif self.type == "_CLOP":
            self.type = DocList.PRIVATE
        elif self.type == "_CLOM":
            self.type = DocList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")


class Doc(models.Model):
    THIS_PROCESSING, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = '_PRO','PUB','PRI','MAN','_DEL','_CLO'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, validators=[validate_file_extension], verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ManyToManyField(DocList, related_name='doc_list', blank=True)
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='doc_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_lists_for_doc(self):
        return self.list.only("pk")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] != "_"

    def get_mime_type(self):
        import magic

        file = self.file
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type

    @classmethod
    def create_doc(cls, creator, title, file, lists, is_public, community):
        from common.processing.doc import get_doc_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")
        private = 0
        doc = cls.objects.create(creator=creator,title=title,file=file)
        if community:
            community.plus_docs(1)
        else:
            creator.plus_docs(1)
        for list_id in lists:
            doc_list = DocList.objects.get(pk=list_id)
            doc_list.doc_list.add(doc)
            if doc_list.is_private():
                private = 1
        if not private and is_public:
            get_doc_processing(doc, Doc.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                community_send_wall(doc.pk, creator.pk, community.pk, None, "create_c_doc_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                    community_send_notify(doc.pk, creator.pk, user_id, community.pk, None, "create_c_doc_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type="DOC", object_id=doc.pk, verb="ITE")
                user_send_wall(doc.pk, None, "create_u_doc_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                    user_send_notify(doc.pk, creator.pk, user_id, None, "create_u_doc_notify")
        else:
            get_doc_processing(doc, Doc.PRIVATE)
        return doc

    def edit_doc(self, title, file, lists, is_public):
        from common.processing.doc  import get_doc_processing

        self.title = title
        self.file = file
        self.lists = lists
        if is_public:
            get_doc_processing(self, Doc.PUBLISHED)
            self.make_publish()
        else:
            get_doc_processing(self, Doc.PRIVATE)
            self.make_private()
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Doc.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Doc.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def delete_doc(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Doc.THIS_DELETED
        elif self.status == "PRI":
            self.status = Doc.THIS_DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Doc.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def restore_doc(self, community):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = Doc.PUBLISHED
        elif self.status == "_DELP":
            self.status = Doc.PRIVATE
        elif self.status == "_DELM":
            self.status = Doc.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Doc.THIS_CLOSED
        elif self.status == "PRI":
            self.status = Doc.THIS_CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Doc.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = Doc.PUBLISHED
        elif self.status == "_CLOP":
            self.status = Doc.PRIVATE
        elif self.status == "_CLOM":
            self.status = Doc.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
