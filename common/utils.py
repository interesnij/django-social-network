def try_except(value):
    try:
        if value:
            return True
    except:
        return False

def hide_text(text):
    words = text.split(" ")
    words_count = len(words)
    if words_count <= 30:
        return text
    elif words_count > 30:
        word = words[30]
        return text.partition(word)[0] + "<br><a class='pointer show_post_text'>Показать полностью...</a><br><span style='display:none'>" + text[text.find(word):] + "</span>"

def safe_json(data):
    import json
    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps(data))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_first_location(request, user):
    import json, requests
    from users.model.profile import UserLocation
    from users.model.profile import IPUser

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    olds_ip = IPUser.objects.create(user=user, ip=ip)
    try:
        response = requests.get(url= "http://api.sypexgeo.net/J5O6d/json/" + ip)
        data = response.json()
        loc = UserLocation.objects.create(user=user)
        sity = data['city']
        region = data['region']
        country = data['country']
        loc.city_ru = sity['name_ru']
        loc.city_en = sity['name_en']
        loc.city_lat = sity['lat']
        loc.city_lon = sity['lon']
        loc.region_ru = region['name_ru']
        loc.region_en = region['name_en']
        loc.country_ru = country['name_ru']
        loc.country_en = country['name_en']
        loc.phone = country['phone']
        loc.save()
    except:
        pass

def get_location(request):
    import json, requests
    from users.model.profile import IPUser

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')


    olds_ip = IPUser.objects.create(user=request.user, ip=ip)

    if not olds_ip.ip:
        response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
        data = response.json()
        try:
            loc = request.user.user_location
        except:
            from users.model.profile import UserLocation
            loc = UserLocation.objects.create(user=request.user)
        sity = data['city']
        region = data['region']
        country = data['country']
        loc.city_ru = sity['name_ru']
        loc.city_en = sity['name_en']
        loc.city_lat = sity['lat']
        loc.city_lon = sity['lon']
        loc.region_ru = region['name_ru']
        loc.region_en = region['name_en']
        loc.country_ru = country['name_ru']
        loc.country_en = country['name_en']
        loc.phone = country['phone']
        olds_ip.ip = ip
        olds_ip.save()
        loc.save()
    else:
        pass

def get_mf_ages(users):
    from users.model.profile import UserLocation
    from collections import Counter

    if not users:
        return '<div><h5 class="mt-4 mb-2" style="margin:10px">Статистических данных пока нет.</h5></div>'
    sities, countries, _sities, _countries = [], [], '', ''
    comp, mob = 0, 0
    m_18, f_18, m_18_21, f_18_21, m_21_24, f_21_24, m_24_27, f_24_27, m_27_30, f_27_30, m_30_35, f_30_35, m_35_45, f_35_45, m_45, f_45 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for user in users:
        if user.device == "Ph":
            mob += 1
        else:
            comp += 1
        try:
            loc =  UserLocation.objects.filter(user_id=user.pk).last()
            country = loc.country_ru
            city = loc.city_ru
            countries, sities = countries + [country], sities + [city]
        except:
            countries, sities = countries + ["Страна не известна"], sities + ["Город не известен"]
        age = user.calculate_age()
        if user.is_men():
            if age < 18:
                m_18 += 1
            elif age >= 18 and age < 21:
                m_18_21 += 1
            elif age >= 21 and age < 24:
                m_21_24 += 1
            elif age >= 24 and age < 27:
                m_24_27 += 1
            elif age >= 27 and age < 30:
                m_27_30 += 1
            elif age >= 30 and age < 35:
                m_30_35 += 1
            elif age >= 35 and age < 45:
                m_35_45 += 1
            elif age >= 45:
                m_45 += 1
        elif user.is_women():
            if age < 18:
                f_18 += 1
            elif age >= 18 and age < 21:
                f_18_21 += 1
            elif age >= 21 and age < 24:
                f_21_24 += 1
            elif age >= 24 and age < 27:
                f_24_27 += 1
            elif age >= 27 and age < 30:
                f_27_30 += 1
            elif age >= 30 and age < 35:
                f_30_35 += 1
            elif age >= 35 and age < 45:
                f_35_45 += 1
            elif age >= 45:
                f_45 += 1
    dict_sities, dict_countries = Counter(sities), Counter(countries)
    for key, value in dict_countries.items():
        _countries = ''.join([_countries, '<div class="stat_city"><span class="city">' , key, '</span><span class="count">' , str(value), '</span></div>'])
    for key, value in dict_sities.items():
        _sities = ''.join([_sities, '<div class="stat_city"><span class="city">' , key, '</span><span class="count">' , str(value), '</span></div>'])
    return ''.join(['<div><h5 class="mt-1 mb-2" style="margin:10px">Страны</h5>', _countries, '</div> <div><h5 class="mt-1 mb-2" style="margin:10px">Города</h5>', _sities, '</div> <div><h5 class="mt-4 mb-2" style="margin:10px">Охват устройств</h5><div class="stat_city"><span class="city">Просмотры с мобильного</span><span class="count">', str(mob), '</span></div><div class="stat_city"><span class="city">Просмотры с компьютера</span><span class="count">', str(comp), '</span></div></div> <div><h5 class="mt-4 mb-2" style="margin:10px">Возраст / Пол</h5><div class="stat_city"><span class="city">До 18 лет</span><span class="count">Муж. ', str(m_18), ' | Жен. ', str(f_18), '</span></div><div class="stat_city"><span class="city">От 18 до 21 года</span><span class="count">Муж. ', str(m_18_21), ' | Жен. ', str(f_18_21), '</span></div><div class="stat_city"><span class="city">От 21 до 24 лет</span><span class="count">Муж. ', str(m_21_24), ' | Жен. ', str(f_21_24), '</span></div><div class="stat_city"><span class="city">От 24 до 27 лет</span><span class="count">Муж. ', str(m_24_27), ' | Жен. ', str(f_24_27), '</span></div><div class="stat_city"><span class="city">От 27 до 30 лет</span><span class="count">Муж. ', str(m_27_30), ' | Жен. ', str(f_27_30), '</span></div><div class="stat_city"><span class="city">От 30 до 35 лет</span><span class="count">Муж. ', str(m_30_35), ' | Жен. ', str(f_30_35), '</span></div><div class="stat_city"><span class="city">От 35 до 45 лет</span><span class="count">Муж. ', str(m_35_45), ' | Жен. ', str(f_35_45), '</span></div><div class="stat_city"><span class="city">От 45 лет</span><span class="count">Муж. ', str(m_45), ' | Жен. ', str(f_45), '</span></div></div>'])

