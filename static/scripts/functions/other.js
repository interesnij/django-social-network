function on(elSelector,eventName,selector,fn) {var element = document.querySelector(elSelector);element.addEventListener(eventName, function(event) {var possibleTargets = element.querySelectorAll(selector);var target = event.target;for (var i = 0, l = possibleTargets.length; i < l; i++) {var el = target;var p = possibleTargets[i];while(el && el !== element) {if (el === p) {return fn.call(p, event);}el = el.parentNode;}}});};

function check_message_form_btn() {
  input = document.body.querySelector(".message_text");
  btn_block = input.nextElementSibling.nextElementSibling;
  if (input.innerHTML.trim() == "" && !document.body.querySelector(".special_block").firstChild){
     btn_block.querySelector("#voice_start_btn").style.display = "block";
     btn_block.querySelector("#message_post_btn").style.display = "none";
  } else {
    btn_block.querySelector("#voice_start_btn").style.display = "none";
    btn_block.querySelector("#message_post_btn").style.display = "block";
  }
}
function show_message_form_send_btn() {
  document.body.querySelector("#voice_start_btn").style.display = "none";
  document.body.querySelector("#message_post_btn").style.display = "block";
}
function show_message_form_voice_btn() {
  document.body.querySelector("#voice_start_btn").style.display = "block";
  document.body.querySelector("#message_post_btn").style.display = "none";
}

function remove_item_and_show_restore_block(item, url, _class, title) {
  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  console.log(item)
    ajax_link.open( 'GET', url + item.getAttribute("data-uuid") + "/", true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        p = document.createElement("div");
        p.classList.add("media", "p-1");
        p.style.padding = "20px";
        p.innerHTML = "<span class='" + _class + " pointer' data-uuid='" + item.getAttribute("data-uuid") + "'>" + title + ". <span class='underline'>Восстановить</span></span>";
        item.parentElement.insertBefore(p, item), item.style.display = "none";
      }
    }
    ajax_link.send();
}

function get_edit_comment_form(_this, url){
  clear_comment_dropdown();
  pk = _this.parentElement.getAttribute("data-pk");
  _this.parentElement.style.display = "none";
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    parent = _this.parentElement.parentElement.parentElement;

    parent.parentElement.querySelector(".comment_text").style.display = "none";
    parent.parentElement.querySelector(".attach_container") ? parent.parentElement.querySelector(".attach_container").style.display = "none" : null;
    parent.append(response);
  }};
  link.send( null );
}

function post_edit_comment_form(_this, url) {
  form = _this.parentElement.parentElement.parentElement
  span_form = form.parentElement;
  block = span_form.parentElement.parentElement.parentElement;
  $input = document.createElement("input");
  $input.setAttribute("name", "text");
  $input.setAttribute("type", "hidden");
  $input.classList.add("input_text");
  $input.value = form.querySelector(".smile_supported").innerHTML;
  form.append($input);
  form_comment = new FormData(form);
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('POST', url + _this.getAttribute("data-pk") + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  if (!form.querySelector(".text-comment").value && !form.querySelector(".img_block").firstChild){
    toast_error("Напишите или прикрепите что-нибудь");
    form.querySelector(".text-comment").style.border = "1px #FF0000 solid";
    form.querySelector(".dropdown").style.border = "1px #FF0000 solid";
    return
  };
  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          block.querySelector(".media-body").innerHTML = new_post.querySelector(".media-body").innerHTML;
          toast_success("Комментарий изменен");
      }
  };
  link_.send(form_comment)
}

function send_change_items(array, link) {
  // функция передает новый порядок элементов, принимая их массив и ссылку, по которой нужно отправить изменения.
  len = array.length + 1;
  console.log(len);
  token = document.body.getAttribute("data-csrf");
  post_array = []
  for (var i=0; i<array.length; i++) {
    count = len -= 1;
    post_array.push({key:array[i].getAttribute("data-pk"),value: count});
    console.log(count)
  };
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST", link);
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlhttp.setRequestHeader('X-CSRFToken', token);
  xmlhttp.send(JSON.stringify(post_array));
}

