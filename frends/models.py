from django.db import models
from django.conf import settings


class Connect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='connections',verbose_name="Инициатор перевода из подписчика в друзья")
    target_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targeted_connections', null=False,verbose_name="Кого переводит из подписчика в друзья")
    target_connection = models.OneToOneField('self', on_delete=models.CASCADE, null=True,blank=True, verbose_name="Связь")

    @classmethod
    def create_connection(cls, user_id, target_user_id):
        target_connection = cls.objects.create(user_id=target_user_id, target_user_id=user_id)
        connection = cls.objects.create(user_id=user_id, target_user_id=target_user_id,
                                        target_connection=target_connection)
        target_connection.target_connection = connection
        target_connection.save()
        connection.save()
        return connection
