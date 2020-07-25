on('#ajax', 'click', '.u_soundcloud_set_create', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_create_list_window/" + pk, loader)
});
on('#ajax', 'click', '.u_soundcloud_set_list', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen("/music/user_progs/souncloud_list_window/" + pk, loader)
});

on('#ajax', 'click', '#soundcloud_set_create_btn', function() {
  form = document.body.querySelector("#soundcloud_set_create_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!");
  }
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/user_progs/create_soundcloud_set_create/" + pk + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;

        uuid = rtr.querySelector(".pk_saver").getAttribute("data-uuid");
        window.history.pushState(null, "vfgffgfgf", '/users/detail/music_list/' + pk + "/" + uuid + '/');
      }
    }
    ajax_link.send(form_data);
});
on('#ajax', 'click', '#soundcloud_set_btn', function() {
  form = document.body.querySelector("#soundcloud_set_form");
  form_data = new FormData(form);
  if (!form.querySelector("#id_permalink").value){
    form.querySelector("#id_permalink").style.border = "1px #FF0000 solid";
    toast_error("Ссылка - обязательное поле!");
  }
  saver = document.body.querySelector(".pk_saver");
  pk = saver.getAttribute("data-pk");
  uuid = saver.getAttribute("data-uuid");

  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/music/user_progs/create_soundcloud_set_create/" + pk + "/" + uuid + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        document.querySelector(".create_fullscreen").style.display = "none";
        document.getElementById("create_loader").innerHTML="";
      }
    }
    ajax_link.send(form_data);
});