function profile_list_block_attach(_this, block, url, actions_class) {
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  request.open( 'GET', "/users/load" + url + _this.parentElement.parentElement.parentElement.getAttribute("data-uuid") + "/", true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ){
        elem_ = document.createElement('span');
        elem_.innerHTML = request.responseText;
       document.body.querySelector(block).innerHTML = elem_.querySelector(block).innerHTML;
       class_to_add = _this.parentElement.parentElement.parentElement.parentElement.parentElement.querySelectorAll(".list_toggle")
       for (var i = 0; i < class_to_add.length; i++) {
         class_to_add[i].classList.add(actions_class, "pointer");
         class_to_add[i].parentElement.parentElement.parentElement.classList.replace("active_border", "border");
       };
       parent = _this.parentElement.parentElement.parentElement;
       parent.querySelector(".list_svg")? parent.querySelector(".list_svg").classList.remove(actions_class, "pointer") : null;
       parent.querySelector(".list_name")? parent.querySelector(".list_name").classList.remove(actions_class, "pointer") : null;
       parent.classList.replace("border", "active_border");

       if (elem_.querySelector(".is_block_paginate")) {
         lenta = elem_.querySelector('.is_block_paginate');
         link = lenta.getAttribute("data-link");
         //list_load(document.body.querySelector(".is_block_paginate"), link);
         console.log("youhuuuu")
         scrolled(document.body.querySelector('.is_block_paginate'), target = 0)
       };
    }};
    request.send( null );
}
function media_list_edit(_this, url) {
  form = _this.parentElement.parentElement.parentElement;
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { _this.disabled = true }
  uuid = form.getAttribute("data-uuid")

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    close_create_window();
    name = form.querySelector('#id_name').value;
    list = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' );
    list.querySelector('.list_name') ? list.querySelector('.list_name').innerHTML = name : null;
    document.body.querySelector('.second_list_name').innerHTML = name;
    toast_success("Список изменен")
  }}
  link_.send(form_data);
}
function media_list_delete(_this, url, old_class, new_class) {
  uuid = _this.parentElement.parentElement.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    _this.previousElementSibling.style.display = "none";
    _this.previousElementSibling.previousElementSibling.style.display = "none";
    _this.parentElement.querySelector(".second_list_name").innerHTML = "Список удален";
    list = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' );
    list.querySelector('.list_name') ? list.querySelector('.list_name').innerHTML = "Список удален" : null;
    _this.classList.replace(old_class, new_class);
    _this.innerHTML = "Восстановить список";
  }}
  link_.send();
}
function media_list_recover(_this, url, old_class, new_class) {
  uuid = _this.parentElement.parentElement.getAttribute('data-uuid');
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'GET', url + uuid + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    _this.previousElementSibling.style.display = "unset";
    _this.previousElementSibling.previousElementSibling.style.display = "unset";
    second_list = document.body.querySelector('.second_list_name');
    name = second_list.getAttribute("data-name");
    second_list.innerHTML = name;
    document.body.querySelector('.file-manager-item') ?
      (list = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ),
       list.querySelector('.list_name').innerHTML = name) : null;
    _this.classList.replace(old_class, new_class);
    _this.innerHTML = "Удалить список";
  }}
  link_.send();
}

