from rest_framework.exceptions import ValidationError
from video.models import Video
from music.models import SoundcloudParsing
from gallery.models import Album, Photo


def get_comment_attach(comment,
                        photo,
                        photo2,
                        select_photo,
                        select_photo2,
                        select_video,
                        select_video2,
                        select_music,
                        select_music2):
    if photo:
        try:
            album=Album.objects.get(creator=commenter, title="Сохраненные фото", is_generic=True, community=None)
        except:
            album=Album.objects.create(creator=commenter, title="Сохраненные фото", is_generic=True, community=None)
        _photo = Photo.objects.create(creator=commenter, file=photo,community=None,is_public=True, album=album)
        _photo.item_comment.add(comment)
    if photo2:
        try:
            album=Album.objects.get(creator=commenter, title="Сохраненные фото", is_generic=True, community=None)
        except:
            album=Album.objects.create(creator=commenter, title="Сохраненные фото", is_generic=True, community=None)
        _photo2 = Photo.objects.create(creator=commenter, file=photo2,community=None,is_public=True, album=album)
        _photo2.item_comment.add(comment)
    if select_photo:
        try:
            _select_photo = Photo.objects.get(pk=select_photo, is_public=True)
            _select_photo.item_comment.add(comment)
        except:
            raise ValidationError('Фото не найдено')
    if select_photo2:
        try:
            _select_photo2 = Photo.objects.get(pk=select_photo2, is_public=True)
            _select_photo2.item_comment.add(comment)
        except:
            raise ValidationError('Фото не найдено')
    if select_video:
        try:
            _select_video = Video.objects.get(pk=select_video, is_public=True)
            _select_video.item_comment.add(comment)
        except:
            raise ValidationError('Видео не найдено')
    if select_video2:
        try:
            _select_video2 = Video.objects.get(pk=select_video2, is_public=True)
            _select_video2.item_comment.add(comment)
        except:
            raise ValidationError('Видео не найдено')
    if select_music:
        try:
            _select_music = SoundcloudParsing.objects.get(pk=select_music)
            _select_music.item_comment.add(comment)
        except:
            raise ValidationError('Аудиозапись не найдена')
    if select_music2:
        try:
            _select_music2 = SoundcloudParsing.objects.get(pk=select_music2)
            _select_music2.item_comment.add(comment)
        except:
            raise ValidationError('Аудиозапись не найдена')
