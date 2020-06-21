from rest_framework.exceptions import ValidationError
from video.models import Video
from music.models import SoundcloudParsing
from gallery.models import Photo
from goods.models import Good
from article.models import Article

def photo_attach(value, comment):
    try:
        _select_photo = Photo.objects.get(uuid=value, is_public=True)
        _select_photo.photo_comment.add(comment)
    except:
        raise ValidationError('Фото не найдено')

def video_attach(value, comment):
    try:
        _select_video = Video.objects.get(pk=value, is_public=True)
        _select_video.item_comment.add(comment)
    except:
        raise ValidationError('Видео не найдено')

def music_attach(value, comment):
    try:
        _select_music = SoundcloudParsing.objects.get(pk=value)
        _select_music.item_comment.add(comment)
    except:
        raise ValidationError('Аудиозапись не найдено')

def get_comment_attach(request, comment):
    if request.POST.get('photo'):
        if request.POST.get('select_photo1'):
            photo_attach(request.POST.get('select_photo1'), comment)
        if request.POST.get('select_photo2'):
            photo_attach(request.POST.get('select_photo2'), comment)

    if request.POST.get('video'):
        if request.POST.get('select_video1'):
            video_attach(request.POST.get('select_video1'), comment)
        if request.POST.get('select_video2'):
            video_attach(request.POST.get('select_video2'), comment)

    if request.POST.get('music'):
        if request.POST.get('select_music1'):
            music_attach(request.POST.get('select_music1'), comment)
        if request.POST.get('select_music2'):
            music_attach(request.POST.get('select_music2'), comment)
