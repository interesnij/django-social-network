from django.db import models
from django.conf import settings
from notifications.models import Notification, notification_handler
from users.models import User


class Connect(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='connections', verbose_name="Инициатор перевода из подписчика в друзья")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='targeted_connections', null=False, verbose_name="Кого переводит из подписчика в друзья")
    target_connection = models.OneToOneField('self', on_delete=models.CASCADE, null=True)

    def notification_connect(self, user):
        notification_handler(user, self.target_user, Notification.CONNECTION_CONFIRMED, action_object=self, id_value=str(user.uuid), key='notification')

    @classmethod
    def create_connection(cls, user_id, target_user_id):
        target_connection = cls.objects.create(user_id=target_user_id, target_user_id=user_id)
        connection = cls.objects.create(user_id=user_id, target_user_id=target_user_id,target_connection=target_connection)
        target_connection.target_connection = connection
        target_connection.save()
        connection.save()
        target_connection.notification_connect(user_id)
        return connection

    class Meta:
        unique_together = ('user', 'target_user')
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'

    @classmethod
    def connection_exists(cls, user_a_id, user_b_id):
        count = Connect.objects.select_related('target_connection__user_id').filter(user_id=user_a_id,                                                                           target_connection__user_id=user_b_id).count()
        return count > 0

    @classmethod
    def connection_with_id_exists_for_user_with_id(cls, connection_id, user_id):
        count = Connect.objects.filter(id=connection_id,
                                          user_id=user_id).count()
        if count > 0:
            return True
        return False
