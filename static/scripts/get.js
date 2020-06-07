

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
window.addEventListener('popstate', function (e) {
    window.history.go(-1);
});
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
    console.log(photo_list[0]);
    console.log(photo_list[1]);
    if (img_block.querySelector(".select_photo2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_photo1")){
        $div1 = document.createElement("div");
        $div1.classList.add("col-md-6", "select_photo2");
        photo1_pk = photo_list[0].getAttribute("photo-pk");
        $input1 = document.createElement("span");
        $input1.innerHTML = '<input type="hidden" name="select_photo2" value="' + photo1_pk + '">';
        $span1 = document.createElement("span");
        $span1.innerHTML = '<svg class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
        $img1 = document.createElement("img");

        $span1.classList.add("item_preview_delete");
        $span1.setAttribute("tooltip", "Не прикреплять");
        $span1.setAttribute("flow", "up");
        $img1.classList.add("u_photo_detail", "image_fit");
        $img1.src = photo_list[0].querySelector("img").getAttribute('data-src');
        $img1.setAttribute('photo-pk', photo1_pk);
        $div1.append($span1);
        $div1.append($input1);
        $div1.append($img1);
        img_block.append($div1);
        add_file_dropdown();
        document.querySelector(".create_fullscreen").style.display = "none";
        document.getElementById("create_loader").innerHTML="";
      }
    else {
      $div1 = document.createElement("div");
      $div1.classList.add("col-md-6", "select_photo1");
      photo1_pk = photo_list[0].getAttribute("photo-pk");
      $input1 = document.createElement("span");
      $input1.innerHTML = '<input type="hidden" name="select_photo" value="' + photo1_pk + '">';
      $span1 = document.createElement("span");
      $span1.innerHTML = '<svg class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
      $img1 = document.createElement("img");

      $span1.classList.add("item_preview_delete");
      $span1.setAttribute("tooltip", "Не прикреплять");
      $span1.setAttribute("flow", "up");
      $img1.classList.add("u_photo_detail", "image_fit");
      $img1.src = photo_list[0].querySelector("img").getAttribute('data-src');
      $img1.setAttribute('photo-pk', photo1_pk);
      $div1.append($span1);
      $div1.append($input1);
      $div1.append($img1);
      img_block.append($div1);
      add_file_dropdown();

      try{
      $div2 = document.createElement("div");
      $div2.classList.add("col-md-6", "select_photo2");
      photo2_pk = photo_list[1].getAttribute("photo-pk");
      $input2 = document.createElement("span");
      $input2.innerHTML = '<input type="hidden" name="select_photo2" value="' + photo2_pk + '">';
      $span2 = document.createElement("span");
      $span2.innerHTML = '<svg class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
      $img2 = document.createElement("img");

      $span2.classList.add("item_preview_delete");
      $span2.setAttribute("tooltip", "Не прикреплять");
      $span2.setAttribute("flow", "up");
      $img2.classList.add("u_photo_detail", "image_fit");
      $img2.src = photo_list[1].querySelector("img").getAttribute('data-src');
      $img2.setAttribute('photo-pk', photo2_pk);
      $div2.append($span2);
      $div2.append($input2);
      $div2.append($img2);
      img_block.append($div2);
      add_file_dropdown();

    } catch { null }
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
      }
  }};
  link_.send(form_data);
});


