function get_post_view() {
    if (document.body.querySelector(".list_pk")) {
        container = document.body.querySelector(".list_pk");
        link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        list = container.querySelectorAll('.pag');
        for (var i = 0; i < list.length; i++) {
            if (!list[i].classList.contains("showed")) {
                inViewport = elementInViewport(list[i]);
                if (inViewport) {
                    try {
                        uuid = list[i].getAttribute('data-uuid');
                        if (list[i].querySelector(".reklama")) {
                            link.open('GET', '/posts/user_progs/post_market_view/' + uuid + "/", true)
                        } else if (!list[i].querySelector(".reklama")) {
                            link.open('GET', '/posts/user_progs/post_view/' + uuid + "/", true)
                        }
                    } catch {null}
                    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                    link.send();
                    list[i].classList.add("showed");
                    console.log(i + " получил класс showed")
                }
            }
        }
    }
}

function scrolled(link, block_id, target) {
    // работа с прокруткой:
    // 1. Ссылка на страницу с пагинацией
    // 2. id блока, куда нужно грузить следующие страницы
    // 3. Указатель на нужность работы просмотров элементов в ленте. Например, target=1 - просмотры постов в ленте
    onscroll = function() {
      //  try {
      console.log("paginate");
            if (document.body.querySelector(".chat_container")){
              console.log("is_chat_paginate");
              block_ = document.body.querySelector(".is_chat_paginate");
              box_ = block_.querySelector('.first');
              if (box_ && box_.classList.contains("first")) {
                console.log(box_);
                inViewport_ = elementInViewport(box_);
                if (inViewport_) {console.log("inViewport");box_.classList.remove("first");top_paginate(link, block_id)}}
            }
            else {_block = document.body.querySelector(block_id);
                  box = _block.querySelector('.last');
                  if (box && box.classList.contains("last")) {
                    inViewport = elementInViewport(box);
                    if (inViewport) {
                      box.classList.remove("last");
                      paginate(link, block_id);
                    }
                  };
                  if (target == 1) {get_post_view()}}
        //        } catch {return}
    }
};
page = 2;
loaded = false;
m_page = 2;
m_loaded = false;

function top_paginate(link, block_id) {
    // работа с прокруткой для подгрузки сообщений вверх страницы:
    // 1. Ссылка на страницу с пагинацией
    // 2. id блока, куда нужно грузить следующие страницы
    block = document.body.querySelector(block_id);
    if (block.getElementsByClassName('pag').length === (m_page - 1) * 15) {
        if (m_loaded) {return};
        var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        link_3.open('GET', link + '?page=' + m_page++, true);
        link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        link_3.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var elem = document.createElement('span');
                elem.innerHTML = link_3.responseText;
                if (elem.getElementsByClassName('pag').length < 15) {
                    m_loaded = true
                };
                if (elem.querySelector(block_id)) {
                    xxx = document.createElement("span");
                    xxx.innerHTML = elem.querySelector(block_id).innerHTML;
                    block.afterbegin('beforeend', xxx.innerHTML)
                } else {
                    block.afterbegin('beforeend', elem.innerHTML)
                }
            }
        }
        link_3.send();
    }
};

function paginate(link, block_id) {
  // общая подгрузка списков в конец указанного блока
    block = document.body.querySelector(block_id);
    if (block.getElementsByClassName('pag').length === (page - 1) * 15) {
        if (loaded) {
            return
        };
        var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        link_3.open('GET', link + '?page=' + page++, true);
        link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        link_3.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var elem = document.createElement('span');
                elem.innerHTML = link_3.responseText;
                if (elem.getElementsByClassName('pag').length < 15) {
                    loaded = true
                };
                if (elem.querySelector(block_id)) {
                    xxx = document.createElement("span");
                    xxx.innerHTML = elem.querySelector(block_id).innerHTML;
                    block.insertAdjacentHTML('beforeend', xxx.innerHTML)
                } else {
                    block.insertAdjacentHTML('beforeend', elem.innerHTML)
                }
            }
        }
        link_3.send();
    }
}

