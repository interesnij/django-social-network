from rest_framework.exceptions import ValidationError
from video.models import Video
from music.models import SoundcloudParsing
from gallery.models import Photo
from goods.models import Good
from main.models import Item

def photo_attach(value):
    try:
        _select_photo = Photo.objects.get(uuid=value, is_public=True)
        _select_photo.item.add(comment)
    except:
        raise ValidationError('Фото не найдено')

def video_attach(value):
    try:
        _select_video = Video.objects.get(pk=value, is_public=True)
        _select_video.item.add(comment)
    except:
        raise ValidationError('Видео не найдено')

def music_attach(value):
    try:
        _select_music = SoundcloudParsing.objects.get(pk=value)
        _select_music.item.add(comment)
    except:
        raise ValidationError('Аудиозапись не найдено')

def good_attach(value):
    try:
        _select_good = Good.objects.get(pk=value)
        _select_good.item.add(comment)
    except:
        raise ValidationError('Товар не найден')

def article_attach(value):
    try:
        _select_article = Item.objects.get(uuid=value)
        _select_article.item_attach.add(comment)
    except:
        raise ValidationError('Статья не найдена')

def get_post_attach(request):
    if request.POST.get('photo'):
        if request.POST.get('select_photo1'):
            photo_attach(select_photo1)
        if request.POST.get('select_photo2'):
            photo_attach(select_photo2)
        if request.POST.get('select_photo3'):
            photo_attach(select_photo3)
        if request.POST.get('select_photo4'):
            photo_attach(select_photo4)
        if request.POST.get('select_photo5'):
            photo_attach(select_photo5)
        if request.POST.get('select_photo6'):
            photo_attach(select_photo6)
        if request.POST.get('select_photo7'):
            photo_attach(select_photo7)
        if request.POST.get('select_photo8'):
            photo_attach(select_photo8)
        if request.POST.get('select_photo9'):
            photo_attach(select_photo9)
        if request.POST.get('select_photo10'):
            photo_attach(select_photo10)

    if request.POST.get('video'):
        if request.POST.get('select_video1'):
            video_attach(select_video1)
        if request.POST.get('select_video2'):
            video_attach(select_video2)
        if request.POST.get('select_video3'):
            video_attach(select_video3)
        if request.POST.get('select_video4'):
            video_attach(select_video4)
        if request.POST.get('select_video5'):
            video_attach(select_video5)
        if request.POST.get('select_video6'):
            video_attach(select_video6)
        if request.POST.get('select_video7'):
            video_attach(select_video7)
        if request.POST.get('select_video8'):
            video_attach(select_video8)
        if request.POST.get('select_video9'):
            video_attach(select_video9)
        if request.POST.get('select_video10'):
            video_attach(select_video10)

    if request.POST.get('music'):
        if request.POST.get('select_music1'):
            music_attach(select_music1)
        if request.POST.get('select_music2'):
            music_attach(select_music2)
        if request.POST.get('select_music3'):
            music_attach(select_music3)
        if request.POST.get('select_music4'):
            music_attach(select_music4)
        if request.POST.get('select_music5'):
            music_attach(select_music5)
        if request.POST.get('select_music6'):
            music_attach(select_music6)
        if request.POST.get('select_music7'):
            music_attach(select_music7)
        if request.POST.get('select_music8'):
            music_attach(select_music8)
        if request.POST.get('select_music9'):
            music_attach(select_music9)
        if request.POST.get('select_music10'):
            music_attach(select_music10)

    if request.POST.get('good'):
        if request.POST.get('select_good1'):
            music_attach(select_good1)
        if request.POST.get('select_good2'):
            music_attach(select_good2)
        if request.POST.get('select_good3'):
            music_attach(select_good3)
        if request.POST.get('select_good4'):
            music_attach(select_good4)
        if request.POST.get('select_good5'):
            music_attach(select_good5)
        if request.POST.get('select_good6'):
            music_attach(select_good6)
        if request.POST.get('select_good7'):
            music_attach(select_good7)
        if request.POST.get('select_good8'):
            music_attach(select_good8)
        if request.POST.get('select_good9'):
            music_attach(select_good9)
        if request.POST.get('select_good10'):
            music_attach(select_good10)

    if request.POST.get('article'):
        if request.POST.get('select_article1'):
            article_attach(select_article1)
        if request.POST.get('select_article2'):
            article_attach(select_article2)
        if request.POST.get('select_article3'):
            article_attach(select_article3)
        if request.POST.get('select_article4'):
            article_attach(select_article4)
        if request.POST.get('select_article5'):
            article_attach(select_article5)
        if request.POST.get('select_article6'):
            article_attach(select_article6)
        if request.POST.get('select_article7'):
            article_attach(select_article7)
        if request.POST.get('select_article8'):
            article_attach(select_article8)
        if request.POST.get('select_article9'):
            article_attach(select_article9)
        if request.POST.get('select_article10'):
            article_attach(select_article10)