function check_span1(span1, uuid, response) {
  if (span1.classList.contains(uuid)){
    document.body.querySelector(".is_paginate").insertAdjacentHTML('afterBegin', response)
  }
}
function profile_list_block_load(_this, block, url, actions_class) {
  // подгрузка списков в профиле пользователя
  var request = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  saver = _this.parentElement.parentElement.parentElement;
  saver.classList.contains("community") ?
  link = "/communities/" + saver.getAttribute("data-pk") + url + saver.getAttribute("data-uuid") + "/" :
  link = "/users/" + saver.getAttribute("data-pk") + url + saver.getAttribute("data-uuid") + "/";
  request.open( 'GET', link, true );
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  request.onreadystatechange = function () {
    if ( request.readyState == 4 && request.status == 200 ){
        elem_ = document.createElement('span');
        elem_.innerHTML = request.responseText;
       document.body.querySelector(block).innerHTML = elem_.querySelector(block).innerHTML;
       if (elem_.querySelector(".is_block_paginate")) {
         lenta = elem_.querySelector('.is_block_paginate');
         link = lenta.getAttribute("data-link");
         list_load(document.body.querySelector(".is_block_paginate"), link);
         //scrolled(lenta.querySelector('.list_pk'), target = 0)
       };
       //create_pagination(document.body.querySelector(block));

       class_to_add = _this.parentElement.parentElement.parentElement.parentElement.parentElement.querySelectorAll(".list_toggle")
       for (var i = 0; i < class_to_add.length; i++) {
         class_to_add[i].classList.add(actions_class, "pointer");
         class_to_add[i].parentElement.parentElement.parentElement.classList.replace("active_border", "border");
       };
       parent = _this.parentElement.parentElement.parentElement;
       parent.querySelector(".list_svg")? parent.querySelector(".list_svg").classList.remove(actions_class, "pointer") : null;
       parent.querySelector(".list_name").classList.remove(actions_class, "pointer");
       parent.classList.replace("border", "active_border");
    }};
    request.send( null );
}

function on_off_list_in_collections(_this, url, new_class, old_class, text) {
  pk = _this.parentElement.parentElement.getAttribute("data-uuid");
  var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + pk + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
    if ( link.readyState == 4 && link.status == 200 ) {
      _this.innerHTML = "";
      _this.classList.add(new_class);
      _this.classList.remove(old_class)
      _this.innerHTML = text
}}
link.send( null );
};

function add_item_in_list(_this, url, old_class, new_class) {
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.style.paddingLeft = "14px";
    _this.classList.add(new_class);
    _this.classList.remove(old_class);
    span = document.createElement("span");
    span.innerHTML = '<svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg> ';
    _this.prepend(span)
  }};
  link.send( null );
}
function remove_item_from_list(_this, url, old_class, new_class) {
  parent = _this.parentElement;
  uuid = parent.getAttribute("data-uuid");
  pk = _this.parentElement.parentElement.parentElement.parentElement.getAttribute("data-pk");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', url + pk + "/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    _this.style.paddingLeft = "30px";
    _this.classList.add(new_class);
    _this.classList.remove(old_class);
    _this.querySelector("svg").remove();
  }};
  link.send( null );
}

