from django.db import models
from django.conf import settings
from notifications.models import Notification, notification_handler


class Connect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='connections', verbose_name="Инициатор перевода из подписчика в друзья")
    target_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targeted_connections', null=False, verbose_name="Кого переводит из подписчика в друзья")

    def notification_follow(self, user):
        notification_handler(user, self.target_user, Notification.CONNECTION_CONFIRMED, action_object=self, id_value=str(user.uuid), key='notification')

    @classmethod
    def create_connection(cls, user_id, target_user_id):
        target_connection = cls.objects.create(user_id=user_id, target_user_id=target_user_id)
        target_connection.notification_follow(user_id)
        target_connection.save()
        return target_connection
