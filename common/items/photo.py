
def u_photo(user, value):
    #try:
    from gallery.models import Photo
    photo = Photo.objects.get(pk=value, status="PUB")
    return ''.join('<div class="photo"><div class="progressive replace image_fit u_' + photo.get_type() + '_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
    #except:
    #    return ''

def c_photo(user, value):
    try:
        from gallery.models import Photo
        photo = Photo.objects.get(pk=value, status="PUB")
        return ''.join(['<div class="photo"><div class="progressive replace image_fit c_' + photo.get_type() + '_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
    except:
        return ''

def get_photo(user, notify):
    if notify.verb == "ITE":
        if notify.community:
            return '<p style="padding-left: 7px;">Сообщество <a href="' + notify.community.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
            notify.community.name + '</a> обновило аватар' + c_photo(user, notify.object_id)
        else:
            return '<p style="padding-left: 7px;">У <a href="' + notify.creator.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
            notify.creator.get_full_name_genitive() + '</a> новый аватар' + u_photo(user, notify.object_id)
    elif notify.verb == "ITS":
        if notify.is_have_object_set():
            photos, set = '', notify.get_object_set()
            if notify.community:
                for img in set:
                    photos = ''.join([photos, c_photo(user, notify.object_id)])
                return ''.join(['<p style="padding-left: 7px;">Сообщество <a href="', notify.community.get_link(), '" class="ajax" style="font-weight: bold;">',\
                notify.community.name, '</a> разместило новые фото </p><div class="attach_container">', photos, "</div>"])
            else:
                for img in set:
                    photos = ''.join([photos, u_photo(user, notify.object_id)])
                return ''.join(['<p style="padding-left: 7px;">У <a href="', notify.creator.get_link(), '" class="ajax" style="font-weight: bold;">',\
                notify.creator.get_full_name_genitive(), '</a> новые фото </p><div class="attach_container">', photos, "</div>"])
        else:
            if notify.community:
                return '<p style="padding-left: 7px;">Сообщество <a href="' + notify.community.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
                notify.community.name + '</a> разместило новое фото' + c_photo(user, notify.object_id)
            else:
                return '<p style="padding-left: 7px;">У <a href="' + notify.creator.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
                notify.creator.get_full_name_genitive() + '</a> новое фото' + u_photo(user, notify.object_id)
    else:
        if notify.is_have_object_set():
            first_notify = notify.get_first_object_set()
            return '<p style="padding-left: 7px;"><a href="' + first_notify.creator.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
            first_notify.creator.get_full_name() + '</a> и ещё ' + str(notify.count_object_set()) + first_notify.get_verb_display()\
             + ' фотографию </p>' + post(user, notify.object_id)
        else:
            return '<p style="padding-left: 7px;"><a href="' + notify.creator.get_link() + '" class="ajax" style="font-weight: bold;">'+ \
            notify.creator.get_full_name() + '</a>' + notify.get_verb_display()\
             + ' фотографию </p>' + post(user, notify.object_id)