on('#ajax', 'click', '.photo_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[photo-pk=' + '"' + _this.getAttribute('photo-pk') + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Изображение уже выбрано");
    _this.parentElement.setAttribute("flow", "up");
    return
  };

  _this.classList.add("photo_load_toggle");
  pk = _this.getAttribute('photo-pk');
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');

    $input = document.createElement("span");
    if (img_block.querySelector(".select_photo2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_photo1")){
        $div = document.createElement("div");
        $div.classList.add("col-md-6", "select_photo2");
        $input.innerHTML = '<input type="hidden" name="select_photo2" value="' + pk + '">';;
      }
    else {
        $div = document.createElement("div", "select_photo1");
        $div.classList.add("col-md-6", "select_photo1");
        $input.innerHTML = '<input type="hidden" name="select_photo" value="' + pk + '">';
      }

  $span = document.createElement("span");
  $span.innerHTML = '<svg class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $img = document.createElement("img");

  $div.setAttribute("data-uuid", uuid);
  $span.classList.add("item_preview_delete");
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  $img.classList.add("u_photo_detail", "image_fit");
  $img.src = _this.getAttribute('data-src');
  $img.setAttribute('photo-pk', pk);
  $div.append($span);
  $div.append($input);
  $div.append($img);
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});

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

        $input = document.createElement("span");
        if (img_block.querySelector(".select_video2")){
            is_full_dropdown()}
        else if (img_block.querySelector(".select_video1")){
            $div = document.createElement("div");
            $div.classList.add("col-md-6", "select_video2");
            $input.innerHTML = '<input type="hidden" name="select_video2" value="' + pk + '">';
          }
        else {
            $div = document.createElement("div", "select_video1");
            $div.classList.add("col-md-6", "select_video1");
            $input.innerHTML = '<input type="hidden" name="select_video" value="' + pk + '">';
          }

      $span = document.createElement("span");
      $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
      $img = document.createElement("img");
      $icon_div = document.createElement("div");

      $span.classList.add("item_preview_delete");
      $span.setAttribute("tooltip", "Не прикреплять");
      $span.setAttribute("flow", "up");
      $img.classList.add("image_fit");
      $img.src = elem_.querySelector("img").getAttribute('data-src');
      $icon_div.classList.add("video_icon_play_v2", "u_video_list_detail");
      $icon_div.setAttribute("video-counter", "0");

      $div.append($span);
      $div.append($input);
      $div.append($img);
      $div.append($icon_div);
      img_block.append($div);

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

  if (img_block.querySelector( '[video-counter=' + '"' + _this.getAttribute('video-counter') + '"' + ']' )){
    _this.parentElement.setAttribute("tooltip", "Видеоролик уже выбран");
    _this.parentElement.setAttribute("flow", "up");
    return
  };

  pk = _this.getAttribute('data-pk');

    $input = document.createElement("span");
    if (img_block.querySelector(".select_video2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_video1")){
        $div = document.createElement("div");
        $div.classList.add("col-md-6", "select_video2");
        $input.innerHTML = '<input type="hidden" name="select_video2" value="' + pk + '">';
      }
    else {
        $div = document.createElement("div", "select_video1");
        $div.classList.add("col-md-6", "select_video1");
        $input.innerHTML = '<input type="hidden" name="select_video" value="' + pk + '">';
      }

  $span = document.createElement("span");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $img = document.createElement("img");
  $icon_div = document.createElement("div");

  $span.classList.add("item_preview_delete");
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  $img.classList.add("image_fit");
  $img.src = _this.getAttribute('data-src');
  $icon_div.classList.add("video_icon_play_v2", "u_video_list_detail");
  $icon_div.setAttribute("video-counter", _this.getAttribute('video-counter'));

  $div.append($span);
  $div.append($input);
  $div.append($img);
  $div.append($icon_div);
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});

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

  media_body = _this.querySelector(".media-body");
  pk = _this.getAttribute('data-pk');

  _this.classList.add("music_load_toggle");

    $input = document.createElement("span");
    if (img_block.querySelector(".select_music2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_music1")){
        $div = document.createElement("div");
        $div.classList.add("col-md-12", "select_music2");
        $input.innerHTML = '<input type="hidden" name="select_music2" value="' + pk + '">';
      }
    else {
        $div = document.createElement("div", "select_music1");
        $div.classList.add("col-md-12", "select_music1");
        $input.innerHTML = '<input type="hidden" name="select_music" value="' + pk + '">';
      }
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.setAttribute('music-counter', counter);

  $span = document.createElement("span");
  $img = document.createElement("img");
  $media = document.createElement("div");
  $figure = document.createElement("figure");

  $span.classList.add("item_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");

  $img.src = _this.querySelector("img").getAttribute('data-src');
  $img.style.width = "50px";
  $figure.append($img);

  $media.innerHTML = media_body.innerHTML;
  $media.style.marginLeft = "10px";
  h6 = $media.querySelector("h6");
  h6.classList.add("music_list_item");

  $div.append($span);
  $div.append($input);
  $div.append($figure);
  $div.append($media);
  img_block.append($div);

  add_file_dropdown()
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
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');

    $input = document.createElement("span");
    $span = document.createElement("span");
    $img = document.createElement("img");
    $info = document.createElement("span");

    if (img_block.querySelector(".select_good2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_good1")){
        $div = document.createElement("div");
        $div.classList.add("col-md-6", "select_good2");
        $input.innerHTML = '<input type="hidden" name="select_good2" value="' + pk + '">';;
      }
    else {
        $div = document.createElement("div", "select_good1");
        $div.classList.add("col-md-6", "select_good1");
        $input.innerHTML = '<input type="hidden" name="select_good" value="' + pk + '">';
      }

  $div.setAttribute('good-pk', pk);
  $div.style.cursor = "pointer";
  $div.style.padding = "5px";
  $div.classList.add("u_good_detail");

  $span.innerHTML = '<svg class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.classList.add("item_preview_delete");
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");

  $img.classList.add("image_fit");
  $img.src = _this.querySelector("img").getAttribute('data-src');

  $info.innerHTML = _this.querySelector(".good_info").innerHTML;
  $div.append($span);
  $div.append($input);
  $div.append($img);
  $div.append($info);
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});

on('#ajax', 'click', '.article_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);
  uuid = _this.getAttribute('item-uuid');
  img_block = dropdown.parentElement.previousElementSibling;

  if (img_block.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' )){
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

  $div.setAttribute('data-uuid', uuid);
  $div.style.cursor = "pointer";

  $span = document.createElement("span");
  $img = document.createElement("img");
  $img.style.width = "100%";
  $media = document.createElement("div");
  $figure = document.createElement("figure");
  $figure.classList.add("u_article_detail");

  $span.classList.add("item_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");

  $img.src = _this.querySelector("img").getAttribute('data-src');
  $figure.append($img);

  $media.innerHTML = media_body.innerHTML;

  $div.append($span);
  $div.append($input);
  $div.append($figure);
  //$div.append($media);
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});
