from rest_framework.exceptions import ValidationError
from video.models import Video
from music.models import SoundcloudParsing
from gallery.models import Photo
from goods.models import Good
from article.models import Article

def photo_attach(value, comment, value):
    try:
        _select_photo = Photo.objects.get(uuid=value, is_public=True)
        if value == "item_comment":
            _select_photo.item_comment.add(comment)
        if value == "photo_comment":
            _select_photo.photo_comment.add(comment)
        if value == "good_comment":
            _select_photo.good_comment.add(comment)
        if value == "video_comment":
            _select_photo.video_comment.add(comment)
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

def good_attach(value, comment):
    try:
        _select_good = Good.objects.get(pk=value)
        _select_good.item_comment.add(comment)
    except:
        raise ValidationError('Товар не найден')

def article_attach(value, comment):
    try:
        _select_article = Article.objects.get(uuid=value)
        _select_article.comment_attach.add(comment)
    except:
        raise ValidationError('Статья не найдена')

def get_comment_attach(request, comment):
    if request.POST.get('photo'):
        if request.POST.get('select_photo1'):
            photo_attach(request.POST.get('select_photo1'), comment, "item_comment")
        if request.POST.get('select_photo2'):
            photo_attach(request.POST.get('select_photo2'), comment, "item_comment")

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

    if request.POST.get('good'):
        if request.POST.get('select_good1'):
            good_attach(request.POST.get('select_good1'), comment)
        if request.POST.get('select_good2'):
            good_attach(request.POST.get('select_good2'), comment)

    if request.POST.get('article'):
        if request.POST.get('select_article1'):
            article_attach(request.POST.get('select_article1'), comment)
        if request.POST.get('select_article2'):
            article_attach(request.POST.get('select_article2'), comment)
