function get_post_view() {
    if (document.body.querySelector(".is_profile_post_paginate")) {
        container = document.body.querySelector(".is_profile_post_paginate");
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
        try {
            if (document.body.querySelector(".chat_container")){
              block_ = document.body.querySelector(block_id);
              box_ = block_.querySelector('.first');
              if (box_ && box_.classList.contains("first")) {
                inViewport = elementInViewport(box_);
                if (inViewport) {box_.classList.remove("first");top_paginate(link, block_id)}}
            } else {_block = document.body.querySelector(block_id);
                  box = _block.querySelector('.last');
                  if (box && box.classList.contains("last")) {
                    inViewport = elementInViewport(box);
                    if (inViewport) {
                      box.classList.remove("last");
                      paginate(link, block_id);
                    }
                  };
                  if (target == 1) {get_post_view()}}
                } catch {return}
    }
};
page = 2;
loaded = false;
m_page = 2;
m_loaded = false;

function get_dragula(block) {
  // функция инициирует библиотеку dragula.js
  _block = document.querySelector(block)
  dragula([_block], {
    moves: function (el, container, handle) {
      return handle.classList.contains('handle')
    }})
    //.on('drag', function (el) {console.log("drag!");})
    .on('drop', function (el) {console.log(el); change_position(_block, el)})
    //.on('over', function (el, container) {console.log("over!"); over = true;})
    //.on('out', function (el, container) {console.log("over!");;});
}

function change_position(block, el) {
  // функция инициирует смену порядка элементов,учитывая их класс.
  if (el.classList.contains("u_list")) {
    send_change_u_post_list(el)
  } else if (el.classList.contains("c_list")) {
    send_change_c_post_list(el)
  } else if (el.classList.contains("u_post")) {
    console.log("Порядок постов изменен!");
    send_change_u_posts(el)
  } else if (el.classList.contains("c_post")) {
    console.log("Порядок постов изменен!");
    send_change_c_posts(el)
  }
}

/// ФУНКЦИИ СМЕНЫ ПОРЯДКА ЭЛЕМЕНТОВ
function send_change_u_posts(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_post"), "/posts/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_posts(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_post"), "/posts/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_post_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_list"), "/posts/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_post_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_list"), "/posts/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
/// КОНЕЦ ФУНКЦИЙ СМЕНЫ ПОРЯДКА ЭЛЕМЕНТОВ

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
                if (elem.querySelector(".is_chat_paginate")) {
                    xxx = document.createElement("span");
                    xxx.innerHTML = elem.querySelector(".is_chat_paginate").innerHTML;
                    document.body.querySelector(".is_chat_paginate").insertAdjacentHTML('afterbegin', xxx.innerHTML)
                } else {
                    document.body.querySelector(".is_chat_paginate").insertAdjacentHTML('afterbegin', elem.innerHTML)
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
  if (block.querySelector('.chat_container')) {
    scrolled(window.location.href, '.chat_container', target = 0)
  }
  else if (block.querySelector('.is_paginate')) {
    scrolled(window.location.href, '.is_paginate', target = 0)
  }
  else if (block.querySelector('.is_post_paginate')) {
    scrolled(window.location.href, '.is_post_paginate', target = 1)
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
        _block = block.querySelector('.is_profile_post_paginate');
        link = "/users/detail/list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + _block.getAttribute("list-pk") + "/";
        list_block_load(_block, ".post_container", link);
        scrolled(link, '.list_pk', target = 1)
    } else if (block.querySelector('.is_community_post_paginate')) {
        _block = block.querySelector('.is_community_post_paginate');
        link = "/communities/list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + _block.getAttribute("list-pk") + "/";
        list_block_load(_block, ".post_container", link);
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
load_chart();
get_dragula(".drag_container");
get_dragula(".drag_list");

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
       target_block.innerHTML = elem_.querySelector(response_block).innerHTML;
       get_dragula(".is_post_paginate");
       get_dragula(".date-list");
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
            create_pagination(rtr);
            get_dragula(".drag_container");
            get_dragula(".drag_list");
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
