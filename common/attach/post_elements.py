def get_post_attach(post, user):
    block = ''
    for item in post.attach.split(","):
        if item[:3] == "pho":
            try:
                from gallery.models import Photo
                photo = Photo.objects.get(pk=item[3:], type="PUB")
                if photo.community:
                    block = ''.join([block, '<div class="photo"><div class="progressive replace image_fit_200 c_post_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
                else:
                    block = ''.join([block, '<div class="photo"><div class="progressive replace image_fit_200 u_post_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
            except:
                pass
        elif item[:3] == "vid":
            try:
                from video.models import Video
                video = Video.objects.get(pk=item[3:], type="PUB")
                if video.community:
                    block = ''.join([block, '<div class="video"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 c_post_video" video-pk="', str(video.pk), '" video-counter="0"></div></div>'])
                else:
                    block = ''.join([block, '<div class="video"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_post_video" video-pk="', str(video.pk), '" video-counter="0"></div></div>'])
            except:
                pass
        elif item[:3] == "goo":
            try:
                from goods.models import Good
                good = Good.objects.get(pk=item[3:], type="PUB")
                if good.image:
                    figure = '<figure class="background-img shadow-dark"><img class="image_fit opacity-100" src="', good.image.url, '" alt="img"></figure>'
                else:
                    figure = '<figure class="background-img shadow-dark"><svg class="image_fit svg_default opacity-100" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg>'
                if video.community:
                    block = ''.join([block, '<div class="card has-background-img c_good_detail mb-3 pointer" good-pk="', good.pk, '" data-uuid="', good.get_list_uuid, '" style="flex-basis: 100%;">', figure, '<div class="card-header"><div class="media"><div class="media-body"><h4 class="text-white mb-0">', good.title, '</h4></div></div></div><div class="card-body spantshirt"></div><div class="card-footer"><p class="small mb-1 text-success">', good.price, ' ₽</p></div></div>'])
                else:
                    block = ''.join([block, '<div class="card has-background-img u_good_detail mb-3 pointer" good-pk="', good.pk, '" data-uuid="', good.get_list_uuid, '" style="flex-basis: 100%;">', figure, '<div class="card-header"><div class="media"><div class="media-body"><h4 class="text-white mb-0">', good.title, '</h4></div></div></div><div class="card-body spantshirt"></div><div class="card-footer"><p class="small mb-1 text-success">', good.price, ' ₽</p></div></div>'])
            except:
                pass
        elif item[:3] == "mus":
            try:
                from music.models import Music
                music = Music.objects.get(pk=item[3:])
                if music.image:
                    figure = ''.join(['<figure><a class="music_list_post music_thumb pointer"><img style="width:30px;heigth:auto" src="', music.image.url, '" alt="img" /></a></figure>'])
                else:
                    figure = '<figure><a class="music_list_post music_thumb pointer"><svg fill="currentColor" style="width:30px;heigth:30px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 5h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S10 13.88 10 12.5s1.12-2.5 2.5-2.5c.57 0 1.08.19 1.5.51V5h4v2zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6z"/></svg></a></figure>'
                span_btn = ''
                if user.is_authenticated:
                    lists = ''
                    for list in user.get_playlists():
                        if list.is_item_in_list(music.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_track_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_track_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                    span_btn = ''.join([span_btn, '<span class="span_btn" style="margin-left:auto;display:flex" data-pk="', str(music.pk), '" user-pk="', str(music.creator.pk), '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 25px;">', lists, '<span class="dropdown-item u_create_music_list_track_add" style="padding-left: 30px;">В новый плейлист</span></div></span><span class="u_ucm_music_repost btn_default pointer"><svg class="svg_default" style="width:20px;height:20px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg></span></span>'])
                block = ''.join([block, '<div class="music" data-path="', music.uri, '" data-duration="', music.duration, '" style="flex-basis: auto;width:100%;position: relative;"><div class="media" music-counter="0">', figure, '<div class="media-body" style="display: flex;"><h6 class="music_list_post music_title"><a>', music.title, '</a></h6>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "doc":
            try:
                from docs.models import Doc
                doc = Doc.objects.get(pk=item[3:], type="PUB")
                span_btn = ''
                if user.is_authenticated:
                    lists = ''
                    for list in user.get_doc_lists():
                        if list.is_item_in_list(doc.pk):
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_doc_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span></span>'])
                        else:
                            lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_add_doc_in_list" style="padding-left: 30px;">', list.name, '</span></span>'])
                span_btn = ''.join([span_btn, '<span class="span_btn" doc-pk="', str(doc.pk), '" data-pk="', str(post.creator.pk), '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop" title="Добавить в плейлист"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 32px;">', lists, '<span class="dropdown-item u_create_doc_list_doc_add" style="padding-left: 30px;">В новый список</span></div></span><span class="u_ucm_doc_repost btn_default pointer" title="Поделиться"><svg class="svg_default" style="width:20px;height:20px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg></span></span>'])
                block = ''.join([block, '<div style="flex-basis: 100%;margin-bottom:10px"><div class="media" style="position: relative;"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body" style="padding: 0"><h6 class="pointer" style="width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, '</a></h6><span class="small">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
            except:
                pass
        elif item[:3] == "sur":
            try:
                from survey.models import Survey
                survey = Survey.objects.get(pk=item[3:], type="PUB")
                _class, voted, answers, creator = "", "", "", survey.creator
                if survey.commuity:
                    survey_vote = "c_survey_vote "
                    survey_detail = "c_survey_detail "
                else:
                    survey_vote = "u_survey_vote "
                    survey_detail = "u_survey_detail "
                if survey.is_time_end():
                    time = "<p>Время голосования вышло</p>"
                else:
                    time = "<p>До " + str(survey.time_end) + "</p>"
                    if user.is_authenticated and not survey.is_user_voted(user.pk):
                        _class = " pointer " + survey_vote + str(survey.is_multiple)
                if survey.image:
                    image = '<img src="' + survey.image.url + '" alt="user image">'
                else:
                    image = ""
                if survey.is_have_votes():
                    voters = '<span class="' + survey_detail + 'pointer">'
                    for user in survey.get_6_users():
                        if user.s_avatar:
                            img = '<img src="' + user.s_avatar.url + '" style="width: 40px;border-radius:40px;" alt="image">'
                        else:
                            img = '<img src="/static/images/no_img/user.jpg" style="width: 40px;border-radius:40px;" alt="image">'
                    voters += '<figure class="staked">' + img + '</figure>'
                else:
                    voters = 'Пока никто не голосовал. Станьте первым!'
                for answer in survey.get_answers():
                    if answer.is_user_voted(user.pk):
                        voted = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg>'
                    answers = ''.join([answers, '<div class="lite_color answer_style', _class, '"><div class="progress2" style="width:', str(answer.get_procent()), '%;"></div><span class="progress_span_r">', answer.text, ' - ', str(answer.get_count()), '</span><span class="progress_span_l" style="margin-left: auto;">', voted, str(answer.get_procent()), '%</span></div>'])
                block = ''.join([block, '<div style="flex: 0 0 100%;" survey-pk="', str(survey.pk), '" data-pk="', str(creator.pk), '" class="border text-center has-background-img position-relative box-shadow"><figure class="background-img">', image, '</figure><div class="container" style="list-style-type:none"><i class="figure avatar120 mr-0 fa fa-gift rounded-circle bg-none border-bottom"></i><br><h4 class="', survey_detail,  '"pointer">', survey.title, '</h4><a class="underline ajax" href="', creator.get_link(), '">', str(creator), '</a>', time, '<br>', answers, voters, '</span></div></div>'])
            except:
                pass
        elif item[:3] == "lmu":
            try:
                from music.models import SoundList
                playlist = SoundList.objects.get(pk=item[3:], type="PUB")
                if playlist.community:
                    creator, name, add, remove, repost = playlist.community, ": " + playlist.community.name, "c_add_music_list", "c_remove_music_list", "c_ucm_music_list_repost"
                else:
                    creator, name, add, remove, repost = playlist.creator, playlist.creator.get_full_name_genitive(), "u_add_music_list", "u_remove_music_list", "u_ucm_music_list_repost"
                if playlist.image:
                    image = '<img src="' + playlist.image.url + '" style="width:120px;height:120px;" alt="image">'
                else:
                    image = '<svg fill="currentColor" class="svg_default border" style="width:120px;height:120px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
                repost_svg, add_svg = '', ''
                if user.is_authenticated:
                    if playlist.is_not_empty():
                        repost_svg = '<span title="Поделиться" class="', repost, ' repost_svg btn_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg></span>'
                    if playlist.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить плейлист" class="', add, ' btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in playlist.get_users_ids():
                        add_svg = '<span title="Удалить плейлист" class="', remove, ' btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(playlist.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_music_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_music_list pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="', creator.get_link(), '">', name, '</a><br>Треков: ', str(playlist.count_items()), '</p></div><span class="playlist_share">', add_svg, repost_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "ldo":
            try:
                from docs.models import DocList
                list = DocList.objects.get(pk=item[3:], type="PUB")
                if list.community:
                    creator, name, add, remove, repost = list.community, ": " + list.community.name, "c_add_doc_list", "c_remove_doc_list", "c_ucm_doc_list_repost"
                else:
                    creator, name, add, remove, repost = list.creator, list.creator.get_full_name_genitive(), "u_add_doc_list", "u_remove_doc_list", "u_ucm_doc_list_repost"
                image = '<svg fill="currentColor" class="svg_default border" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
                repost_svg, add_svg = '', ''
                if user.is_authenticated:
                    if list.is_not_empty():
                        repost_svg = '<span title="Поделиться" class="', repost, ' repost_svg btn_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg></span>'
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список документов" class="', add, ' btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список документов" class="', remove, ' btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_doc_list pointer">', list.name, '</h6><p>Список документов <a class="ajax underline" href="', creator.get_link(), '">', name, '</a><br>Документов: ', str(list.count_items()), '</p></div><span class="playlist_share">', add_svg, repost_svg, '</span></div></div></div>'])
            except:
                pass
        elif item[:3] == "lph":
            #try:
            from gallery.models import PhotoList
            list = PhotoList.objects.get(pk=item[3:])
            if list.type[0] == "_":
                pass
            if list.community:
                creator, name, add, remove, repost = list.community, list.community.name, "c_add_photo_list", "c_remove_photo_list", "c_ucm_photo_list_repost"
            else:
                creator, name, add, remove, repost = list.creator, list.creator.get_full_name(), "u_add_photo_list", "u_remove_photo_list", "u_ucm_photo_list_repost"
            share_svg, add_svg = '', ''
            if user.is_authenticated:
                if list.is_not_empty():
                    share_svg = '<a class="col pointer ', repost, ' ">Поделиться</a>'
                if list.is_user_can_add_list(user.pk):
                    add_svg = '<a class="col pointer ', add, '">В коллекцию</a>'
                elif user.pk in list.get_users_ids():
                    add_svg = '<a class="col pointer ', remove, '">Удалить</a>'
            block = ''.join([block, '<div class="custom_color text-center has-background-img position-relative box-shadow" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '" style="width: 100%;flex-basis: 100%;"><figure class="background-img"><img src="', list.get_cover_photo(), '">"</figure><div class="container"><i class="figure avatar120 mr-0 fa fa-gift rounded-circle bg-none"></i><br><h4 class="u_load_photo_list pointer"><a>', list.name, '</a></h4><p class="lead"><a class="ajax underline" href="', creator.get_link(), '">', name, '</a></p><hr class="my-3"><a class="u_load_photo_list pointer">', list.count_items_ru(), '</a><div class="row">', share_svg, add_svg, '</div>', '</div></div>'])
            #except:
            #    pass
        elif item[:3] == "lgo":
            try:
                from goods.models import GoodList
                list = GoodList.objects.get(pk=item[3:], type="PUB")
                if list.community:
                    creator, name, add, remove, repost = list.community, list.community.name, "c_add_good_list", "c_remove_good_list", "c_ucm_good_list_repost"
                else:
                    creator, name, add, remove, repost = list.creator, list.creator.get_full_name(), "u_add_good_list", "u_remove_good_list", "u_ucm_good_list_repost"
                share, add = '', ''
                if user.is_authenticated:
                    if list.is_not_empty():
                        share = '<a class="btn btn-sm primary-gradient ', repost, '"><svg fill="#ffffff" style="width: 17px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"></path></svg></a>'
                    if list.is_user_can_add_list(user.pk):
                        add = '<a class="btn btn-sm primary-gradient ', add, '"><svg fill="#ffffff" style="width: 17px;" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></a>'
                    elif user.pk in list.get_users_ids():
                        add = '<a class="btn btn-sm primary-gradient ', remove, '"><svg fill="#ffffff" style="width: 17px;" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg></a>'
                block = ''.join([block, '<div data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '" style="padding: 7px;width: 100%;flex-basis: 100%"><div class="media mb-2"><div class="media-body"><h4 class="content-color-primary mb-0 u_load_good_list pointer"><a>', list.name, '</a></h4></div><span class="small">', share, add, '</span></div><div class="align-items-center no-gutters"><figure class="mx-auto mb-3" style="width:120px"><img class="u_load_good_list pointer image_fit_small" src="', list.get_cover(), '" style="border-radius:50%" /></figure></div><h5 class="card-title mb-2 header-color-primary text-center"><a href="', creator.get_link(), '" class="ajax underline">', name, '</a></h5><h6 class="card-subtitle header-color-secondary text-center">', list.count_items_ru(), '</h6></div>'])
            except:
                pass
        elif item[:3] == "lvi":
            try:
                from video.models import VideoList
                list = VideoList.objects.get(pk=item[3:], type="PUB")
                if list.community:
                    creator, name, add, remove, repost = list.community, ": " + list.community.name, "c_add_video_list", "c_remove_video_list", "c_ucm_video_list_repost"
                else:
                    creator, name, add, remove, repost = list.creator, list.creator.get_full_name_genitive(), "u_add_video_list", "u_remove_video_list", "u_ucm_video_list_repost"
                image = '<svg fill="currentColor" class="svg_default border" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
                repost_svg, add_svg = '', ''
                if user.is_authenticated:
                    if list.is_not_empty():
                        repost_svg = '<span title="Поделиться" class="', repost, ' repost_svg btn_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg></span>'
                    if list.is_user_can_add_list(user.pk):
                        add_svg = '<span title="Добавить список видеозаписей" class="', add, ' btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span>'
                    elif user.pk in list.get_users_ids():
                        add_svg = '<span title="Удалить список видеозаписей" class="', remove, ' btn_default"><svg fill="currentColor" class="svg_default add_svg" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg></span>'
                block = ''.join([block, '<div style="flex-basis: 100%;" class="card"><div class="card-body" data-pk="', str(creator.pk), '" data-uuid="', str(list.uuid), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_video_list pointer">', list.name, '</h6><p>Список видеозаписей <a class="ajax underline" href="', creator.get_link(), '">', name, '</a><br>Видеозаписей: ', str(list.count_items()), '</p></div><span class="playlist_share">', add_svg, repost_svg, '</span></div></div></div>'])
            except:
                pass
        return ''.join(["<div class='attach_container'>", block, "</div>"])
