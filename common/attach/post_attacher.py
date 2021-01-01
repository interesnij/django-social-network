from rest_framework.exceptions import ValidationError


def photo_attach(value, post):
    try:
        from gallery.models import Photo
        _select_photo = Photo.objects.get(pk=value, is_public=True)
        _select_photo.post.add(post)
    except:
        raise ValidationError('Фото не найдено')

def video_attach(value, post):
    try:
        from video.models import Video
        _select_video = Video.objects.get(pk=value, is_public=True)
        _select_video.post.add(post)
    except:
        raise ValidationError('Видео не найдено')

def music_attach(value, post):
    try:
        from music.models import SoundcloudParsing
        _select_music = SoundcloudParsing.objects.get(pk=value)
        _select_music.post.add(post)
    except:
        raise ValidationError('Аудиозапись не найдено')

def good_attach(value, post):
    try:
        from goods.models import Good
        _select_good = Good.objects.get(pk=value)
        _select_good.post.add(post)
    except:
        raise ValidationError('Товар не найден')

def article_attach(value, post):
    try:
        from article.models import Article
        _select_article = Article.objects.get(uuid=value)
        _select_article.post.add(post)
    except:
        raise ValidationError('Статья не найдена')

def doc_attach(value, post):
    try:
        from docs.models import Doc2
        _select_doc = Doc2.objects.get(pk=value)
        _select_doc.post.add(post)
    except:
        raise ValidationError('Документ не найден')

def playlist_attach(value, post):
    try:
        from music.models import SoundList
        _select_playlist = SoundList.objects.get(pk=value)
        _select_playlist.post.add(post)
    except:
        raise ValidationError('Плейлист не найден')

def doclist_attach(value, post):
    try:
        from docs.models import DocList
        _select_doc_list = DocList.objects.get(pk=value)
        _select_doc_list.post.add(post)
    except:
        raise ValidationError('Плейлист не найден')

def photolist_attach(value, post):
    try:
        from gallery.models import Album
        _select_photo_list = Album.objects.get(pk=value)
        _select_photo_list.post.add(post)
    except:
        raise ValidationError('Фотоальбом не найден')

def videolist_attach(value, post):
    try:
        from video.models import VideoAlbum
        _select_video_list = VideoAlbum.objects.get(pk=value)
        _select_video_list.post.add(post)
    except:
        raise ValidationError('Видеоальбом не найден')

def goodlist_attach(value, post):
    try:
        from goods.models import GoodAlbum
        _select_good_list = GoodAlbum.objects.get(pk=value)
        _select_good_list.post.add(post)
    except:
        raise ValidationError('Видеоальбом не найден')

def survey_attach(value, survey):
    try:
        from survey.models import Survey
        _select_survey = Survey.objects.get(pk=value)
        _select_survey.post.add(post)
    except:
        raise ValidationError('Опрос не найден')


def get_post_attach(request, post):
    if request.POST.get('playlist'):
        playlist_attach(request.POST.get('playlist'), post)
    elif request.POST.get('doc_list'):
        doclist_attach(request.POST.get('doc_list'), post)
    elif request.POST.get('photo_list'):
        photolist_attach(request.POST.get('photo_list'), post)
    elif request.POST.get('video_list'):
        videolist_attach(request.POST.get('video_list'), post)
    elif request.POST.get('good_list'):
        goodlist_attach(request.POST.get('good_list'), post)
    else:
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

        if request.POST.get('doc'):
            if request.POST.get('select_doc1'):
                doc_attach(request.POST.get('select_doc1'), post)
            if request.POST.get('select_doc2'):
                doc_attach(request.POST.get('select_doc2'), post)
            if request.POST.get('select_doc3'):
                doc_attach(request.POST.get('select_doc3'), post)
            if request.POST.get('select_doc4'):
                doc_attach(request.POST.get('select_doc4'), post)
            if request.POST.get('select_doc5'):
                doc_attach(request.POST.get('select_doc5'), post)
            if request.POST.get('select_doc6'):
                doc_attach(request.POST.get('select_doc6'), post)
            if request.POST.get('select_doc7'):
                doc_attach(request.POST.get('select_doc7'), post)
            if request.POST.get('select_doc8'):
                doc_attach(request.POST.get('select_doc8'), post)
            if request.POST.get('select_doc9'):
                doc_attach(request.POST.get('select_doc9'), post)
            if request.POST.get('select_doc10'):
                doc_attach(request.POST.get('select_doc10'), post)
