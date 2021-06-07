def try_except(value):
    try:
        if value:
            return True
    except:
        return False

def safe_json(data):
    import json
    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps(data))

def check_manager_state(user):
    if not user.is_user_manager() or not user.is_community_manager() or not user.is_post_manager() or not user.is_good_manager() or not user.is_photo_manager() or not user.is_audio_manager() or not user.is_video_manager():
        user.type = 'ST'
        user.save(update_fields=['type'])

def check_supermanager_state(user):
    if not user.is_superuser_manager() or not user.is_community_supermanager() or not user.is_post_supermanager() or not user.is_good_supermanager() or not user.is_photo_supermanager() or not user.is_audio_supermanager() or not user.is_video_supermanager():
        user.type = 'ST'
        user.save(update_fields=['type'])

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
    olds_ip = IPUser.objects.create(user=user)
    response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
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
    olds_ip.ip = ip
    olds_ip.save()
    loc.save()

def get_location(request):
    import json, requests
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        olds_ip = request.user.user_ip
    except:
        from users.model.profile import IPUser
        olds_ip = IPUser.objects.create(user=request.user)

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

def update_activity(user, user_agent):
    from datetime import datetime
    import re
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(user_agent):
        user.last_activity, user.device = datetime.now(), "Ph"
        user.save(update_fields=['last_activity', 'device'])
    else:
        user.last_activity, user.device = datetime.now(), "De"
        user.save(update_fields=['last_activity', 'device'])

def get_folder(user_agent):
    import re
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(user_agent):
        return "mobile/"
    else:
        return "mobile/" 
