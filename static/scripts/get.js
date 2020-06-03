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
  uuid = this.getAttribute('data-uuid');
  pk = this.getAttribute('data-id');
  loader = document.getElementById("create_loader");
  open_fullscreen('/users/load/img_load/' + uuid + '/', loader)
});

function is_full_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_two")){
    dropdown.style.display = "none";
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";
  }
  if (dropdown.classList.contains("files_one") || dropdown.classList.contains("files_null")){
    dropdown.style.display = "block"}
}
function add_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_null")){
    dropdown.classList.add("files_one"),
    dropdown.classList.remove("files_null")}
  else if(dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_two"), dropdown.classList.remove("files_one")};
}
function remove_file_dropdown(){
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (dropdown.classList.contains("files_one")){
    dropdown.classList.add("files_null"), dropdown.classList.remove("files_one")}
  else if(dropdown.classList.contains("files_two")){
    dropdown.classList.add("files_one"), dropdown.classList.remove("files_two")};
}

on('#ajax', 'click', '.upload_photo', function() {
  this.classList.add("current_file_dropdown");
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown();
  img_block = dropdown.parentElement.previousElementSibling.previousElementSibling;
  $div = document.createElement("div");
  $div.classList.add("col-md-6");

  if (img_block.querySelector(".comment_photo2")){
    $div.innerHTML = ''
  } else if (img_block.querySelector(".comment_photo1")){
    $div.innerHTML = '<div class="comment_photo2"><input class="file1 hide_image" name="photo2" accept="image/*" id="id_item_comment_photo2"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div>'
  } else{
    $div.innerHTML = '<div class="comment_photo1"><input class="file2 hide_image" name="photo" accept="image/*" id="id_item_comment_photo"><h4 class="svg_default"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div>'
  }
  img_block.append($div);
  add_file_dropdown()
  is_full_dropdown();
});

on('#ajax', 'click', '.delete_thumb', function(e) {
  e.preventDefault();
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  if (this.parentElement.querySelector("img")){
    remove_file_dropdown();
    is_full_dropdown();
  }
  this.parentElement.remove();
})

on('#ajax', 'click', '.photo_load_detail', function() {
  _this = this;
  dropdown = document.body.querySelector(".current_file_dropdown").parentElement.parentElement;
  is_full_dropdown(dropdown);
  _this.classList.add("photo_load_toggle");
  pk = _this.getAttribute('data-pk');
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');

  img_block = dropdown.parentElement.previousElementSibling.previousElementSibling;
  $div = document.createElement("div");
  $span = document.createElement("span");
  $span.innerHTML = '<svg class="svg_default" fill="currentColor" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
  $img = document.createElement("img");

  $div.classList.add("col-md-6");
  $div.setAttribute("data-uuid", uuid);
  $span.classList.add("photo_selected");
  $span.setAttribute("tooltip", "Не прикреплять");
  $span.setAttribute("flow", "up");
  $img.classList.add("u_photo_detail", "image_fit");
  $img.src = _this.getAttribute('data-src');
  $img.setAttribute('data-pk', pk);
  $div.append($span);
  $div.append($img);
  img_block.append($div);

  input_1 = img_block.querySelector(".input_select_photo");
  input_2 = img_block.querySelector(".input_select_photo2");
    if (input_2.value != "" && input_1.value != ""){
        is_full_dropdown(dropdown)}
    else if(input_2.value == "" && input_1.value != ""){
        input_2.value = pk}
    else if(input_2.value == "" && input_1.value == ""){
        input_1.value = pk}

  add_file_dropdown()
  is_full_dropdown();
});

on('#ajax', 'click', '.photo_selected', function() {
  pk = this.nextElementSibling.getAttribute("data-pk");
  parent = this.parentElement;
  input_1 = parent.parentElement.querySelector(".input_select_photo");
  input_2 = parent.parentElement.querySelector(".input_select_photo2");
  if (input_1.value == pk){input_1.value = ""}
  else if (input_2.value == pk){input_2.value = ""};
  parent.remove();

  remove_file_dropdown(dropdown);
  is_full_dropdown();
});


on('body', 'click', '.menu_drop', function() {var block = this.nextElementSibling;block.classList.toggle("show");});
