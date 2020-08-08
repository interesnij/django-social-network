from rest_framework.exceptions import ValidationError
from video.models import Video
from music.models import SoundcloudParsing
from gallery.models import Photo
from goods.models import Good
from article.models import Article

def photo_attach(value, post):
    try:
        _select_photo = Photo.objects.get(uuid=value, is_public=True)
        _select_photo.item.add(post) 
    except:
        raise ValidationError('Фото не найдено')

def video_attach(value, post):
    try:
        _select_video = Video.objects.get(pk=value, is_public=True)
        _select_video.item.add(post)
    except:
        raise ValidationError('Видео не найдено')

def music_attach(value, post):
    try:
        _select_music = SoundcloudParsing.objects.get(pk=value)
        _select_music.item.add(post)
    except:
        raise ValidationError('Аудиозапись не найдено')

def good_attach(value, post):
    try:
        _select_good = Good.objects.get(pk=value)
        _select_good.item.add(post)
    except:
        raise ValidationError('Товар не найден')

def article_attach(value, post):
    try:
        _select_article = Article.objects.get(uuid=value)
        _select_article.item_attach.add(post)
    except:
        raise ValidationError('Статья не найдена')

def get_post_attach(request, post):
    if request.POST.get('photo'):
        if request.POST.get('select_photo1'):
            photo_attach(request.POST.get('select_photo1'), post)
        if request.POST.get('select_photo2'):
            photo_attach(request.POST.get('select_photo2'), post)
        if request.POST.get('select_photo3'):
            photo_attach(request.POST.get('select_photo3'), post)
        if request.POST.get('select_photo4'):
            photo_attach(request.POST.get('select_photo4'), post)
        if request.POST.get('select_photo5'):
            photo_attach(request.POST.get('select_photo5'), post)
        if request.POST.get('select_photo6'):
            photo_attach(request.POST.get('select_photo6'), post)
        if request.POST.get('select_photo7'):
            photo_attach(request.POST.get('select_photo7'), post)
        if request.POST.get('select_photo8'):
            photo_attach(request.POST.get('select_photo8'), post)
        if request.POST.get('select_photo9'):
            photo_attach(request.POST.get('select_photo9'), post)
        if request.POST.get('select_photo10'):
            photo_attach(request.POST.get('select_photo10'), post)

    if request.POST.get('video'):
        if request.POST.get('select_video1'):
            video_attach(request.POST.get('select_video1'), post)
        if request.POST.get('select_video2'):
            video_attach(request.POST.get('select_video2'), post)
        if request.POST.get('select_video3'):
            video_attach(request.POST.get('select_video3'), post)
        if request.POST.get('select_video4'):
            video_attach(request.POST.get('select_video4'), post)
        if request.POST.get('select_video5'):
            video_attach(request.POST.get('select_video5'), post)
        if request.POST.get('select_video6'):
            video_attach(request.POST.get('select_video6'), post)
        if request.POST.get('select_video7'):
            video_attach(request.POST.get('select_video7'), post)
        if request.POST.get('select_video8'):
            video_attach(request.POST.get('select_video8'), post)
        if request.POST.get('select_video9'):
            video_attach(request.POST.get('select_video9'), post)
        if request.POST.get('select_video10'):
            video_attach(request.POST.get('select_video10'), post)

    if request.POST.get('music'):
        if request.POST.get('select_music1'):
            music_attach(request.POST.get('select_music1'), post)
        if request.POST.get('select_music2'):
            music_attach(request.POST.get('select_music2'), post)
        if request.POST.get('select_music3'):
            music_attach(request.POST.get('select_music3'), post)
        if request.POST.get('select_music4'):
            music_attach(request.POST.get('select_music4'), post)
        if request.POST.get('select_music5'):
            music_attach(request.POST.get('select_music5'), post)
        if request.POST.get('select_music6'):
            music_attach(request.POST.get('select_music6'), post)
        if request.POST.get('select_music7'):
            music_attach(request.POST.get('select_music7'), post)
        if request.POST.get('select_music8'):
            music_attach(request.POST.get('select_music8'), post)
        if request.POST.get('select_music9'):
            music_attach(request.POST.get('select_music9'), post)
        if request.POST.get('select_music10'):
            music_attach(request.POST.get('select_music10'), post)

    if request.POST.get('good'):
        if request.POST.get('select_good1'):
            good_attach(request.POST.get('select_good1'), post)
        if request.POST.get('select_good2'):
            good_attach(request.POST.get('select_good2'), post)
        if request.POST.get('select_good3'):
            good_attach(request.POST.get('select_good3'), post)
        if request.POST.get('select_good4'):
            good_attach(request.POST.get('select_good4'), post)
        if request.POST.get('select_good5'):
            good_attach(request.POST.get('select_good5'), post)
        if request.POST.get('select_good6'):
            good_attach(request.POST.get('select_good6'), post)
        if request.POST.get('select_good7'):
            good_attach(request.POST.get('select_good7'), post)
        if request.POST.get('select_good8'):
            good_attach(request.POST.get('select_good8'), post)
        if request.POST.get('select_good9'):
            good_attach(request.POST.get('select_good9'), post)
        if request.POST.get('select_good10'):
            good_attach(request.POST.get('select_good10'), post)

    if request.POST.get('article'):
        if request.POST.get('select_article1'):
            article_attach(request.POST.get('select_article1'), post)
        if request.POST.get('select_article2'):
            article_attach(request.POST.get('select_article2'), post)
        if request.POST.get('select_article3'):
            article_attach(request.POST.get('select_article3'), post)
        if request.POST.get('select_article4'):
            article_attach(request.POST.get('select_article4'), post)
        if request.POST.get('select_article5'):
            article_attach(request.POST.get('select_article5'), post)
        if request.POST.get('select_article6'):
            article_attach(request.POST.get('select_article6'), post)
        if request.POST.get('select_article7'):
            article_attach(request.POST.get('select_article7'), post)
        if request.POST.get('select_article8'):
            article_attach(request.POST.get('select_article8'), post)
        if request.POST.get('select_article9'):
            article_attach(request.POST.get('select_article9'), post)
        if request.POST.get('select_article10'):
            article_attach(request.POST.get('select_article10'), post)
