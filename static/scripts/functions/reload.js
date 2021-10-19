function get_post_view() {
    if (document.body.querySelector(".post_view_generator")) {
        container = document.body.querySelector(".post_view_generator");
        link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        list = container.querySelectorAll('.pag');
        for (var i = 0; i < list.length; i++) {
            if (!list[i].classList.contains("showed") && list[i].classList.contains("post")) {
                inViewport = elementInViewport(list[i]);
                if (inViewport) {
                    try {
                      list[i].getAttribute('data-uuid') ? uuid = list[i].getAttribute('data-uuid') : uuid = list[i].querySelector(".post").getAttribute('data-uuid');
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

/// ФУНКЦИИ СМЕНЫ ПОРЯДКА ЭЛЕМЕНТОВ
function change_position(block, el) {
  // функция инициирует смену порядка элементов,учитывая их класс.
  if (el.classList.contains("u_list")) {send_change_u_post_list(el)} else if (el.classList.contains("c_list")) {send_change_c_post_list(el)} else if (el.classList.contains("u_post")) {send_change_u_post(el)} else if (el.classList.contains("c_post")) {send_change_c_post(el)}
  else if (el.classList.contains("u_doc_list")) {send_change_u_doc_list(el)} else if (el.classList.contains("c_doc_list")) {send_change_c_doc_list(el)} else if (el.classList.contains("u_doc")) {send_change_u_doc(el)} else if (el.classList.contains("c_doc")) {send_change_c_doc(el)}
  else if (el.classList.contains("u_photo_list")) {send_change_u_photo_list(el)} else if (el.classList.contains("c_photo_list")) {send_change_c_photo_list(el)} else if (el.classList.contains("u_photo")) {send_change_u_photo(el)} else if (el.classList.contains("c_photo")) {send_change_c_photo(el)}
  else if (el.classList.contains("u_good_list")) {send_change_u_good_list(el)} else if (el.classList.contains("c_good_list")) {send_change_c_good_list(el)} else if (el.classList.contains("u_good")) {send_change_u_good(el)} else if (el.classList.contains("c_good")) {send_change_c_good(el)}
  else if (el.classList.contains("u_music_list")) {send_change_u_music_list(el)} else if (el.classList.contains("c_music_list")) {send_change_c_music_list(el)} else if (el.classList.contains("u_music")) {send_change_u_music(el)} else if (el.classList.contains("c_music")) {send_change_c_music(el)}
  else if (el.classList.contains("u_survey_list")) {send_change_u_survey_list(el)} else if (el.classList.contains("c_survey_list")) {send_change_c_survey_list(el)} else if (el.classList.contains("u_survey")) {send_change_u_survey(el)} else if (el.classList.contains("c_survey")) {send_change_c_survey(el)}
  else if (el.classList.contains("u_video_list")) {send_change_u_video_list(el)} else if (el.classList.contains("c_video_list")) {send_change_c_video_list(el)} else if (el.classList.contains("u_video")) {send_change_u_video(el)} else if (el.classList.contains("c_video")) {send_change_c_video(el)}
}

function send_change_u_post(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_post"), "/posts/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_post(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_post"), "/posts/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_post_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_list"), "/posts/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_post_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_list"), "/posts/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}

function send_change_u_doc(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_doc"), "/docs/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_doc(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_doc"), "/docs/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_doc_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_doc_list"), "/docs/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_doc_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_doc_list"), "/docs/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}

function send_change_u_photo(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_photo"), "/gallery/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_photo(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_photo"), "/gallery/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_photo_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_photo_list"), "/gallery/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_photo_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_photo_list"), "/gallery/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}

function send_change_u_good(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_good"), "/goods/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_good(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_good"), "/goods/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_good_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_good_list"), "/goods/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_good_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_good_list"), "/goods/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}

function send_change_u_music(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_music"), "/music/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_music(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_music"), "/music/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_music_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_music_list"), "/music/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_music_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_music_list"), "/music/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}

function send_change_u_survey(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_survey"), "/survey/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_survey(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_survey"), "/survey/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_survey_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_survey_list"), "/survey/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_survey_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_survey_list"), "/survey/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}

function send_change_u_video(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".u_video"), "/video/user_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_c_video(el) {
  parent = el.parentElement;
  send_change_items(parent.querySelectorAll(".c_video"), "/video/community_progs/change_position/" + parent.getAttribute("owner-pk") + "/")
}
function send_change_u_video_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".u_video_list"), "/video/user_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
function send_change_c_video_list(el) {
  send_change_items(el.parentElement.querySelectorAll(".c_video_list"), "/video/community_progs/change_list_position/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/")
}
/// КОНЕЦ ФУНКЦИЙ СМЕНЫ ПОРЯДКА ЭЛЕМЕНТОВ
function block_scrolled(_block) {
  window.onscroll = function() {
    console.log("paginate")
      try {
          box = _block.querySelector('.next_page_list');
          if (box && box.classList.contains("next_page_list")) {
              inViewport = elementInViewport(box);
              if (inViewport) {
                  box.classList.remove("next_page_list");
                  paginate(box, target);
              }
          };
          if (target == 1) {
              get_post_view()
          }
      } catch {return}
  }
}
function scrolled(_block, target) {
    // работа с прокруткой:
    // 1. Ссылка на страницу с пагинацией
    // 2. id блока, куда нужно грузить следующие страницы
    // 3. Указатель на нужность работы просмотров элементов в ленте. Например, target=1 - просмотры постов в ленте
    window.onscroll = function() {
        try {
            box = _block.querySelector('.next_page_list');
            if (box && box.classList.contains("next_page_list")) {
                inViewport = elementInViewport(box);
                if (inViewport) {
                    box.classList.remove("next_page_list");
                    paginate(box, target);
                }
            };
            if (target == 1) {
                get_post_view()
            }
        } catch {return}
    }
}

function top_paginate(block, target) {
    // работа с прокруткой для подгрузки сообщений вверх страницы:
    // 1. Ссылка на страницу с пагинацией
    // 2. id блока, куда нужно грузить следующие страницы
        var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        link_3.open('GET', location.protocol + "//" + location.host + block.getAttribute("data-link"), true);
        link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        link_3.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var elem = document.createElement('span');
                elem.innerHTML = link_3.responseText;
                if (target == 1) {
                  block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_post_paginate").innerHTML)
                } else {
                  block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_paginate").innerHTML)
                };
                block.remove()
            }
        }
        link_3.send();
};

function open_video_fullscreen(url) {
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', url, true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem = link.responseText;
            block = document.body.querySelector("#video_loader")
            block.parentElement.style.display = "block";
            block.innerHTML = elem;
            get_document_opacity_0();
        }
    };
    link.send();
};

function paginate(block, target) {
        var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        link_3.open('GET', location.protocol + "//" + location.host + block.getAttribute("data-link"), true);
        link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        link_3.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var elem = document.createElement('span');
                elem.innerHTML = link_3.responseText;
                if (elem.querySelector(".is_post_paginate")) {
                  block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_post_paginate").innerHTML)
                } else if (elem.querySelector(".is_paginate")){
                  block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_paginate").innerHTML)
                } else if (document.body.querySelector(".is_block_paginate")){
                  block_paginate = document.body.querySelector(".is_block_paginate");
                  if (elem.querySelector(".load_block")){
                      block.parentElement.insertAdjacentHTML('beforeend', elem.querySelector(".is_block_paginate").innerHTML)
                  } else {
                    block.parentElement.insertAdjacentHTML('beforeend', elem.innerHTML)
                  }};
                block.remove()
            }
        }
        link_3.send();
}

function create_pagination(block) {
  if (block.querySelector('.chat_container')) {
    scrolled(block.querySelector('.chat_container'), target = 0)
  }
  else if (block.querySelector('.is_paginate')) {
    scrolled(block.querySelector('.is_paginate'), target = 0);
    console.log("Работает пагинация для списка не постов")
  }
  else if (block.querySelector('.is_post_paginate')) {
    scrolled(block.querySelector('.is_post_paginate'), target = 1);
    console.log("Работает пагинация для списка постов")
  }
};

function scrollToBottom(id) {
    document.querySelector(id).scrollIntoView(false);
};

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

function load_item_window() {
  params = window.location.search.replace( '?', '').split('&');
  if (params) {
    if (params[0].split("=")[1] == "wall") {
      console.log(params[1]);
      console.log(params[2]);
      console.log(params[3]);
      // если есть параметр wall, значит открыт элемент стены: пост, прикрепленный элемент, и т.д.
      if (params[2].split("=")[0] == "post_uuid") {
        setTimeout(create_fullscreen("/posts/post/" + params[2].split("=")[1] + "/", "worker_fullscreen"), 3000)
      } else if (params[2].split("=")[0] == "photo_uuid") {
        setTimeout(create_fullscreen("/gallery/post_photo/" + params[3].split("=")[1] + "/" + params[2].split("=")[1] + "/", "photo_fullscreen"), 3000)
      } else if (params[2].split("=")[0] == "doclist") {
        console.log("doclist");
        setTimeout(create_fullscreen("/docs/load_list/" + params[2].split("=")[1] + "/", "worker_fullscreen"), 3000)
      }
    }

    else if (params[0].split("=")[1] == "big_page") {
      // если есть параметр big_page, значит открыта страница пользователя или сообщества
      if (params[2].split("=")[0] == "photo_uuid") {
        setTimeout(create_fullscreen("/gallery/photo/" + params[2].split("=")[1] + "/", "photo_fullscreen"), 3000)
      }
      else if (params[2].split("=")[0] == "ava_photo_uuid") {
        if (params[1].split("=")[0] == "user_id") {
          folder = "user"
        } else { folder = "community" };
        setTimeout(create_fullscreen("/gallery/" + folder + "/avatar/" + params[2].split("=")[1] + "/", "photo_fullscreen"), 3000)
      }
    }
  }
};


function if_list(block) {
  // прога подгружает списки чего либо при подгрузке страницы, а также подтягивает окна
    if (block.querySelector('.is_profile_post_paginate')) {
        _block = block.querySelector('.is_profile_post_paginate');
        link = "/users/detail/list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + _block.getAttribute("list-pk") + "/";
        list_block_load(_block, ".post_container", link);
        scrolled(_block.querySelector('.list_pk'), target = 1);
    } else if (block.querySelector('.is_community_post_paginate')) {
        _block = block.querySelector('.is_community_post_paginate');
        link = "/communities/list/" + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/" + _block.getAttribute("list-pk") + "/";
        list_block_load(_block, ".post_container", link);
        scrolled(_block.querySelector('.list_pk'), target = 1)
    } else if (block.querySelector('.is_block_post_paginate')) {
        lenta = block.querySelector('.is_block_post_paginate');
        link = lenta.getAttribute("data-link");
        list_load(lenta, link);
        scrolled(lenta.querySelector('.list_pk'), target = 1)
    } else if (block.querySelector('.is_block_paginate')) {
        lenta = block.querySelector('.is_block_paginate');
        link = lenta.getAttribute("data-link");
        list_load(block.querySelector(".is_block_paginate"), link);
        scrolled(lenta.querySelector('.list_pk'), target = 1);
    };
    load_item_window()
};

if_list(document.getElementById('ajax'));
create_pagination(document.getElementById('ajax'));
get_dragula(".drag_container");
get_dragula(".drag_list");

function list_load(block, link) {
    var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    request.open('GET', link, true);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200) {
            block.innerHTML = request.responseText;
            get_dragula(".drag_container");
            create_pagination(block);
            fullscreen_resize()
        }
    };
    request.send(null);
};

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
       create_pagination(target_block);
    }};
    request.upload.onprogress = function(event) {
      console.log( 'начало работы');
    };
    request.upload.onload = function() {
      alert( 'конец работы!' );
    };
    request.send( null );
}

