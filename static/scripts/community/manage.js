
on('#ajax', 'click', '#community_private_post_btn', function() {
  form = document.querySelector("#community_private_post_form");
  pk = rtr.querySelector(".pk_saver").getAttribute("data-pk");
  form_data = new FormData(form);
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/communities/manage/private_post/', true );
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            toast_info("Изменения приняты!");
        }
      }
      ajax_link.send(form_data);
});

document.querySelector(".add_staff_options").addEventListener("click", (e) => {
    var uuid = '{{ user.uuid }}';
    var pk = {{ community.pk }};
    if (document.getElementById('user_moderator').checked) {
    {% if not moderator %}
      fetch("/communities/progs/add_moderator/" + pk + "/" + uuid + "/").then(data => {
      document.querySelector(".manage_window_fullscreen").style.display = "none";
      document.getElementById('load_staff_window').innerHTML = "";
      li = document.querySelector(".li_{{user.pk }}");
      staff_btn = li.querySelector(".staff_btn");
      staff_btn.innerHTML = "<span class='staff_btn'>Модератор<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_moderator' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")});
    {% else %}
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    {% endif %}
  }else if(document.getElementById('user_editor').checked){
    {% if not editor %}
    fetch("/communities/progs/add_editor/" + pk + "/" + uuid + "/").then(data => {
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    li = document.querySelector(".li_{{user.pk }}");
    staff_btn = li.querySelector(".staff_btn");
    staff_btn.innerHTML = "<span class='staff_btn'>Редактор<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_editor' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")});
    {% else %}
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    {% endif %}}else if(document.getElementById('user_administrator').checked){
    {% if not administrator %}
    fetch("/communities/progs/add_admin/" + pk + "/" + uuid + "/").then(data => {
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    li = document.querySelector(".li_{{user.pk }}");
    staff_btn = li.querySelector(".staff_btn");
    staff_btn.innerHTML = "<span class='staff_btn'>Администратор<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_admin' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")});
    {% else %}
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    {% endif %}}else if(document.getElementById('user_advertiser').checked){
    {% if not advertiser %}
    fetch("/communities/progs/add_advertiser/" + pk + "/" + uuid + "/").then(data => {
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    li = document.querySelector(".li_{{user.pk }}");
    staff_btn = li.querySelector(".staff_btn");
    staff_btn.innerHTML = "<span class='staff_btn'>Рекламодатель<br><span class='small'><span class='show_staff_window' style='cursor:pointer'>Редактировать</span> | <span class='remove_advertiser' style='cursor:pointer'>Разжаловать</span></span><br></span>";
    }).catch(error => {console.log("Все не ОК")});
    {% else %}
    document.querySelector(".manage_window_fullscreen").style.display = "none";
    document.getElementById('load_staff_window').innerHTML = "";
    {% endif %}
  };
});