function get_preview(response, type) {
  if (document.body.querySelector(".current_file_dropdown")){
    if (type == "doc") {
      pk = response.querySelector(".span_btn").getAttribute("data-pk");
      media_body = response.querySelector(".media-body");
      media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
      doc_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, media_body, pk)
    } else if (type == "track") {
      response.querySelector(".span_btn").remove(); response.querySelector(".small").remove();
      track_comment_attach(document.body.querySelector(".current_file_dropdown").parentElement.parentElement, response)
    }
  } else if (document.body.querySelector(".attach_block")){
    if (type == "doc") {
      pk = response.querySelector(".span_btn").getAttribute("data-pk");
      media_body = response.querySelector(".media-body");
      media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
      doc_post_attach(document.body.querySelector(".attach_block"), response.querySelector(".media-body"), pk)
    }
  } else if (document.body.querySelector(".message_attach_block")){
    if (type == "doc") {
      pk = response.querySelector(".span_btn").getAttribute("data-pk");
      media_body = response.querySelector(".media-body");
      media_body.querySelector(".span_btn").remove(); media_body.querySelector(".small").remove();
      doc_message_attach(document.body.querySelector(".message_attach_block"), response.querySelector(".media-body"), pk)
  }
  };
};
function close_fullscreen() {
  if (document.body.querySelector(".create_fullscreen").style.display == "block") {
    get_document_opacity_1(document.getElementById("create_loader"))
    document.body.querySelector(".create_fullscreen").style.display = "none";
    document.querySelector("#create_fullscreen").innerHTML=""
  } else if (document.body.querySelector(".photo_fullscreen").style.display == "block") {
    get_document_opacity_1(document.getElementById("photo_loader"))
    document.body.querySelector(".photo_fullscreen").style.display = "none";
    document.querySelector("#photo_loader").innerHTML=""
  } else if (document.body.querySelector(".article_fullscreen").style.display == "block") {
    get_document_opacity_1(document.getElementById("article_loader"))
    document.body.querySelector(".article_fullscreen").style.display = "none";
    document.querySelector("#article_loader").innerHTML=""
  } else if (document.body.querySelector(".item_fullscreen").style.display == "block") {
    get_document_opacity_1(document.getElementById("item_loader"))
    document.body.querySelector(".item_fullscreen").style.display = "none";
    document.body.querySelector(".item_fullscreen").querySelector(".loader_0").innerHTML=""
  } else if (document.body.querySelector(".good_fullscreen").style.display == "block") {
    get_document_opacity_1(document.getElementById("good_loader"))
    document.body.querySelector(".good_fullscreen").style.display = "none";
    document.body.querySelector(".good_fullscreen").querySelector(".loader_0").innerHTML=""
  } else if (document.body.querySelector(".votes_fullscreen").style.display == "block") {
    get_document_opacity_1(document.getElementById("votes_loader"))
    document.body.querySelector(".votes_fullscreen").style.display = "none";
    document.body.querySelector(".votes_fullscreen").querySelector(".loader_0").innerHTML=""
  }
}
function check_photo_in_block(block, _this, pk) {
    if (block.querySelector('[photo-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_photo_list_in_block(block, _this, pk) {
    if (block.querySelector('[photolist-pk=' + '"' + pk + '"' + ']')) {
        toats_info("Альбом уже прикреплён")
        return true
    } else {
        return false
    }
}
function check_video_in_block(block, _this, pk) {
    if (block.querySelector('[video-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Видеоролик уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_video_list_in_block(block, _this, pk) {
    if (block.querySelector('[videolist-pk=' + '"' + pk + '"' + ']')) {
        toats_info("Видеоальбом уже прикреплён")
        return true
    } else {
        return false
    }
}
function check_music_in_block(block, _this, counter) {
    if (block.querySelector('[music-counter=' + '"' + pk + '"' + ']')) {
        _this.parentElement.setAttribute("tooltip", "Аудиозапись уже выбрана");
        _this.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_playlist_in_block(block, _this, pk) {
    if (block.querySelector('[playlist-pk=' + '"' + pk + '"' + ']')) {
        toats_info("Плейлист уже прикреплён")
        return true
    } else {
        return false
    }
}
function check_doc_in_block(block, _this, pk) {
    if (block.querySelector('[doc-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.parentElement.setAttribute("tooltip", "Документ уже выбран");
        _this.parentElement.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_doc_list_in_block(block, _this, pk) {
    if (block.querySelector('[doclist-pk=' + '"' + pk + '"' + ']')) {
        toats_info("Список документов уже прикреплён")
        return true
    } else {
        return false
    }
}
function check_good_in_block(block, _this, pk) {
    if (block.querySelector('[good-pk=' + '"' + pk + '"' + ']')) {
        _this.parentElement.setAttribute("tooltip", "Товар уже выбран");
        _this.parentElement.setAttribute("flow", "up");
        return true
    } else {
        return false
    }
}
function check_good_list_in_block(block, _this, pk) {
    if (block.querySelector('[goodlist-pk=' + '"' + pk + '"' + ']')) {
        toats_info("Список товаров уже прикреплён")
        return true
    } else {
        return false
    }
}

function close_create_window() {
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML = "";
    get_document_opacity_1(document.body.querySelector(".main_container"))
}

function repost_constructor(_this, wall_url, wall_toast, community_url, community_toast, message_url, message_toast) {
    form_post = _this.parentElement.parentElement.parentElement;
    form_data = new FormData(form_post);
    uuid = _this.getAttribute("data-uuid");
    pk = _this.getAttribute("data-pk");
    preview_target_block = form_post.querySelector('#selected_message_target_items');
    link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    if (form_post.querySelector('#repost_radio_wall').checked) {
        link_.open('POST', wall_url + pk + "/" + uuid + "/", true);
        link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        link_.send(form_data);
        toast_info(wall_toast)
    } else if (form_post.querySelector('#repost_radio_community').checked) {
        staff_communities = form_post.querySelector("#id_staff_communities");
        if (preview_target_block.querySelector(".community").value) {
            link_.open('POST', community_url + pk + "/" + uuid + "/", true);
            link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            link_.send(form_data);
            toast_info(community_toast)
        } else {
            toast_error("Выберите сообщества для репоста")
        }
    } else if (form_post.querySelector('#repost_radio_message').checked) {
        if (preview_target_block.querySelector(".chat").value) {
            link_.open('POST', message_url + pk + "/" + uuid + "/", true);
            link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            link_.send(form_data);
            toast_info(message_toast)
        } else {
            toast_error("Выберите пользователя для репоста")
        }
    };
    link_.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.querySelector(".votes_fullscreen").style.display = "none";
            document.getElementById("votes_loader").innerHTML = ""
        }
    }
}

function attach_list_for_post(_this, url) {
    if (document.body.querySelector(".current_file_dropdown")) {
        toast_error("Элемент прикрепляется только к постам")
    } else if (document.body.querySelector(".attach_block")) {
        attach_block = document.body.querySelector(".attach_block");
        if (attach_block.classList.contains("files_0")) {
            pk = _this.getAttribute("data-pk");
            link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
            link_.open('GET', url + pk + "/", true);
            link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            link_.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    attach_block.nextElementSibling.querySelector(".attach_panel").style.display = "none";
                    elem = link_.responseText;
                    response = document.createElement("span");
                    response.innerHTML = elem;
                    attach_block.insertAdjacentHTML('afterBegin', response.innerHTML);
                    close_create_window()
                }
            };
            link_.send()
        } else {
            toast_error("Элемент не влезает, очистите панель прикрепленеия")
        }
    }
}

function post_and_load_object_page(form, url_post, url_1, url_2) {
    form_data = new FormData(form);
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('POST', url_post + pk + "/", true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            window.scrollTo(0, 0);
            document.title = elem_.querySelector('title').innerHTML;
            uuid = rtr.querySelector(".uuid_saver").getAttribute("data-uuid");
            window.history.pushState(null, "vfgffgfgf", url_1 + pk + url_2 + uuid + '/')
        }
    }
    ajax_link.send(form_data)
}

function edit_and_load_object_page(form, url_post, url_1, url_2) {
    form_data = new FormData(form);
    pk = form.getAttribute("data-pk");
    uuid = form.getAttribute("data-uuid");
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('POST', url_post + pk + "/" + uuid + "/", true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            window.scrollTo(0, 0);
            document.title = elem_.querySelector('title').innerHTML;
            uuid = rtr.querySelector(".pk_saver").getAttribute("data-uuid");
            window.history.pushState(null, "vfgffgfgf", url_1 + pk + url_2 + uuid + '/')
        }
    }
    ajax_link.send(form_data)
}

function send_form_and_toast(url, form, toast) {
    form_data = new FormData(form);
    ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    ajax_link.open('POST', url, true);
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            toast_info(toast);
        }
    }
    ajax_link.send(form_data);
}

function get_with_pk_and_reload(url) {
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link_.open('GET', url + pk + "/", true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            this_page_reload(document.location.href);
        }
    };
    link_.send();
}