// Работаем с историей, создавая свою! Всё, что меняет адреса, отправляем сюда!

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
            loaded = false;
            create_pagination(rtr);

        }
    }
    ajax_link.send()
};


$serf_history = [];

window.addEventListener('popstate', function (e) {
  e.preventDefault();

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  ajax_link.open('GET', $serf_history.slice(-1), true);
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
          window.history.pushState(null, "vfgffgfgf", $serf_history.slice(-1));
          document.title = title;
          if_list(rtr);
          create_pagination(rtr);
          get_dragula(".drag_container");
          get_dragula(".drag_list");
          get_document_opacity_1(rtr);
          $serf_history.pop();
      }
  }
  ajax_link.send()
});

function ajax_get_reload(url) {
  $serf_history.push(document.location.href);

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
            create_pagination(rtr);
            get_dragula(".drag_container");
            get_dragula(".drag_list");
            get_document_opacity_1(rtr);
        }
    }
    ajax_link.send()
}

function create_fullscreen(url, type_class) {
  container = document.body.querySelector("#fullscreens_container");
  try {count_items = container.querySelectorAll(".card_fullscreen").length} catch {count_items = 0};

  $parent_div = document.createElement("div");
  $parent_div.classList.add("card_fullscreen", "mb-3", "border", type_class);
  $parent_div.style.zIndex = 100 + count_items;
  $parent_div.style.opacity = "0";

  if (document.body.querySelector(".desctop_nav")) {
    hide_svg = '<svg class="svg_default" style="position:fixed;" width="30" height="30" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>'
  } else { hide_svg = "" };
  $hide_span = document.createElement("span");
  $hide_span.classList.add("this_fullscreen_hide");
  $loader = document.createElement("div");

  $loader.setAttribute("id", "fullscreen_loader");
  $hide_span.innerHTML = hide_svg;
  $parent_div.append($hide_span);
  $parent_div.append($loader);
  $parent_div.append(create_gif_loading ());
  container.prepend($parent_div);

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link.open('GET', url, true);
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          $load_div.remove();
          elem = link.responseText;

          $loader.innerHTML = elem;
          height = $loader.scrollHeight*1 + 30;
          if (height < 500 && !$loader.querySelector(".data_display")) {
            $parent_div.style.height = height + "px";
            $loader.style.overflowY = "unset";

            _height = (window.innerHeight - height - 50) / 2;
            $parent_div.style.top = _height + "px";
            prev_next_height = _height*1 + 50 + "px";
            try {$loader.querySelector(".prev_item").style.top = "-" + prev_next_height}catch {null};
            try {$loader.querySelector(".next_item").style.top = "-" + prev_next_height}catch {null}
          } else {
            $parent_div.style.height = "100%";
            $parent_div.style.top = "15px";
            $loader.style.overflowY = "auto";
          };
          $parent_div.style.opacity = "1";
          if ($loader.querySelector(".data_display")) {
            $loader.style.overflowY = "unset";
          }

          get_document_opacity_0();

          if ($loader.querySelector(".next_page_list")) {
            $loader.onscroll = function() {
              box = $loader.querySelector('.next_page_list');
              if (box && box.classList.contains("next_page_list")) {
                  inViewport = elementInViewport(box);
                  if (inViewport) {
                      box.remove();
                      var link_3 = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
                      link_3.open('GET', location.protocol + "//" + location.host + box.getAttribute("data-link"), true);
                      link_3.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                      link_3.onreadystatechange = function() {
                          if (this.readyState == 4 && this.status == 200) {
                              var elem = document.createElement('span');
                              elem.innerHTML = link_3.responseText;
                              $loader.querySelector(".is_block_paginate").insertAdjacentHTML('beforeend', elem.querySelector(".is_block_paginate").innerHTML);
                            }
                      }
                      link_3.send();
                  }
              };
            }
          }
      }
  };
  link.send();
};


