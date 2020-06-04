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

on('#ajax', 'click', '#add_board_hide', function() {
  document.querySelector('#for_settings').style.display = "block";
});
on('#ajax', 'click', '#images_upload', function() {
  document.querySelector('#for_images_upload').style.display = "block";
});
on('#ajax', 'click', '#settings', function() {
  document.querySelector('#for_settings').style.display = "block";
});
on('#ajax', 'click', '#gallery', function() {
  document.querySelector('#for_gallery').style.display = "block";
});
on('#ajax', 'click', '#doc', function() {
  document.querySelector('#for_doc').style.display = "block";
});
on('#ajax', 'click', '#good', function() {
  document.querySelector('#for_good').style.display = "block";
});
on('#ajax', 'click', '#question', function() {
  document.querySelector('#for_question').style.display = "block";
});

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
  pk = this.getAttribute('data-id');
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


on('#ajax', 'click', '.upload_photo', function() {
  this.classList.add("current_file_dropdown");
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling;
  $div = document.createElement("div");
  $div.classList.add("col-md-6");
  console.log(img_block);

  if (img_block.querySelector(".comment_photo2")){
    $div.innerHTML = ''
  } else if (img_block.querySelector(".comment_photo1")){
    $div.innerHTML = '<div class="comment_photo2"><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><span id="photo2"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></span></div>'
  } else{
    $div.innerHTML = '<div class="comment_photo1"><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><span id="photo"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></span></div>'
  }
  img_block.append($div);
  is_full_dropdown();
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (this.parentElement.querySelector("img")){
    remove_file_dropdown();
    is_full_dropdown();
  }
  this.parentElement.parentElement.parentElement.remove();
})

on('#ajax', 'click', '.photo_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  if (img_block.querySelector(".comment_photo1")){
    comment_photo1 = img_block.querySelector(".comment_photo1");
    if (!comment_photo1.querySelector("img")){
      comment_photo1.parentElement.remove();
    }
  }
  if (img_block.querySelector(".comment_photo2")){
    comment_photo2 = img_block.querySelector(".comment_photo2");
    if (!comment_photo2.querySelector("img")){
      comment_photo2.parentElement.remove();
    }
  }

  _this.classList.add("photo_load_toggle");
  pk = _this.getAttribute('data-pk');
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');

    $input = document.createElement("span");
    if (img_block.querySelector(".select_photo2")){
        is_full_dropdown()}
    else if (img_block.querySelector(".select_photo1")){
        $div = document.createElement("div");
        $div.classList.add("col-md-6", "select_photo2");
        $input.innerHTML = '<input type="hidden" name="select_photo2" value="' + pk + '">';
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
  $img.setAttribute('data-pk', pk);
  $div.append($span);
  $div.append($input);
  $div.append($img);
  img_block.append($div);

  add_file_dropdown()
  is_full_dropdown();
});

on('#ajax', 'click', '.video_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);
  img_block = dropdown.parentElement.previousElementSibling;
  if (img_block.querySelector(".comment_photo1")){
    comment_photo1 = img_block.querySelector(".comment_photo1");
    if (!comment_photo1.querySelector("img")){
      comment_photo1.parentElement.remove();
    }
  }
  if (img_block.querySelector(".comment_photo2")){
    comment_photo2 = img_block.querySelector(".comment_photo2");
    if (!comment_photo2.querySelector("img")){
      comment_photo2.parentElement.remove();
    }
  }

  _this.classList.add("video_load_toggle");
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
  $icon_div.classList.add("video_icon_play_v2", "u_video_detail");
  $icon_div.setAttribute("data-counter", _this.getAttribute('data-counter'));

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
  img_block = dropdown.parentElement.previousElementSibling;
  media_body = _this.querySelector(".media-body");
  pk = _this.getAttribute('data-pk');

  if (img_block.querySelector(".comment_photo1")){
    comment_photo1 = img_block.querySelector(".comment_photo1");
    if (!comment_photo1.querySelector("img")){
      comment_photo1.parentElement.remove();
    }
  }
  if (img_block.querySelector(".comment_photo2")){
    comment_photo2 = img_block.querySelector(".comment_photo2");
    if (!comment_photo2.querySelector("img")){
      comment_photo2.parentElement.remove();
    }
  }

  _this.classList.add("music_load_toggle");
  counter = _this.getAttribute('data-counter');

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
        $div.classList.add("col-md-12", "select_video1");
        $input.innerHTML = '<input type="hidden" name="select_music" value="' + pk + '">';
      }
  $div.style.display = "flex";
  $div.style.margin = "5px";
  $div.setAttribute('data-counter', counter);

  $span = document.createElement("span");
  $img = document.createElement("img");
  $media = document.createElement("div");
  $figure = document.createElement("figure");
  $figure.classList.add("music_list_item");

  $span.classList.add("item_preview_delete");
  $span.innerHTML = '<svg fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");

  $img.src = _this.querySelector("img").getAttribute('data-src');
  $img.style.width = "50px";
  $figure.append($img);

  $media.innerHTML = media_body.innerHTML;
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
