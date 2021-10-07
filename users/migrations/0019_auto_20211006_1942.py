# Generated by Django 3.2 on 2021-10-06 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20210922_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprivatemusic',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprivatephoto',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprivateplanner',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprivatepost',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprivatevideo',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserPrivateGood',
        ),
        migrations.DeleteModel(
            name='UserPrivateMusic',
        ),
        migrations.DeleteModel(
            name='UserPrivatePhoto',
        ),
        migrations.DeleteModel(
            name='UserPrivatePlanner',
        ),
        migrations.DeleteModel(
            name='UserPrivatePost',
        ),
        migrations.DeleteModel(
            name='UserPrivateVideo',
        ),
    ]