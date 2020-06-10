on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});

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
    else if (img_block.querySelector(".select_photo2") || !img_block.querySelector(".select_photo1")){
      div = create_preview_photo("select_photo1", photo_list[0].querySelector("img").getAttribute('data-src'), photo_list[0].getAttribute("photo-uuid"))
      img_block.append(div);
      add_file_dropdown();
      document.querySelector(".create_fullscreen").style.display = "none";
      document.getElementById("create_loader").innerHTML="";
    }
    else if (!img_block.querySelector(".select_photo2") || !img_block.querySelector(".select_photo1")){
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
    if (img_block.querySelector(".select_photo1")){
        div = create_preview_photo("select_photo2", _this.getAttribute('data-src'), pk)
      }
    else if (img_block.querySelector(".select_photo2") || !img_block.querySelector(".select_photo1")){
        div = create_preview_photo("select_photo1", _this.getAttribute('data-src'), pk)
      }
  img_block.append(div);

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
        if (img_block.querySelector(".select_video1")){
            div = create_preview_video("select_video2", elem_.querySelector("img").getAttribute('data-src'), pk)
          }
        else if (img_block.querySelector(".select_video2") || !img_block.querySelector(".select_video1")){
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
  video_comment_attach(_this, dropdown);
});

on('#ajax', 'click', '.music_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  music_comment_attach(_this, dropdown)
});

on('#ajax', 'click', '.item_preview_delete', function() {
  pk = this.nextElementSibling.getAttribute("data-pk");
  parent = this.parentElement;
  parent.remove();

  remove_file_dropdown(dropdown);
  is_full_dropdown();
});

on('#ajax', 'click', '.good_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  good_comment_attach(_this, dropdown)
});

on('#ajax', 'click', '.article_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  article_comment_attach(_this, dropdown)
});
