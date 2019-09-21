from django.db import models
from django.conf import settings


class Connect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='connections',verbose_name="Инициатор перевода из подписчика в друзья")
    target_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targeted_connections', null=False,verbose_name="Кого переводит из подписчика в друзья")

    @classmethod
    def create_connection(cls, user_id, target_user_id):
        target_connection = cls.objects.create(user_id=target_user_id, target_user_id=user_id)
        target_connection.save()
        return target_connection

    @classmethod
    def delete_connection(cls, user_id, target_user_id):
        target_connection = cls.objects.get(user_id=target_user_id, target_user_id=user_id)
        target_connection.delete()
