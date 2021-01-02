from rest_framework.exceptions import ValidationError


def comment_attach(attach_items, comment, target):
    for item in attach_items:
        if item[:3] == "pho":
            from gallery.models import Photo
            try:
                photo = Photo.objects.get(pk=item[3:], is_public=True)
                if target == "item_comment":
                    photo.item_comment.add(comment)
                elif target == "photo_comment":
                    photo.photo_comment.add(comment)
                elif target == "good_comment":
                    photo.good_comment.add(comment)
                elif target == "video_comment":
                    photo.video_comment.add(comment)
            except:
                raise ValidationError('Фото не найдено')
        elif item[:3] == "vid":
            from video.models import Video
            try:
                video = Video.objects.get(pk=item[3:], is_public=True)
                if target == "item_comment":
                    video.item_comment.add(comment)
                elif target == "photo_comment":
                    video.photo_comment.add(comment)
                elif target == "good_comment":
                    video.good_comment.add(comment)
                elif target == "video_comment":
                    video.video_comment.add(comment)
            except:
                raise ValidationError('Видео не найдено')
        elif item[:3] == "mus":
            try:
                from music.models import SoundcloudParsing
                music = SoundcloudParsing.objects.get(pk=item[3:])
                if target == "item_comment":
                    music.item_comment.add(comment)
                elif target == "photo_comment":
                    music.photo_comment.add(comment)
                elif target == "good_comment":
                    music.good_comment.add(comment)
                elif target == "video_comment":
                    music.video_comment.add(comment)
            except:
                raise ValidationError('Аудиозапись не найдено')
        elif item[:3] == "goo":
            try:
                from goods.models import Good
                good = Good.objects.get(pk=item[3:])
                if target == "item_comment":
                    good.item_comment.add(comment)
                elif target == "photo_comment":
                    good.photo_comment.add(comment)
                elif target == "good_comment":
                    good.good_comment.add(comment)
                elif target == "video_comment":
                    good.video_comment.add(comment)
            except:
                raise ValidationError('Товар не найден')
        elif item[:3] == "art":
            try:
                from article.models import Article
                article = Article.objects.get(pk=item[3:])
                article.comment_attach.add(comment)
            except:
                raise ValidationError('Статья не найдена')