function create_load_pagination(block) {
    // подключаем пагинцию списков в подгружаемых окнах.
    if (block.querySelector('.img_load_container')) {
        _block = block.querySelector('.img_load_container');
        scrolled(_block.getAttribute("data-link"), '.img_load_container', target = 0)
    } else if (block.querySelector('.articles_load_container')) {
        _block = block.querySelector('.articles_load_container');
        scrolled(_block.getAttribute("data-link"), '.articles_load_container', target = 0)
    } else if (block.querySelector('.goods_load_container')) {
        _block = block.querySelector('.goods_load_container');
        scrolled(_block.getAttribute("data-link"), '.goods_load_container', target = 0)
    } else if (block.querySelector('.music_load_container')) {
        _block = block.querySelector('.music_load_container');
        scrolled(_block.getAttribute("data-link"), '.music_load_container', target = 0)
    } else if (block.querySelector('.music_list_load_container')) {
        _block = block.querySelector('.music_list_load_container');
        scrolled(_block.getAttribute("data-link"), '.music_list_load_container', target = 0)
    } else if (block.querySelector('.video_load_container')) {
        _block = block.querySelector('.video_load_container');
        scrolled(_block.getAttribute("data-link"), '.video_load_container', target = 0)
    }
}


function create_pagination(block) {
  if (block.querySelector('.is_paginate')) {
    scrolled(window.location.href, '.is_paginate', target = 0)
  }
  else if (block.querySelector('.is_post_paginate')) {
    scrolled(window.location.href, '.is_post_paginate', target = 1)
  }
  else if (block.querySelector('.is_chat_paginate')) {
    scrolled(window.location.href, '.is_chat_paginate', target = 0)
  }
}

function scrollToBottom(id) {
    document.querySelector(id).scrollIntoView(false);
}

function minus_one_chat() {
    if (document.body.querySelector(".new_unread_chats")) {
        unread_chats = document.body.querySelector(".new_unread_chats"),
            count = unread_chats.innerHTML,
            count * 1,
            count -= 1,
            count > 0 ? unread_chats.innerHTML = count : unread_chats.innerHTML = ""
    }
}

function minus_new_followers() {
    if (document.body.querySelector(".new_followers_bagde")) {
        new_followers = document.body.querySelector(".new_followers_bagde"),
            count = new_followers.innerHTML,
            count * 1,
            count -= 1,
            count > 0 ? new_followers.innerHTML = count : new_followers.innerHTML = ""
    }
}

function if_list(block) {
    if (block.querySelector('.is_profile_post_paginate')) {
        pk = document.body.querySelector(".tab_active").getAttribute("list-pk");
        link = "/users/detail/list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + pk + "/";
        list_block_load(block.querySelector('.is_profile_post_paginate'), ".post_stream", link);
        scrolled(link, '.list_pk', target = 1)
    } else if (block.querySelector('.is_community_post_paginate')) {
        pk = document.body.querySelector(".tab_active").getAttribute("list-pk");
        link = "/communities/list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + pk + "/";
        list_block_load(block.querySelector('.is_community_post_paginate'), ".post_stream", link);
        scrolled(link, '.list_pk', target = 1)
    } else if (block.querySelector('.is_block_post_paginate')) {
        lenta = block.querySelector('.is_block_post_paginate');
        link = lenta.getAttribute("data-link");
        list_load(lenta, link);
        scrolled(link, '.list_pk', target = 1)
    } else if (block.querySelector('.is_block_paginate')) {
        lenta = block.querySelector('.is_block_paginate');
        link = lenta.getAttribute("data-link");
        list_load(block.querySelector(".is_block_paginate"), link);
        scrolled(link, '.list_pk', target = 1)
    }
}

if_list(document.getElementById('ajax'));
create_pagination(document.getElementById('ajax'));
load_chart()

function list_load(block, link) {
    var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    request.open('GET', link, true);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {
            block.innerHTML = request.responseText;
        }
    };
    request.send(null);
}
function list_block_load(target_block, response_block, link) {
  // грузим блок response_block по ссылке link в блок target_block
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', link, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ){
        elem_ = document.createElement('span');
        elem_.innerHTML = request.responseText;
       target_block.innerHTML = elem_.querySelector(response_block).innerHTML
    }};
    request.send( null );
}

function ajax_get_reload(url) {
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('GET', url, true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            window.scrollTo(0, 0);
            title = elem_.querySelector('title').innerHTML;
            window.history.pushState(null, "vfgffgfgf", url);
            document.title = title;
            if_list(rtr);
            load_chart();
            page = 2;
            loaded = false;
            create_pagination(rtr)
        }
    }
    ajax_link.send()
}

function this_page_reload(url) {
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('GET', url, true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            window.scrollTo(0, 0);
            if_list(rtr);
            page = 2;
            loaded = false;
            create_pagination(rtr)
        }
    }
    ajax_link.send()
}