function post_with_pk_and_reload(parent, url) {
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    form_data = new FormData(parent);

    link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link_.open('POST', url + pk + "/", true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            this_page_reload(document.location.href);
        }
    };
    link_.send(form_data);
}

function comment_delete(_this, _link, _class) {
    data = _this.parentElement;
    comment_pk = data.getAttribute("data-pk");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + comment_pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            comment = data.parentElement.parentElement.parentElement.parentElement;
            comment.style.display = "none";
            div = document.createElement("div");
            div.classList.add("media", "comment");
            div.innerHTML = "<p class='" + _class + "'style='cursor:pointer;text-decoration:underline;padding:15px' data-pk='" + comment_pk + "'>Комментарий удален. Восстановить</p>";
            comment.style.display = "none"
            comment.parentElement.insertBefore(div, comment);
        }
    };
    link.send()
}

function comment_owner_delete(_this, _link, _class) {
    data = _this.parentElement.parentElement;
    comment_pk = data.getAttribute("data-pk");
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/" + comment_pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            comment = data.parentElement.parentElement.parentElement.parentElement;
            comment.style.display = "none";
            div = document.createElement("div");
            div.classList.add("media", "comment");
            div.innerHTML = "<p class='" + _class + "'style='cursor:pointer;text-decoration:underline;padding:15px' data-pk='" + comment_pk + "'>Комментарий удален. Восстановить</p>";
            comment.parentElement.insertBefore(div, comment);
            comment.style.display = "none"
        }
    };
    link.send()
}