def create_user_models(user):
    from docs.models import DocsList
    from gallery.models import PhotoList
    from goods.models import GoodList
    from music.models import MusicList
    from posts.models import PostsList
    from video.models import VideoList
    from users.model.list import (
                                    UserPhotoListPosition,
                                    UserGoodListPosition,
                                    UserPlayListPosition,
                                    UserPostsListPosition,
                                    UserDocsListPosition,
                                    UserVideoListPosition,
                                    ListUC,
                                )
    doc_list = DocsList.objects.create(creator=user, type=DocsList.MAIN, name="Основной список")
    UserDocsListPosition.objects.create(user=user.pk, list=doc_list.pk, position=1)

    list_1 = PhotoList.objects.create(creator=user, type=PhotoList.MAIN, name="Основной альбом")
    list_2 = PhotoList.objects.create(creator=user, type=PhotoList.AVATAR, name="Фото со страницы")
    list_3 = PhotoList.objects.create(creator=user, type=PhotoList.WALL, name="Фото со стены")
    UserPhotoListPosition.objects.create(user=user.pk, list=list_1.pk, position=1)
    UserPhotoListPosition.objects.create(user=user.pk, list=list_2.pk, position=2)
    UserPhotoListPosition.objects.create(user=user.pk, list=list_3.pk, position=3)

    good_list = GoodList.objects.create(creator=user, type=GoodList.MAIN, name="Основной список")
    UserGoodListPosition.objects.create(user=user.pk, list=good_list.pk, position=1)

    post_list = PostsList.objects.create(creator=user, type=PostsList.MAIN, name="Записи")
    UserPostsListPosition.objects.create(user=user.pk, list=post_list.pk, position=1)

    music_list = MusicList.objects.create(creator=user, type=MusicList.MAIN, name="Основной список")
    UserPlayListPosition.objects.create(user=user.pk, list=music_list.pk, position=1)

    video_list = VideoList.objects.create(creator=user, type=VideoList.MAIN, name="Основной список")
    UserVideoListPosition.objects.create(user=user.pk, list=video_list.pk, position=1)

    ListUC.objects.create(type=1, owner=user.pk, name="Основной список")


