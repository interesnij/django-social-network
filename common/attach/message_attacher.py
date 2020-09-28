from rest_framework.exceptions import ValidationError
from video.models import Video, VideoAlbum
from music.models import SoundcloudParsing, SoundList
from gallery.models import Photo, Album
from goods.models import Good, GoodAlbum
from article.models import Article
from docs.models import Doc2, DocList
from users.models import User
from communities.models import Community


def photo_attach(value, message):
    try:
        _select_photo = Photo.objects.get(uuid=value, is_public=True)
        _select_photo.message.add(message)
    except:
        raise ValidationError('Фото не найдено')

def video_attach(value, message):
    try:
        _select_video = Video.objects.get(pk=value, is_public=True)
        _select_video.message.add(message)
    except:
        raise ValidationError('Видео не найдено')

def music_attach(value, message):
    try:
        _select_music = SoundcloudParsing.objects.get(pk=value)
        _select_music.message.add(message)
    except:
        raise ValidationError('Аудиозапись не найдено')

def good_attach(value, message):
    try:
        _select_good = Good.objects.get(pk=value)
        _select_good.message.add(message)
    except:
        raise ValidationError('Товар не найден')

def article_attach(value, message):
    try:
        _select_article = Article.objects.get(uuid=value)
        _select_article.message.add(message)
    except:
        raise ValidationError('Статья не найдена')

def doc_attach(value, message):
    try:
        _select_doc = Doc2.objects.get(pk=value)
        _select_doc.message.add(message)
    except:
        raise ValidationError('Документ не найден')

def playlist_attach(value, message):
    try:
        _select_playlist = SoundList.objects.get(pk=value)
        _select_playlist.message.add(message)
    except:
        raise ValidationError('Плейлист не найден')

def doclist_attach(value, message):
    try:
        _select_doc_list = DocList.objects.get(pk=value)
        _select_doc_list.message.add(message)
    except:
        raise ValidationError('Плейлист не найден')

def photolist_attach(value, message):
    try:
        _select_photo_list = Album.objects.get(pk=value)
        _select_photo_list.message.add(message)
    except:
        raise ValidationError('Фотоальбом не найден')

def videolist_attach(value, message):
    try:
        _select_video_list = VideoAlbum.objects.get(pk=value)
        _select_video_list.message.add(message)
    except:
        raise ValidationError('Видеоальбом не найден')

def goodlist_attach(value, message):
    try:
        _select_good_list = GoodAlbum.objects.get(pk=value)
        _select_good_list.message.add(message)
    except:
        raise ValidationError('Видеоальбом не найден')


