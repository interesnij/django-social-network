from rest_framework.exceptions import ValidationError


def post_attach(attach_items, post):
    for item in attach_items:
        if item[:3] == "pho":
            from gallery.models import Photo
            try:
                photo = Photo.objects.get(pk=item[3:], is_public=True)
                photo.post.add(post)
            except:
                raise ValidationError('Фото не найдено')
        elif item[:3] == "vid":
            from video.models import Video
            try:
                video = Video.objects.get(pk=item[3:], is_public=True)
                video.post.add(post)
            except:
                raise ValidationError('Видео не найдено')
        elif item[:3] == "mus":
            try:
                from music.models import SoundcloudParsing
                music = SoundcloudParsing.objects.get(pk=item[3:])
                music.post.add(post)
            except:
                raise ValidationError('Аудиозапись не найдено')
        elif item[:3] == "goo":
            try:
                from goods.models import Good
                good = Good.objects.get(pk=item[3:])
                good.post.add(post)
            except:
                raise ValidationError('Товар не найден')
        elif item[:3] == "art":
            try:
                from article.models import Article
                article = Article.objects.get(pk=item[3:])
                article.post.add(post)
            except:
                raise ValidationError('Статья не найдена')
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(pk=item[3:])
                doc.post.add(post)
            except:
                raise ValidationError('Документ не найден')
        elif item[:3] == "sur":
            try:
                from survey.models import Survey
                survey = Survey.objects.get(pk=item[3:])
                survey.post.add(post)
            except:
                raise ValidationError('Опрос не найден')
        elif item[:3] == "lmu":
            try:
                from music.models import SoundList
                playlist = SoundList.objects.get(pk=item[3:])
                playlist.post.add(post)
            except:
                raise ValidationError('Плейлист не найден')
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                doc_list = DocList.objects.get(pk=item[3:])
                doc_list.post.add(post)
            except:
                raise ValidationError('Документ не найден')
        elif item[:3] == "lph":
            try:
                from gallery.models import Album
                photo_list = Album.objects.get(pk=item[3:])
                photo_list.post.add(post)
            except:
                raise ValidationError('Фотоальбом не найден')
        elif item[:3] == "lvi":
            try:
                from video.models import VideoAlbum
                video_list = VideoAlbum.objects.get(pk=item[3:])
                video_list.post.add(post)
            except:
                raise ValidationError('Видеоальбом не найден')
        elif item[:3] == "lgo":
            try:
                from goods.models import GoodAlbum
                good_list = GoodAlbum.objects.get(pk=item[3:])
                good_list.post.add(post)
            except:
                raise ValidationError('Подборка товаров не найдена')