def create_community_models(community):
    from docs.models import DocsList
    from gallery.models import PhotoList
    from goods.models import GoodList
    from music.models import MusicList
    from posts.models import PostsList
    from video.models import VideoList
    from communities.model.list import (
                                    CommunityPhotoListPosition,
                                    CommunityGoodListPosition,
                                    CommunityPlayListPosition,
                                    CommunityPostsListPosition,
                                    CommunityDocsListPosition,
                                    CommunityVideoListPosition,
                                )
    doc_list = DocsList.objects.create(creator=community.creator, community=community, type=DocsList.MAIN, name="Основной список")
    CommunityDocsListPosition.objects.create(community=community.pk, list=doc_list.pk, position=1)

    list_1 = PhotoList.objects.create(creator=community.creator, community=community, type=PhotoList.MAIN, name="Основной альбом")
    list_2 = PhotoList.objects.create(creator=community.creator, community=community, type=PhotoList.AVATAR, name="Фото со страницы")
    list_3 = PhotoList.objects.create(creator=community.creator, community=community, type=PhotoList.WALL, name="Фото со стены")
    CommunityPhotoListPosition.objects.create(community=community.pk, list=list_1.pk, position=1)
    CommunityPhotoListPosition.objects.create(community=community.pk, list=list_2.pk, position=2)
    CommunityPhotoListPosition.objects.create(community=community.pk, list=list_3.pk, position=3)

    good_list = GoodList.objects.create(creator=community.creator, community=community, type=GoodList.MAIN, name="Основной список")
    CommunityGoodListPosition.objects.create(community=community.pk, list=good_list.pk, position=1)

    post_list = PostsList.objects.create(creator=community.creator, community=community, type=PostsList.MAIN, name="Записи")
    CommunityPostsListPosition.objects.create(community=community.pk, list=post_list.pk, position=1)

    music_list = MusicList.objects.create(creator=community.creator, community=community, type=MusicList.MAIN, name="Основной список")
    CommunityPlayListPosition.objects.create(community=community.pk, list=music_list.pk, position=1)

    video_list = VideoList.objects.create(creator=community.creator, community=community, type=VideoList.MAIN, name="Основной список")
    CommunityVideoListPosition.objects.create(community=community.pk, list=video_list.pk, position=1)

def get_item_of_type(type):
    if type[0] == "l":
        if type[:3] == "lpo":
            from posts.models import PostsList
            return PostsList.objects.get(pk=type[3:])
        elif type[:3] == "lph":
            from gallery.models import PhotoList
            return PhotoList.objects.get(pk=type[3:])
        elif type[:3] == "lgo":
            from goods.models import GoodList
            return GoodList.objects.get(pk=type[3:])
        elif type[:3] == "lvi":
            from video.models import VideoList
            return VideoList.objects.get(pk=type[3:])
        elif type[:3] == "ldo":
            from docs.models import DocsList
            return DocsList.objects.get(pk=type[3:])
        elif type[:3] == "lmu":
            from music.models import MusicList
            return MusicList.objects.get(pk=type[3:])
        elif type[:3] == "lsu":
            from survey.models import SurveyList
            return SurveyList.objects.get(pk=type[3:])
    else:
        if type[:3] == "pos":
            from posts.models import Post
            return Post.objects.get(pk=type[3:])
        elif type[:3] == "pho":
            from gallery.models import Photo
            return Photo.objects.get(pk=type[3:])
        elif type[:3] == "goo":
            from goods.models import Good
            return Good.objects.get(pk=type[3:])
        elif type[:3] == "vid":
            from video.models import Video
            return Video.objects.get(pk=type[3:])
        elif type[:3] == "doc":
            from docs.models import Doc
            return Doc.objects.get(pk=type[3:])
        elif type[:3] == "mus":
            from music.models import Music
            return Music.objects.get(pk=type[3:])
        elif type[:3] == "sur":
            from survey.models import Survey
            return Survey.objects.get(pk=type[3:])


def get_item_with_comments(item):
    if item[:3] == "pos":
        from posts.models import Post
        return Post.objects.get(pk=item[3:])
    elif item[:3] == "pho":
        from gallery.models import Photo
        return Photo.objects.get(pk=item[3:])
    elif item[:3] == "goo":
        from goods.models import Good
        return Good.objects.get(pk=item[3:])
    elif item[:3] == "vid":
        from video.models import Video
        return Video.objects.get(pk=item[3:])

def get_comment(item):
    if item[:3] == "pos":
        from posts.models import PostComment
        return PostComment.objects.get(pk=item[3:])
    elif item[:3] == "pho":
        from gallery.models import PhotoComment
        return PhotoComment.objects.get(pk=item[3:])
    elif item[:3] == "goo":
        from goods.models import GoodComment
        return GoodComment.objects.get(pk=item[3:])
    elif item[:3] == "vid":
        from video.models import VideoComment
        return VideoComment.objects.get(pk=item[3:])