function comment_restore(_this, _link) {
    comment = _this.parentElement.nextElementSibling;
    pk = _this.getAttribute("data-pk");
    block = _this.parentElement;
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            block.remove();
            comment.style.display = "flex";
        }
    };
    link.send()
}

function comment_wall_restore(_this, _link) {
    comment = _this.parentElement.nextElementSibling;
    comment_pk = _this.getAttribute("data-pk");
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    block = _this.parentElement;
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/" + comment_pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            block.remove();
            comment.style.display = "flex";
        }
    };
    link.send()
}

function send_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    item.getAttribute("data-uuid") ? uuid = item.getAttribute("data-uuid") : uuid = item.getAttribute("good-pk"); link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + uuid + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}
function mob_send_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement;
    item.getAttribute("data-uuid") ? uuid = item.getAttribute("data-uuid") : uuid = item.getAttribute("good-pk"); link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + uuid + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}

function send_good_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    pk = item.getAttribute("good-pk");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}
function send_mob_good_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = parent.parentElement.parentElement.parentElement.parentElement;
    pk = item.getAttribute("good-pk");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("span");
            new_span.classList.add(new_class, "dropdown-item");
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}

function send_photo_change(span, _link, new_class, html) {
    parent = span.parentElement;
    item = span.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    uuid = item.getAttribute("data-uuid");
    pk = item.getAttribute("data-pk");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', _link + pk + "/" + uuid + "/", true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (link.readyState == 4 && link.status == 200) {
            new_span = document.createElement("a");
            new_span.classList.add(new_class);
            new_span.innerHTML = html;
            parent.innerHTML = "";
            parent.append(new_span)
        }
    };
    link.send(null)
}

class ToastManager {
    constructor() {
        this.id = 0;
        this.toasts = [];
        this.icons = {
            'SUCCESS': "",
            'ERROR': '',
            'INFO': '',
            'WARNING': '',
        };
        var body = document.querySelector('#ajax');
        this.toastsContainer = document.createElement('div');
        this.toastsContainer.classList.add('toasts', 'border-0');
        body.appendChild(this.toastsContainer)
    }
    showSuccess(message) {
        return this._showToast(message, 'SUCCESS')
    }
    showError(message) {
        return this._showToast(message, 'ERROR')
    }
    showInfo(message) {
        return this._showToast(message, 'INFO')
    }
    showWarning(message) {
        return this._showToast(message, 'WARNING')
    }
    _showToast(message, toastType) {
        var newId = this.id + 1;
        var newToast = document.createElement('div');
        newToast.style.display = 'inline-block';
        newToast.classList.add(toastType.toLowerCase());
        newToast.classList.add('toast');
        newToast.innerHTML = `<progress max="100"value="0"></progress><h3>${message}</h3>`;
        var newToastObject = {
            id: newId,
            message,
            type: toastType,
            timeout: 4000,
            progressElement: newToast.querySelector('progress'),
            counter: 0,
            timer: setInterval(() => {
                newToastObject.counter += 1000 / newToastObject.timeout;
                newToastObject.progressElement.value = newToastObject.counter.toString();
                if (newToastObject.counter >= 100) {
                    newToast.style.display = 'none';
                    clearInterval(newToastObject.timer);
                    this.toasts = this.toasts.filter((toast) => {
                        return toast.id === newToastObject.id
                    })
                }
            }, 10)
        }
        newToast.addEventListener('click', () => {
            newToast.style.display = 'none';
            clearInterval(newToastObject.timer);
            this.toasts = this.toasts.filter((toast) => {
                return toast.id === newToastObject.id
            })
        });
        this.toasts.push(newToastObject);
        this.toastsContainer.appendChild(newToast);
        return this.id++
    }
}

