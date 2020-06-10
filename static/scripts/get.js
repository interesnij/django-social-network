
on('body', 'click', '#add_multi_comments_photos', function(event) {
  this.previousElementSibling.click();
})

on('body', 'click', '.ajax', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  if (url != window.location.pathname){
    ajax_get_reload(url);
  }
})

//window.addEventListener('popstate', function (e) {window.history.go(-1);});

on('body', 'click', '.next_item', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('item_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})
on('body', 'click', '.prev_item', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('item_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})

on('body', 'click', '.next_photo', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('photo_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})
on('body', 'click', '.prev_photo', function(event) {
  event.preventDefault();
  var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        rtr = document.getElementById('photo_loader');
        rtr.innerHTML = elem_.innerHTML;
      }
    }
    ajax_link.send();
})

on('#ajax', 'click', '.item_stat_f', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = parent.getAttribute("item-uuid");
  loader = document.getElementById("stat_loader");
  open_fullscreen("/stat/item/" + uuid + "/", loader)
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

// END FULLSCREENS //
//--------------------------------------------------------------------//

on('#ajax', 'click', '.show_replies', function() {
  this.nextElementSibling.classList.toggle('replies_open');
});

on('#ajax', 'click', '.reply_comment', function() {
  var objectUser = this.previousElementSibling.innerHTML;
  var form = this.nextElementSibling.querySelector(".text-comment");
  form.value = objectUser + ', ';
  this.nextElementSibling.style.display = "block";
  form.focus();
})

on('#ajax', 'click', '.comment_image', function() {
  var uuid, pk, loader;
  pk = this.getAttribute('photo-pk');
  uuid = this.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/comment/" + pk + "/" + uuid + "/", loader)
});


on('#ajax', 'click', '.select_photo', function() {
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/img_load/', loader)
});
on('#ajax', 'click', '.select_video', function() {
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/video_load/', loader)
});
on('#ajax', 'click', '.select_music', function() {
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/music_load/', loader)
});
on('#ajax', 'click', '.select_good', function() {
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/good_load/', loader)
});
on('#ajax', 'click', '.select_article', function() {
  this.classList.add("current_file_dropdown");
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/article_load/', loader)
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  this.nextElementSibling.remove();
  block = document.createElement("div");
  this.parentElement.innerHTML = "<h4>Изображение</h4><i>(обязательно)</i>";
  this.remove();
})


on('#ajax', 'change', '#photo_add_attach', function() {
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(document.body.querySelector("#add_photos"));
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/gallery/user/add_comment_photo/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    response = document.createElement("span");
    response.innerHTML = elem;
    photo_list = response.querySelectorAll(".u_photo_detail");
    if (img_block.querySelector(".select_photo1")){
      div = create_preview_photo("select_photo2", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
      img_block.append(div);
      add_file_dropdown();
      document.querySelector(".create_fullscreen").style.display = "none";
      document.getElementById("create_loader").innerHTML="";
      }
    else if (img_block.querySelector(".select_photo2") && !img_block.querySelector(".select_photo1")){
      div = create_preview_photo("select_photo1", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
      img_block.append(div);
      add_file_dropdown();
      document.querySelector(".create_fullscreen").style.display = "none";
      document.getElementById("create_loader").innerHTML="";
    }
    else {
      div = create_preview_photo("select_photo1", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
      img_block.append(div);
      add_file_dropdown();
      if (dropdown.classList.contains("files_two")){
        document.querySelector(".create_fullscreen").style.display = "none";
        document.getElementById("create_loader").innerHTML="";
        return
      }
      create_preview_photo("select_photo2", photo_list[1].querySelector("img").getAttribute('data-src'), photo_list[1].getAttribute("photo-uuid"))
      add_file_dropdown();
      is_full_dropdown();
    }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
      }
  };
  link_.send(form_data);
});

on('#ajax', 'click', '.photo_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[photo-uuid=' + '"' + _this.getAttribute('photo-uuid') + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
    _this.parentElement.setAttribute("flow", "up");
    return
  };

  _this.classList.add("photo_load_toggle");
  pk = _this.getAttribute('photo-uuid');

    $input = document.createElement("span");
    if (img_block.querySelector(".select_photo1")){
        div = create_preview_photo("select_photo2", _this.getAttribute('data-src'), pk)
      }
    else if (img_block.querySelector(".select_photo2") && !img_block.querySelector(".select_photo1")){
        div = create_preview_photo("select_photo1", _this.getAttribute('data-src'), pk)
      }
    else {
      div = create_preview_photo("select_photo1", _this.getAttribute('data-src'), pk)
    }
  img_block.append(div);

  add_file_dropdown()
  is_full_dropdown();
});

function create_preview_photo(div_class, img_src, pk){
  $div = document.createElement("div");
  $div.classList.add("col-md-6", div_class);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $img.classList.add("u_photo_detail", "image_fit");
  $img.src = img_src;
  $img.setAttribute('photo-uuid', pk);
  $div.append(get_delete_span());
  $div.append($input);
  $div.append($img);
  return $div
}

function create_preview_video(div_class, img_src, pk, counter){
  $div = document.createElement("div");
  $div.classList.add("col-md-6", div_class);
  $input = document.createElement("span");
  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $icon_div = document.createElement("div");
  $img.classList.add("image_fit");
  $img.src = img_src;
  $icon_div.classList.add("video_icon_play_v2", "u_video_list_detail");
  $icon_div.setAttribute("video-counter", counter);

  $div.append(get_delete_span());
  $div.append($input);
  $div.append($img);
  $div.append($icon_div);
  return $div
}

on('#ajax', 'click', '.create_video_attach_btn', function() {
  form_data = new FormData(document.querySelector("#create_video_form"));

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/video/progs/create_video_attach/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
    is_full_dropdown(dropdown);
    img_block = dropdown.parentElement.previousElementSibling;

      elem_ = document.createElement('div');
      elem_.innerHTML = link_.responseText;

      pk = elem_.querySelector("img").getAttribute('data-pk');
        if (img_block.querySelector(".select_video1")){
            div = create_preview_video("select_video2", elem_.querySelector("img").getAttribute('data-src'), pk)
          }
        else if (img_block.querySelector(".select_video2") && !img_block.querySelector(".select_video1")){
            div = create_preview_video("select_video1", elem_.querySelector("img").getAttribute('data-src'), pk)
          }
      img_block.append(div);

      add_file_dropdown()
      is_full_dropdown();
      document.querySelector(".create_fullscreen").style.display = "none";
      document.getElementById("create_loader").innerHTML="";
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.video_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  counter = _this.getAttribute('video-counter');
  if (img_block.querySelector( '[video-counter=' + '"' + counter + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Видеоролик уже выбран");
    _this.parentElement.setAttribute("flow", "up");
    return
  };

  pk = _this.getAttribute('data-pk');

    if (img_block.querySelector(".select_video1")){
        create_preview_video("select_video2", _this.getAttribute('data-src'), pk, counter)
      }
    else if (img_block.querySelector(".select_video2") || !img_block.querySelector(".select_video1")){
        create_preview_video("select_video1", _this.getAttribute('data-src'), pk, counter)
      }
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});


function create_preview_music(div_class, img_src, pk, counter){
  $div = document.createElement("div");
  $input = document.createElement("span");
  $img = document.createElement("img");
  $figure = document.createElement("figure");
  $media = document.createElement("div");

  media_body = _this.querySelector(".media-body");

  $div.classList.add("col-md-12", div_class);
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.setAttribute('music-counter', counter);

  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';

  $img.src = img_src;
  $img.style.width = "50px";
  $figure.append($img);

  $media.innerHTML = media_body.innerHTML;
  $media.style.marginLeft = "10px";
  h6 = $media.querySelector("h6");
  h6.classList.add("music_list_item");

  $div.append(get_delete_span());
  $div.append($input);
  $div.append($figure);
  $div.append($media);

  return $div
}

on('#ajax', 'click', '.music_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);

  counter = _this.getAttribute('music-counter');
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[music-counter=' + '"' + counter + '"' + ']' )){
    _this.setAttribute("tooltip", "Аудиозапись уже выбрана");
    _this.setAttribute("flow", "up");
    return
  };

  _this.classList.add("music_load_toggle");

    $input = document.createElement("span");
    if (img_block.querySelector(".select_music1")){
        div = create_preview_music("select_music2", _this.querySelector("img").getAttribute('data-src'), _this.getAttribute('data-pk'), _this.getAttribute('music-counter') )
        img_block.append(div); add_file_dropdown();
      }
    else if (img_block.querySelector(".select_music2") || !img_block.querySelector(".select_music1")){
        div = create_preview_music("select_music1", _this.querySelector("img").getAttribute('data-src'), _this.getAttribute('data-pk'), _this.getAttribute('music-counter') )
        img_block.append(div); add_file_dropdown();
      }
    else{ return };

  is_full_dropdown();
});

on('#ajax', 'click', '.item_preview_delete', function() {
  pk = this.nextElementSibling.getAttribute("data-pk");
  parent = this.parentElement;
  parent.remove();

  remove_file_dropdown(dropdown);
  is_full_dropdown();
});

on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});


function create_preview_good(div_class, img_src, pk, title){
  $div = document.createElement("div");
  $div.classList.add("col-md-6", div_class);
  $div.setAttribute('good-pk', pk);
  $div.style.cursor = "pointer";
  $div.classList.add("u_good_detail");

  $input = document.createElement("span");
  $title = document.createElement("span");
  $title.innerHTML = '<span class="badge badge-info mb-2" style="position: absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M17.21 9l-4.38-6.56c-.19-.28-.51-.42-.83-.42-.32 0-.64.14-.83.43L6.79 9H2c-.55 0-1 .45-1 1 0 .09.01.18.04.27l2.54 9.27c.23.84 1 1.46 1.92 1.46h13c.92 0 1.69-.62 1.93-1.46l2.54-9.27L23 10c0-.55-.45-1-1-1h-4.79zM9 9l3-4.4L15 9H9zm3 8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/></svg>' + title + '</span>'

  $input.innerHTML = '<input type="hidden" name="' + div_class + '" value="' + pk + '">';
  $img = document.createElement("img");
  $img.classList.add("image_fit");
  $img.src = img_src;

  $div.append(get_delete_span());
  $div.append($input);
  $div.append($title);
  $div.append($img);
  return $div
}

on('#ajax', 'click', '.good_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[good-pk=' + '"' + _this.getAttribute('good-pk') + '"' + ']' )){
    _this.setAttribute("tooltip", "Товар уже выбран");
    _this.setAttribute("flow", "up");
    return
  };

  _this.classList.add("good_load_toggle");
  pk = _this.getAttribute('good-pk');
  title = _this.querySelector(".good_title").innerHTML;

    if (img_block.querySelector(".select_good1")){
      div = create_preview_good("select_good2", _this.querySelector("img").getAttribute('data-src'), pk, _this.querySelector(".good_title").innerHTML)
    }
    else if (img_block.querySelector(".select_good2") && !img_block.querySelector(".select_good1")){
      div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, _this.querySelector(".good_title").innerHTML)
    }
    else {
      div = create_preview_good("select_good1", _this.querySelector("img").getAttribute('data-src'), pk, _this.querySelector(".good_title").innerHTML)
    }

  img_block.append(div);

  add_file_dropdown()
  is_full_dropdown();
});