function change_this_fullscreen(_this, type_class) {
  _this.parentElement.classList.contains("col") ? $loader = _this.parentElement.parentElement.parentElement.parentElement : $loader = _this.parentElement.parentElement;
  $loader.innerHTML = "";
  $parent_div.style.opacity = "0";
  $parent_div.style.height = "35px";
  url = _this.getAttribute("href");
  $serf_history.push(url);

  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link.open('GET', url, true);
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          elem = link.responseText;
          $loader.innerHTML = elem;
          height = $loader.scrollHeight*1 + 30;
          $parent_div = $loader.parentElement
          if (height < 500 && !$loader.querySelector(".data_display")){
            $parent_div.style.height = height + "px";
            _height = (window.innerHeight - height - 50) / 2;
            $parent_div.style.top = _height + "px";
            prev_next_height = _height*1 + 50 + "px";
            $loader.style.overflowY = "unset";
            try {$loader.querySelector(".prev_item").style.top = "-" + prev_next_height}catch {null};
            try {$loader.querySelector(".next_item").style.top = "-" + prev_next_height}catch {null}
          } else {
            $parent_div.style.height = "100%";
            $parent_div.style.top = "15px";
            $loader.style.overflowY = "auto";
          };
          $parent_div.style.opacity = "1";
          $parent_div.style.opacity = "1";
          if ($loader.querySelector(".data_display")) {
            $loader.style.overflowY = "unset";
          };
          url_split = url.split("/");
          new_uuid = url_split.slice(-2);
          params = window.location.search.replace( '?', '').split('&');
          new_url = window.location.href.replace(params[2].split("=")[1], new_uuid[0])
          window.history.replaceState(null, null, new_url);
      }
  };
  link.send();
};

function create_gif_loading () {
  $load_gif = document.createElement("img");
  $load_gif.setAttribute("src", "/static/images/preloader.gif");
  $load_gif.style.width = "40px";
  $load_div = document.createElement("div");
  $load_div.classList.add("centered", "m-1");
  $load_div.append($load_gif);
  return $load_div
};

function close_fullscreen() {
  container = document.body.querySelector("#fullscreens_container");
  container.querySelector(".card_fullscreen").remove();
  if (!container.innerHTML) {
    get_document_opacity_1(document.body.querySelector(".main-container"));
  };
  window.history.replaceState(null, null, window.location.pathname);
};
