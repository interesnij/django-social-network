on('#ajax', 'click', '.show_staff_window', function() {
  var parent, pk, uuid, loader
  parent = this.parentElement.parentElement.parentElement.parentElement.parentElement;
  pk = parent.getAttribute("data-pk");
  uuid = parent.getAttribute("data-uuid");
  loader = document.getElementById("load_staff_window");
  open_fullscreen("/communities/manage/staff_window/" + pk + "/" + uuid + "/", loader)
});

on('#ajax', 'click', '.community_follow_view', function() {
    li = this.parentElement.parentElement.parentElement.parentElement;
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    uuid = li.getAttribute("data-uuid");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/follows/community_view/" + pk + "/" + uuid + "/", true );
    link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        li.remove()
      }};
  link.send( null );
});
on('#ajax', 'click', '.community_member_create', function() {
    li = this.parentElement.parentElement.parentElement.parentElement;
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    uuid = li.getAttribute("data-uuid");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/communities/progs/manager_add_member/" + pk + "/" + uuid + "/", true );
    link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        li.remove()
      }};
  link.send( null );
});
on('#ajax', 'click', '.community_member_delete', function() {
    li = this.parentElement.parentElement.parentElement.parentElement;
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    uuid = li.getAttribute("data-uuid");
    link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/communities/progs/manager_delete_member/" + pk + "/" + uuid + "/", true );
    link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        li.remove()
      }};
  link.send( null );
});

on('#ajax', 'click', '#community_private_post_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/private_post/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_private_post_form"), "Изменения приняты!")
});
on('#ajax', 'click', '#community_private_photo_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/private_photo/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_private_photo_form"), "Изменения приняты!")
});
on('#ajax', 'click', '#community_private_good_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/private_good/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_private_good_form"), "Изменения приняты!")
});
on('#ajax', 'click', '#community_private_video_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/private_video/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_private_video_form"), "Изменения приняты!")
});

on('#ajax', 'click', '#community_notify_post_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/notify_post/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_notify_post_form"), "Изменения приняты!")
});
on('#ajax', 'click', '#community_notify_photo_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/notify_photo/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_notify_photo_form"), "Изменения приняты!")
});
on('#ajax', 'click', '#community_notify_good_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/notify_good/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_notify_good_form"), "Изменения приняты!")
});
on('#ajax', 'click', '#community_notify_video_btn', function() {
  send_form_with_pk_and_toast('/communities/manage/notify_video/' + document.body.querySelector(".pk_saver").getAttribute("data-pk") + "/", document.body.querySelector("#community_notify_video_form"), "Изменения приняты!")
});

on('#ajax', 'click', '.add_staff_options', function() {
    uuid = this.getAttribute("data-uuid");
    status = this.getAttribute("data-status");
    pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
    if (document.getElementById('user_moderator').checked) {
    status == "moderator" ?
      fetch("/communities/progs/add_moderator/" + pk + "/" + uuid + "/").then(data => {
      document.querySelector(".manage_window_fullscreen").style.display = "none";
      document.getElementById('load_staff_window').innerHTML = "";
      li = document.querySelector(".li_{{user.pk }}");
      staff_btn = li.querySelector(".staff_btn");
      staff_btn.innerHTML = "<span class='staff_btn'>Модератор<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_moderator' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")})
    :
    (document.querySelector(".manage_window_fullscreen").style.display = "none",
    document.getElementById('load_staff_window').innerHTML = "")
  }else if(document.getElementById('user_editor').checked){
    status == "editor" ?
    fetch("/communities/progs/add_editor/" + pk + "/" + uuid + "/").then(data => {
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    li = document.querySelector(".li_{{user.pk }}");
    staff_btn = li.querySelector(".staff_btn");
    staff_btn.innerHTML = "<span class='staff_btn'>Редактор<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_editor' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")})
    :
    (document.querySelector(".manage_window_fullscreen").style.display = "none",
    document.getElementById('load_staff_window').innerHTML = "")}
    else if(document.getElementById('user_administrator').checked){
    status == "administrator" ?
    fetch("/communities/progs/add_admin/" + pk + "/" + uuid + "/").then(data => {
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    li = document.querySelector(".li_{{user.pk }}");
    staff_btn = li.querySelector(".staff_btn");
    staff_btn.innerHTML = "<span class='staff_btn'>Администратор<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_admin' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")})
    :
    (document.querySelector(".manage_window_fullscreen").style.display = "none",
    document.getElementById('load_staff_window').innerHTML = "")
    }else if(document.getElementById('user_advertiser').checked){
    status == "advertiser" ?
    fetch("/communities/progs/add_advertiser/" + pk + "/" + uuid + "/").then(data => {
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    li = document.querySelector(".li_{{user.pk }}");
    staff_btn = li.querySelector(".staff_btn");
    staff_btn.innerHTML = "<span class='staff_btn'>Рекламодатель<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_advertiser' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")})
    :
    (document.querySelector(".manage_window_fullscreen").style.display = "none",
    document.getElementById('load_staff_window').innerHTML = "")
  };
});