def get_message_attach(request, message):
    if request.POST.get('playlist'):
        playlist_attach(request.POST.get('playlist'), message)
    elif request.POST.get('doc_list'):
        doclist_attach(request.POST.get('doc_list'), message)
    elif request.POST.get('photo_list'):
        photolist_attach(request.POST.get('photo_list'), message)
    elif request.POST.get('video_list'):
        videolist_attach(request.POST.get('video_list'), message)
    elif request.POST.get('good_list'):
        goodlist_attach(request.POST.get('good_list'), message)
    else:
        if request.POST.get('photo'):
            if request.POST.get('select_photo1'):
                photo_attach(request.POST.get('select_photo1'), message)
            if request.POST.get('select_photo2'):
                photo_attach(request.POST.get('select_photo2'), message)
            if request.POST.get('select_photo3'):
                photo_attach(request.POST.get('select_photo3'), message)
            if request.POST.get('select_photo4'):
                photo_attach(request.POST.get('select_photo4'), message)
            if request.POST.get('select_photo5'):
                photo_attach(request.POST.get('select_photo5'), message)
            if request.POST.get('select_photo6'):
                photo_attach(request.POST.get('select_photo6'), message)
            if request.POST.get('select_photo7'):
                photo_attach(request.POST.get('select_photo7'), message)
            if request.POST.get('select_photo8'):
                photo_attach(request.POST.get('select_photo8'), message)
            if request.POST.get('select_photo9'):
                photo_attach(request.POST.get('select_photo9'), message)
            if request.POST.get('select_photo10'):
                photo_attach(request.POST.get('select_photo10'), message)

        if request.POST.get('video'):
            if request.POST.get('select_video1'):
                video_attach(request.POST.get('select_video1'), message)
            if request.POST.get('select_video2'):
                video_attach(request.POST.get('select_video2'), message)
            if request.POST.get('select_video3'):
                video_attach(request.POST.get('select_video3'), message)
            if request.POST.get('select_video4'):
                video_attach(request.POST.get('select_video4'), message)
            if request.POST.get('select_video5'):
                video_attach(request.POST.get('select_video5'), message)
            if request.POST.get('select_video6'):
                video_attach(request.POST.get('select_video6'), message)
            if request.POST.get('select_video7'):
                video_attach(request.POST.get('select_video7'), message)
            if request.POST.get('select_video8'):
                video_attach(request.POST.get('select_video8'), message)
            if request.POST.get('select_video9'):
                video_attach(request.POST.get('select_video9'), message)
            if request.POST.get('select_video10'):
                video_attach(request.POST.get('select_video10'), message)

        if request.POST.get('music'):
            if request.POST.get('select_music1'):
                music_attach(request.POST.get('select_music1'), message)
            if request.POST.get('select_music2'):
                music_attach(request.POST.get('select_music2'), message)
            if request.POST.get('select_music3'):
                music_attach(request.POST.get('select_music3'), message)
            if request.POST.get('select_music4'):
                music_attach(request.POST.get('select_music4'), message)
            if request.POST.get('select_music5'):
                music_attach(request.POST.get('select_music5'), message)
            if request.POST.get('select_music6'):
                music_attach(request.POST.get('select_music6'), message)
            if request.POST.get('select_music7'):
                music_attach(request.POST.get('select_music7'), message)
            if request.POST.get('select_music8'):
                music_attach(request.POST.get('select_music8'), message)
            if request.POST.get('select_music9'):
                music_attach(request.POST.get('select_music9'), message)
            if request.POST.get('select_music10'):
                music_attach(request.POST.get('select_music10'), message)

        if request.POST.get('good'):
            if request.POST.get('select_good1'):
                good_attach(request.POST.get('select_good1'), message)
            if request.POST.get('select_good2'):
                good_attach(request.POST.get('select_good2'), message)
            if request.POST.get('select_good3')
                good_attach(request.POST.get('select_good3'), message)
            if request.POST.get('select_good4'):
                good_attach(request.POST.get('select_good4'), message)
            if request.POST.get('select_good5'):
                good_attach(request.POST.get('select_good5'), message)
            if request.POST.get('select_good6'):
                good_attach(request.POST.get('select_good6'), message)
            if request.POST.get('select_good7'):
                good_attach(request.POST.get('select_good7'), message)
            if request.POST.get('select_good8'):
                good_attach(request.POST.get('select_good8'), message)
            if request.POST.get('select_good9'):
                good_attach(request.POST.get('select_good9'), message)
            if request.POST.get('select_good10'):
                good_attach(request.POST.get('select_good10'), message)

        if request.POST.get('article'):
            if request.POST.get('select_article1'):
                article_attach(request.POST.get('select_article1'), message)
            if request.POST.get('select_article2'):
                article_attach(request.POST.get('select_article2'), message)
            if request.POST.get('select_article3'):
                article_attach(request.POST.get('select_article3'), message)
            if request.POST.get('select_article4'):
                article_attach(request.POST.get('select_article4'), message)
            if request.POST.get('select_article5'):
                article_attach(request.POST.get('select_article5'), message)
            if request.POST.get('select_article6'):
                article_attach(request.POST.get('select_article6'), message)
            if request.POST.get('select_article7'):
                article_attach(request.POST.get('select_article7'), message)
            if request.POST.get('select_article8'):
                article_attach(request.POST.get('select_article8'), message)
            if request.POST.get('select_article9'):
                article_attach(request.POST.get('select_article9'), message)
            if request.POST.get('select_article10'):
                article_attach(request.POST.get('select_article10'), message)

        if request.POST.get('doc'):
            if request.POST.get('select_doc1'):
                doc_attach(request.POST.get('select_doc1'), message)
            if request.POST.get('select_doc2'):
                doc_attach(request.POST.get('select_doc2'), message)
            if request.POST.get('select_doc3'):
                doc_attach(request.POST.get('select_doc3'), message)
            if request.POST.get('select_doc4'):
                doc_attach(request.POST.get('select_doc4'), message)
            if request.POST.get('select_doc5'):
                doc_attach(request.POST.get('select_doc5'), message)
            if request.POST.get('select_doc6'):
                doc_attach(request.POST.get('select_doc6'), message)
            if request.POST.get('select_doc7'):
                doc_attach(request.POST.get('select_doc7'), message)
            if request.POST.get('select_doc8'):
                doc_attach(request.POST.get('select_doc8'), message)
            if request.POST.get('select_doc9'):
                doc_attach(request.POST.get('select_doc9'), message)
            if request.POST.get('select_doc10'):
                doc_attach(request.POST.get('select_doc10'), message)