on('body', 'click', '.menu_drop', function() {
  block = this.nextElementSibling;
  if (block.classList.contains("show")) { block.classList.remove("show") }
  else {
  all_drop = document.body.querySelectorAll(".dropdown-menu");
  for(i=0; i<all_drop.length; i++) {
    all_drop[i].classList.remove("show")
  } block.classList.add("show")}
});

on('body', 'click', '.user_nav_button', function() {
  document.body.querySelector(".settings_block_hide") ? (settings_block = document.body.querySelector(".settings_block_hide"),settings_block.classList.add("settings_block_show"),settings_block.classList.remove("settings_block_hide"))
  : (settings_block = document.body.querySelector(".settings_block_show"),settings_block.classList.add("settings_block_hide"),settings_block.classList.remove("settings_block_show"))
});

on('body', 'click', '.clean_panel', function(event) {
  close_fullscreen()
})

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  this.querySelector(".unread_count") ? (minus_one_chat(), console.log("minus_one_chat")) : null
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url);
  } else {toast_info("Вы уже на этой странице")}
})
on('body', 'click', '.notify_ajax', function(event) {
  event.preventDefault();
  _this = this;
  var url = _this.getAttribute('href');

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  ajax_link.open('GET', url, true);
  ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  ajax_link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          // если есть блок с классом "user_notify_block", то пользователь на странице видит блоки уведомлений.
          // и, если есть у блока (в который переходит пользователь) непрочитанные уведомления, нужно убавить общий счетчик уведомлений на число этого блока
          if (document.body.querySelector(".user_notify_block")){
            _this.querySelector(".tab_badge") ? (_count = _this.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''),
                                                             _count = _count*1,
                                                             notify = document.body.querySelector(".new_unread_notify"),
                                                             all_count = notify.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''),
                                                             all_count = all_count*1,
                                                             result = all_count - _count,
                                                             result > 0 ? notify.querySelector(".tab_badge").innerHTML = result : notify.innerHTML = '',
                                                             console.log("Вычитаем основной счетчик")
                                                           ) : null;
          }
          elem_ = document.createElement('span');
          elem_.innerHTML = ajax_link.responseText;
          ajax = elem_.querySelector("#reload_block");
          rtr = document.getElementById('ajax');
          rtr.innerHTML = ajax.innerHTML;
          window.scrollTo(0, 0);
          title = elem_.querySelector('title').innerHTML;
          window.history.pushState(null, "vfgffgfgf", url);
          document.title = title;
          page = 2;
          loaded = false;
          create_pagination(rtr);
          if (rtr.querySelector(".user_all_notify_container")) {
            document.body.querySelector(".new_unread_notify").innerHTML = "";
            console.log("Обнуляем основной счетчик")
          }
      }
  }
  ajax_link.send()
})

window.addEventListener('popstate', function (e) {
  e.preventDefault();
  ajax_get_reload(document.referrer);
});

on('body', 'click', '.next_item', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('item_loader'));
})
on('body', 'click', '.prev_item', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('item_loader'));
})

on('body', 'click', '.next_good', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('good_loader'));
})
on('body', 'click', '.prev_good', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('good_loader'));
})

on('body', 'click', '.next_photo', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('photo_loader'));
})
on('body', 'click', '.prev_photo', function(event) {
  event.preventDefault();
  this.style.display = "none";
  open_fullscreen(this.getAttribute('href'), document.getElementById('photo_loader'));
})

on('#ajax', 'click', '.item_stat_f', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("data-uuid");
  loader = document.getElementById("votes_loader");
  open_fullscreen("/stat/item/" + uuid + "/", loader)
});

on('#ajax', 'click', '.post_fullscreen_hide_2', function() {
  parent = this.parentElement.parentElement.parentElement.parentElement;
  parent.parentElement.style.display = "none";
  parent.innerHTML=""
});