on('#ajax', 'click', '.article_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);
  uuid = _this.getAttribute('item-uuid');
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[item-uuid=' + '"' + uuid + '"' + ']' )){
    _this.setAttribute("tooltip", "Статья уже выбрана");
    _this.setAttribute("flow", "up");
    return
  };

  media_body = _this.querySelector(".article_info");

  _this.classList.add("attach_toggle");

    $input = document.createElement("span");
    if (img_block.querySelector(".select_article2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_article1")){
        $div = document.createElement("div");
        $div.classList.add("col-md-6", "select_article2");
        $input.innerHTML = '<input type="hidden" name="select_article2" value="' + uuid + '">';
      }
    else {
        $div = document.createElement("div", "select_article1");
        $div.classList.add("col-md-6", "select_article1");
        $input.innerHTML = '<input type="hidden" name="select_article" value="' + uuid + '">';
      }
  $title = document.createElement("span");
  $div.setAttribute('item-uuid', uuid);
  $div.style.cursor = "pointer";

  $img = document.createElement("img");
  $img.style.width = "100%";
  $img.classList.add("image_fit");
  $p = document.createElement("p");
  $figure = document.createElement("figure");
  $figure.classList.add("u_article_detail");

  $img.src = _this.querySelector("img").getAttribute('data-src');
  $figure.append($img);

  title = _this.querySelector(".article_title").innerHTML;
  $title.innerHTML = '<span class="badge badge-info mb-2" style="position: absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>'
     + title + '</span>'

  $div.append(get_delete_span());
  $div.append($input);
  $div.append($figure);
  $div.append($title);
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});