function toast_success(text) {
    var toasts = new ToastManager();
    toasts.showSuccess(text)
}

function toast_error(text) {
    var toasts = new ToastManager();
    toasts.showError(text)
}

function toast_info(text) {
    var toasts = new ToastManager();
    toasts.showInfo(text)
}

function toast_warning(text) {
    var toasts = new ToastManager();
    toasts.showWarning(text)
}

function elementInViewport(el) {
    var bounds = el.getBoundingClientRect();
    return ((bounds.top + bounds.height > 0) && (window.innerHeight - bounds.top > 0));
}

function send_comment(form, block, link) {
  $input = document.createElement("input");
  $input.setAttribute("name", "text");
  $input.setAttribute("type", "hidden");
  $input.classList.add("type_hidden");
  $input.value = form.querySelector(".comment_text").innerHTML;
  form.append($input);
    form_comment = new FormData(form);
    link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link_.open('POST', link, true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    if (form.querySelector(".comment_text").value || form.querySelector(".img_block").firstChild) {
      toast_error("Напишите или прикрепите что-нибудь"); return
    };
    link_.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            form.querySelector(".comment_text").innerHTML = "";
            elem = link_.responseText;
            new_post = document.createElement("span");
            new_post.innerHTML = elem;
            block.append(new_post);
            toast_success(" Комментарий опубликован");
            form.querySelector(".img_block").innerHTML = "";
            form.querySelector(".type_hidden").remove();
            try {
                form_dropdown = form.querySelector(".current_file_dropdown");
                form_dropdown.classList.remove("current_file_dropdown");
                form_dropdown.parentElement.parentElement.classList.remove("files_one", "files_two");
                form_dropdown.parentElement.parentElement.classList.add("files_null")
            } catch {
                null
            }
        }
    };
    link_.send(form_comment)
}

function load_chart() {
    try {
        var ctx = document.getElementById('canvas');
        var dates = ctx.getAttribute('dates').split(",");
        var data_1 = ctx.getAttribute('data_1').split(",");
        var data_2 = ctx.getAttribute('data_2').split(",");
        var label_1 = ctx.getAttribute('label_1');
        var label_2 = ctx.getAttribute('label_2');
        var config = {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: label_1,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_1,
                    fill: false,
                }, {
                    label: label_2,
                    fill: false,
                    backgroundColor: 'rgb(54, 162, 235)',
                    borderColor: 'rgb(54, 162, 235)',
                    data: data_2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: ''
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: ''
                        }
                    }]
                }
            }
        };
        ctx.getContext('2d');
        window.myLine = new Chart(ctx, config)
    } catch {
        return
    }
}

function addStyleSheets(href) {
    $head = document.head, $link = document.createElement('link');
    $link.rel = 'stylesheet';
    $link.classList.add("my_color_settings");
    $link.href = href;
    $head.appendChild($link)
}

function get_document_opacity_0() {
  if (document.body.querySelector(".mobile_naw")) {
    document.body.querySelector(".main-container").style.opacity = "0";
  } else {
  document.body.querySelector(".main-header").style.opacity = "0";
  document.body.querySelector(".main-container").style.opacity = "0";
  document.body.querySelector(".left_panel_menu").style.opacity = "0"
  }
};
function get_document_opacity_1(block) {
  main_container = document.body.querySelector(".main-container");
  if (document.body.querySelector(".mobile_naw")) {
    main_container.style.opacity = "1";
  } else {
  document.body.querySelector(".main-header").style.opacity = "1";
  main_container.style.opacity = "1";
  document.body.querySelector(".left_panel_menu").style.opacity = "1"
  };
    create_pagination(main_container);
};