on('#ajax', 'click', '.article_fullscreen_hide', function() {document.querySelector(".article_fullscreen").style.display = "none";document.getElementById("article_loader").innerHTML=""});
on('#ajax', 'click', '.photo_fullscreen_hide', function() {document.querySelector(".photo_fullscreen").style.display = "none";document.getElementById("photo_loader").innerHTML=""});
on('#ajax', 'click', '.votes_fullscreen_hide', function() {document.querySelector(".votes_fullscreen").style.display = "none";document.getElementById("votes_loader").innerHTML=""});
on('#ajax', 'click', '.item_fullscreen_hide', function() {document.querySelector(".item_fullscreen").style.display = "none";document.getElementById("item_loader").innerHTML=""});
on('#ajax', 'click', '.community_fullscreen_hide', function() {document.querySelector(".community_fullscreen").style.display = "none";document.getElementById("community_loader").innerHTML=""});
on('#ajax', 'click', '.community_manage_fullscreen_hide', function() {document.querySelector(".manage_window_fullscreen").style.display = "none";document.getElementById("load_staff_window").innerHTML=""});
on('#ajax', 'click', '.good_fullscreen_hide', function() {document.querySelector(".good_fullscreen").style.display = "none";document.getElementById("good_loader").innerHTML=""});
on('#ajax', 'click', '.stat_fullscreen_hide', function() {document.querySelector(".stat_fullscreen").style.display = "none";document.getElementById("stat_loader").innerHTML=""});
on('body', 'click', '.video_fullscreen_hide', function() {document.querySelector(".video_fullscreen").style.display = "none";document.getElementById("video_loader").innerHTML=""});
on('body', 'click', '.small_video_fullscreen_hide', function() {
  document.querySelector(".video_fullscreen").style.display = "none";
  video_window = document.querySelector(".video_fullscreen");
  video_window.classList.remove("video_fullscreen_resized", "draggable");
  document.body.querySelector(".video_btn_small").style.display = "none";
  document.body.querySelector(".video_btn_big").style.display = "block";
  document.getElementById("video_loader").innerHTML=""
});
on('body', 'click', '.create_fullscreen_hide', function() {document.querySelector(".create_fullscreen").style.display = "none";document.getElementById("create_loader").innerHTML=""});
on('body', 'click', '.worker_fullscreen_hide', function() {document.querySelector(".worker_fullscreen").style.display = "none";document.getElementById("worker_loader").innerHTML=""});

// END FULLSCREENS //
//--------------------------------------------------------------------//

on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle('replies_open');
});

on('body', 'click', '.reply_comment', function() {
  div = this.nextElementSibling.nextElementSibling;
  input = div.querySelector(".text-comment");
  input.value = this.previousElementSibling.innerHTML + ', ';
  div.style.display = "block";
  input.focus();
})


on('#ajax', 'click', '.tag_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("tag_" + tag_pk)){
    save_playlist("tag_" + tag_pk, '/music/manage/temp_tag/' + tag_pk, '/music/get/tag/' + tag_pk + "/", track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("tag_" + tag_pk + "/", track_id)}, 50);
  }
  }
  });

on('#ajax', 'click', '.genre_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter') - 1;
  var genre_pk = document.querySelector(".genre_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("genre_" + genre_pk)){
    save_playlist("genre_" + genre_pk, '/music/manage/temp_genre/' + genre_pk, '/music/get/genre/' + genre_pk + "/", track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("genre_" + list_pk + "/", track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_post', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  item = this.parentElement.parentElement.parentElement.parentElement;
  var item_pk = item.getAttribute('data-pk');
  if (!document.body.classList.contains("item_" + item_pk)){
    document.querySelector("body").classList = "";
    document.querySelector("body").classList.add("item_" + item_pk);
    list = [].slice.call(item.querySelectorAll(".music"), 0).reverse();
    for(i=0; i<list.length; i++) {
      _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
      _title=list[i].querySelector(".music_title").innerHTML;
      try{_thumbPath= list[i].querySelector("img").getAttribute("data-src")} catch {_thumbPath = "/static/images/no_track_img.jpg"};
      _duration=list[i].getAttribute("data-duration");
      time = msToTime(_duration);
      music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
    }
    music_player.playSpecificTrack("item_" + item_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("item_" + item_pk, track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_comment', function() {
  var track_id = this.parentElement.parentElement.getAttribute('music-counter');
  comment = this.parentElement.parentElement.parentElement.parentElement;
  var comment_pk = comment.getAttribute('data-pk');
  if (!document.body.classList.contains("comment_" + comment_pk)){
    document.querySelector("body").classList = "";
    document.querySelector("body").classList.add("comment_" + comment_pk);
    list = [].slice.call(comment.querySelectorAll(".media"), 0).reverse();
    for(i=0; i<list.length; i++) {
      _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
      _title=list[i].querySelector(".music_title").innerHTML;
      try{_thumbPath= list[i].querySelector("img").getAttribute("data-src")} catch {_thumbPath = "/static/images/no_track_img.jpg"};
      _duration=list[i].getAttribute("data-duration");
      time = msToTime(_duration);
      music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
    }
    music_player.playSpecificTrack("comment_" + comment_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
    setTimeout(function() {music_player.playSpecificTrack("comment_" + comment_pk, track_id)}, 50);
  }
  }
});
