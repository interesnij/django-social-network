from django.db import models
from django.conf import settings


class Connect(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='connections',verbose_name="Инициатор перевода из подписчика в друзья")
    target_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='targeted_connections', null=False,verbose_name="Кого переводит из подписчика в друзья")
    target_connection = models.OneToOneField('self', on_delete=models.CASCADE, null=True,blank=True, verbose_name="Связь")

    @classmethod
    def connection_with_id_exists_for_user_with_id(cls, connection_id, user_id):
        count = Connect.objects.filter(id=connect_id,
                                          user_id=user_id).count()
        if count > 0:
            return True

        return False
