on('#ajax', 'click', '.u_photo_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  //uuid = this.getAttribute('photo-uuid');
  data_img = this.getAttribute("src");
  data_img.substr(8,);
  console.log(data_img);
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.avatar_detail', function() {
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  uuid = this.getAttribute('photo-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/avatar/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_album_photo_detail', function() {
  container = this.parentElement;
  document.body.querySelector(".pk_saver") ? uuid = document.body.querySelector(".pk_saver").getAttribute('album-uuid') : uuid = this.getAttribute('album-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/album_photo/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_wall_image', function() {
  uuid = this.getAttribute('data-uuid');
  document.body.querySelector(".pk_saver") ? pk = document.body.querySelector(".pk_saver").getAttribute('data-pk') : pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/wall/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '.u_albums_add', function() {
  var container, uuid, loader;
  container = this.parentElement;
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/gallery/user/add_album/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})


on('#ajax', 'click', '#add_album', function() {
  form = document.body.querySelector("#form_album_add");
  form_data = new FormData(form);
  if (!form.querySelector("#id_title").value){
    form.querySelector("#id_title").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else { null }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/gallery/user/add_album/" + pk + "/", true );
    ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        uuid = rtr.querySelector(".pk_saver").getAttribute("album-uuid");
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;
        window.history.pushState(null, "vfgffgfgf", '/gallery/user/album/' + pk + '/' + uuid + '/');
        toast_info("Альбом изображений создан!");
        album_photo_load =  rtr.querySelector("#album_photo_load");
        list_load(album_photo_load, album_photo_load.getAttribute("data-link"));
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'click', '.u_all_photo_likes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('photo-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_like/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_all_photo_dislikes', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('photo-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_dislike/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_all_photo_comment_likes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_comment_like/" + pk + "/", loader)
});
on('#ajax', 'click', '.u_all_photo_comment_dislikes', function() {
  container = this.parentElement.parentElement.parentElement;
  pk = container.getAttribute('data-pk');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_comment_dislike/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_all_photo_reposts', function() {
  container = this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
  uuid = container.getAttribute('data-uuid');
  loader = document.getElementById("votes_loader");
  open_fullscreen("/gallery/window/all_user_reposts/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_photo_comments', function() {
  clear_comment_dropdown();
  data = document.body.querySelector(".data_display");
  pk = data.getAttribute("user-pk");
  uuid = data.getAttribute("data-uuid");
  url = "/gallery/user_progs/comment/" + uuid + "/" + pk + "/";
  list_load(data.querySelector(".u_load_comments"), url);
  this.classList.toggle("comments_open");
});