function open_fullscreen(url, block) {
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link.open('GET', url, true);
    link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem = link.responseText;
            block.parentElement.style.display = "block";
            block.innerHTML = elem;
            if (block.querySelector(".next_page_list")) {
              get_document_opacity_0();
              if (block.querySelector(".is_block_paginate")) {
                scrolled(block.querySelector(".is_block_paginate"), target = 0);
                console.log("Работает пагинация обычная")
              } else {
                scrolled(block.querySelector(".is_block_post_paginate"), target = 1)
                console.log("Работает пагинация постов")
              }
            }
        }
    };
    link.send();
}

function open_load_fullscreen(link, block) {
    var link_, elem;
    link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link_.open('GET', link, true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link_.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            elem = link_.responseText;
            block.parentElement.style.display = "block";
            block.innerHTML = "";
            block.innerHTML = elem;
            if (block.querySelector(".next_page_list")) {
              get_document_opacity_0();
              if (block.querySelector(".is_block_paginate")) {
                scrolled(block.querySelector(".is_block_paginate"), target = 0);
                console.log("Работает пагинация обычная")
              } else {
                scrolled(block.querySelector(".is_block_post_paginate"), target = 1)
                console.log("Работает пагинация постов")
              }
            }
        }
    };
    link_.send();
}

function post_update_votes(post, uuid) {
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('GET', "/posts/user_progs/update_votes/" + uuid + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          jsonResponse = JSON.parse(link_.responseText);
          post.querySelector(".likes_count").innerHTML = jsonResponse.like_count;
          post.querySelector(".dislikes_count").innerHTML = jsonResponse.dislike_count;
      }
  };

  link_.send();
}

function send_like(item, link) {
    like = item.querySelector(".like");
    dislike = item.querySelector(".dislike");
    link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link__.overrideMimeType("application/json");
    link__.open('GET', link, true);
    link__.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link__.onreadystatechange = function() {
        if (link__.readyState == 4 && link__.status == 200) {
            jsonResponse = JSON.parse(link__.responseText);
            likes_count = item.querySelector(".likes_count");
            dislikes_count = item.querySelector(".dislikes_count");
            likes_count.innerHTML = jsonResponse.like_count;
            dislikes_count.innerHTML = jsonResponse.dislike_count;
            like.classList.toggle("btn_success");
            like.classList.toggle("btn_default");
            dislike.classList.add("btn_default");
            dislike.classList.remove("btn_danger")
        }
    };
    link__.send(null)
}

function send_dislike(item, link) {
    like = item.querySelector(".like");
    dislike = item.querySelector(".dislike");
    link__ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    link__.overrideMimeType("application/json");
    link__.open('GET', link, true);
    link__.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    link__.onreadystatechange = function() {
        if (link__.readyState == 4 && link__.status == 200) {
            jsonResponse = JSON.parse(link__.responseText);
            likes_count = item.querySelector(".likes_count");
            dislikes_count = item.querySelector(".dislikes_count");
            likes_count.innerHTML = jsonResponse.like_count;
            dislikes_count.innerHTML = jsonResponse.dislike_count;
            dislike.classList.toggle("btn_danger");
            dislike.classList.toggle("btn_default");
            like.classList.add("btn_default");
            like.classList.remove("btn_success")
        }
    };
    link__.send(null)
}

function get_image_priview(ggg, img) {
    entrou = false;
    img.click();
    img.onchange = function() {
        if (!entrou) {
            imgPath = img.value;
            extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
            if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
                if (typeof FileReader != "undefined") {
                    if (ggg) {}
                    ggg.innerHTML = "";
                    reader = new FileReader();
                    reader.onload = function(e) {
                        $img = document.createElement("img");
                        $img.src = e.target.result;
                        $img.class = "thumb-image";
                        $img.style.width = "100%";
                        ggg.innerHTML = '<a href="#" style="right:15px;top: 0;" class="delete_thumb">Удалить</a>'
                        ggg.append($img)
                    };
                    reader.readAsDataURL(img.files[0])
                }
            } else {
                this.value = null
            }
        }
        entrou = true;
        setTimeout(function() {
            entrou = false
        }, 1000)
    }
};
