# Generated by Django 3.2 on 2021-04-30 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='type',
            field=models.CharField(choices=[('LIS', 'Пользовательский'), ('PRI', 'Приватный'), ('MAN', 'Созданный персоналом'), ('_PRO', 'Обработка'), ('_FIX', 'Закреплённый'), ('_DEL', 'Удалённый'), ('_DELP', 'Удалённый приватный'), ('_DELM', 'Удалённый менеджерский'), ('_CLO', 'Закрытый менеджером'), ('_CLOP', 'Закрытый приватный'), ('_CLOM', 'Закрытый основной'), ('_CLOMA', 'Закрытый менеджерский'), ('_CLOF', 'Закрытый закреплённый')], default='_PRO', max_length=6, verbose_name='Тип чата'),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('_PRO', 'Обработка'), ('PUB', 'Опубликовано'), ('_DEL', 'Удалено'), ('PRI', 'Приватно'), ('_CLO', 'Закрыто модератором'), ('MAN', 'Созданный персоналом'), ('_DELP', 'Удалённый приватный'), ('_DELM', 'Удалённый менеджерский'), ('_CLOP', 'Закрытый приватный'), ('_CLOM', 'Закрытый менеджерский')], default='_PRO', max_length=5, verbose_name='Статус сообщения'),
        ),
    ]