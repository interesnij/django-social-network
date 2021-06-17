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
    MAIN, LIST, MANAGER, PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    DELETED, DELETED_PRIVATE, DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    CLOSED, CLOSED_PRIVATE, CLOSED_MAIN, CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PROCESSING, 'Обработка'),
        (DELETED, 'Удалённый'),(DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='doc_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doc_lists_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=PROCESSING, verbose_name="Тип списка")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"

    def add_in_community_collections(self, community):
        from communities.model.list import CommunityDocListPosition
        CommunityDocListPosition.objects.create(community=community.pk, list=self.pk, position=DocList.get_community_lists_count(community.pk))
        self.communities.add(community)
    def remove_in_community_collections(self, community):
        from communities.model.list import CommunityDocListPosition
        CommunityDocListPosition.objects.get(community=community.pk, list=self.pk).delete()
        self.communities.remove(user)
    def add_in_user_collections(self, user):
        from users.model.list import UserDocListPosition
        UserDocListPosition.objects.create(user=user.pk, list=self.pk, position=DocList.get_user_lists_count(user.pk))
        self.users.add(user)
    def remove_in_user_collections(self, user):
        from users.model.list import UserDocListPosition
        UserDocListPosition.objects.get(user=user.pk, list=self.pk).delete()
        self.users.remove(user)

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            list = DocList.objects.create(community=instance, type=DocList.MAIN, name="Основной список", creator=instance.creator)
            from communities.model.list import CommunityDocListPosition
            CommunityDocListPosition.objects.create(community=instance.pk, list=list.pk, position=1)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            list = DocList.objects.create(creator=instance, type=DocList.MAIN, name="Основной список")
            from users.model.list import UserDocListPosition
            UserDocListPosition.objects.create(user=instance.pk, list=list.pk, position=1)

    def is_item_in_list(self, item_id):
        return self.doc_list.filter(pk=item_id).values("pk").exists()

    def is_not_empty(self):
        return self.doc_list.exclude(type__contains="_").values("pk").exists()

    def get_staff_items(self):
        return self.doc_list.exclude(type__contains="_")
    def get_items(self):
        return self.doc_list.filter(type="PUB")
    def get_manager_items(self):
        return self.doc_list.filter(type="MAN")
    def count_items(self):
        return self.doc_list.exclude(type__contains="_").values("pk").count()

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
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
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_open(self):
        return self.type[0] != "_"
    def is_have_edit(self):
        return self.is_list() or self.is_private()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(Q(type="MAI")&Q(creator_id=user_pk)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type="MAI")&Q(creator_id=user_pk)), Q.AND)
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(community_id=community_pk)|Q(communities__id=community_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(Q(type="MAI")&Q(community_id=community_pk)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(community_id=community_pk)|Q(communities__id=community_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        query.add(~Q(Q(type="MAI")&Q(community_id=community_pk)), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(community_id=community_pk)|Q(communities__id=community_pk)
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.doc import get_doc_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description,community=community)
        if community:
            from communities.model.list import CommunityDocListPosition
            CommunityDocListPosition.objects.create(community=community.pk, list=list.pk, position=DocList.get_community_lists_count(community.pk))
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="DOL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_doc_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_doc_list_notify")
        else:
            from users.model.list import UserDocListPosition
            UserDocListPosition.objects.create(user=creator.pk, list=list.pk, position=DocList.get_user_lists_count(creator.pk))
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="DOL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_doc_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="POL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_doc_list_notify")
        get_doc_list_processing(list, DocList.LIST)
        return list
    def edit_list(self, name, description, is_public):
        from common.processing.doc import get_doc_list_processing

        self.name = name
        self.description = description
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

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocList.DELETED
        elif self.type == "PRI":
            self.type = DocList.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = DocList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
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
            self.type = DocList.CLOSED
        elif self.type == "MAI":
            self.type = DocList.CLOSED_MAIN
        elif self.type == "PRI":
            self.type = DocList.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = DocList.CLOSED_MANAGER
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
    PROCESSING, PUBLISHED, PRIVATE, MANAGER, DELETED, CLOSED = '_PRO','PUB','PRI','MAN','_DEL','_CLO'
    DELETED_PRIVATE, DELETED_MANAGER, CLOSED_PRIVATE, CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    BOOK, ARTICLE, PUBLIC, FILE, OTHER = 'BOO','ART','PU','FIL','OTH'
    TYPE = (
        (PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_PRIVATE, 'Удалённый приватный'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_PRIVATE, 'Закрытый приватный'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    TYPE_2 = (
        (BOOK, 'Книга'),(ARTICLE, 'Статья'),(PUBLIC, 'Заметка'),(FILE, 'Файл'),(OTHER, 'Другое'),
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, validators=[validate_file_extension], verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ForeignKey(DocList, on_delete=models.SET_NULL, related_name='doc_list', blank=True, null=True)
    type = models.CharField(choices=TYPE, default=PROCESSING, max_length=5)
    type_2 = models.CharField(choices=TYPE_2, default=PROCESSING, max_length=5)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='doc_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_lists(self):
        return self.list.only("pk")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] != "_"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"

    def get_mime_type(self):
        import magic

        file = self.file
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type

    @classmethod
    def create_doc(cls, creator, title, file, list, is_public, community, type_2):
        from common.processing.doc import get_doc_processing

        _list = DocList.objects.get(pk=list)

        _list.count += 1
        _list.save(update_fields=["count"])
        doc = cls.objects.create(creator=creator,order=_list.count,title=title,list=_list,file=file,community=community, type_2=type_2)
        if not list.is_private() and is_public:
            get_doc_processing(doc, Doc.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="DOC", object_id=doc.pk, verb="ITE")
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
        if community:
            community.plus_docs(1)
        else:
            creator.plus_docs(1)
        return doc

    def edit_doc(self, title, list, file, is_public):
        from common.processing.doc  import get_doc_processing

        if self.list.pk != list.pk:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
            list.count += 1
            list.save(update_fields=["count"])
        self.title = title
        self.list = list
        self.file = file
        if is_public:
            get_doc_processing(self, Doc.PUBLISHED)
            self.make_publish()
        else:
            get_doc_processing(self, Doc.PRIVATE)
            self.make_private()
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Doc.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Doc.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.DELETED
        elif self.type == "PRI":
            self.type = Doc.DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = Doc.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Doc.PUBLISHED
        elif self.type == "_DELP":
            self.type = Doc.PRIVATE
        elif self.type == "_DELM":
            self.type = Doc.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.CLOSED
        elif self.type == "PRI":
            self.type = Doc.CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = Doc.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Doc.PUBLISHED
        elif self.type == "_CLOP":
            self.type = Doc.PRIVATE
        elif self.type == "_CLOM":
            self.type = Doc.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
