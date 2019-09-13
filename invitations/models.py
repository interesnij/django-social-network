from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import six
from main.models import Badge


class UserInvite(models.Model):
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invited_users',null=True, blank=True,verbose_name="Кого приглашает")
    created = models.DateTimeField(default=timezone.now, null=False, blank=False,verbose_name="Приглашение создано")
    #created_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,verbose_name="Кто приглашает")
    name = models.CharField(max_length=35, null=True, blank=True)
    nickname = models.CharField(max_length=35, null=True, blank=True)
    email = models.EmailField(null=True, blank=True,verbose_name="Емаил")
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
    badge = models.ForeignKey(Badge, blank=True, null=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length=255, unique=True)
    is_invite_email_sent = models.BooleanField(default=False)


    def __str__(self):
        return 'UserInvite'
