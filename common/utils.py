def safe_json(data):
    import json
    from django.utils.safestring import mark_safe

    return mark_safe(json.dumps(data))

def check_manager_state(user):
    if not user.is_user_manager() or not user.is_community_manager() or not user.is_post_manager() or not user.is_good_manager() or not user.is_photo_manager() or not user.is_audio_manager() or not user.is_video_manager():
        user.is_manager = False

def check_supermanager_state(user):
    if not user.is_superuser_manager() or not user.is_community_supermanager() or not user.is_post_supermanager() or not user.is_good_supermanager() or not user.is_photo_supermanager() or not user.is_audio_supermanager() or not user.is_video_supermanager():
        user.is_supermanager = False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_first_location(request, user):
    import json, requests
    from users.model.profile import OneUserLocation
    from users.model.profile import IPUser

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    olds_ip = IPUser.objects.create(user=user)
    response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
    data = response.json()
    loc = OneUserLocation.objects.create(user=user)
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
    olds_ip.ip_1 = ip
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

    if not olds_ip.ip_1:
        response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
        data = response.json()
        try:
            loc = request.user.user_location
        except:
            from users.model.profile import OneUserLocation
            loc = OneUserLocation.objects.create(user=request.user)
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
        olds_ip.ip_1 = ip
        olds_ip.save()
        loc.save()
    elif not olds_ip.ip_2 and olds_ip.ip_3 != ip and olds_ip.ip_2 != ip and olds_ip.ip_1 != ip:
        response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
        data = response.json()
        try:
            loc = request.user.user_location_2
        except:
            from users.model.profile import TwoUserLocation
            loc = TwoUserLocation.objects.create(user=request.user)
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
        olds_ip.ip_2 = ip
        olds_ip.save()
        loc.save()
    elif not olds_ip.ip_3 and olds_ip.ip_3 != ip and olds_ip.ip_2 != ip and olds_ip.ip_1 != ip:
        response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
        data = response.json()
        try:
            loc = request.user.user_location_3
        except:
            from users.model.profile import ThreeUserLocation
            loc = ThreeUserLocation.objects.create(user=request.user)
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
        olds_ip.ip_3 = ip
        olds_ip.save()
        loc.save()
    elif olds_ip.ip_3 and olds_ip.ip_3 != ip and olds_ip.ip_2 != ip and olds_ip.ip_1 != ip:
        response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
        data = response.json()
        sity = data['city']
        region = data['region']
        country = data['country']
        loc.city_ru = sity['name_ru']
        loc.city_en = sity['name_en']
        loc.region_ru = region['name_ru']
        loc.region_en = region['name_en']
        loc.country_ru = country['name_ru']
        loc.country_en = country['name_en']
        loc.phone = country['phone']
        olds_ip.ip_1 = ip
        olds_ip.save()
        loc.save()

    else:
        pass
