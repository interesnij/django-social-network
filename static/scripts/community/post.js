on('#ajax', 'click', '#add_community_btn', function() {
  form = document.querySelector("#add_community_form");
  if (!form.querySelector("#id_name").value){
    form.querySelector("#id_name").style.border = "1px #FF0000 solid";
    toast_error("Название - обязательное поле!");
  } else if (!form.querySelector("#sub_category").value){
    form.querySelector("#sub_category").style.border = "1px #FF0000 solid";
    toast_error("Тематика - обязательное поле!")
  } else {toast_info("Сообщество создано!")};

  	form_data = new FormData(form);
    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/communities/progs/add/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            elem_ = document.createElement('span');
            elem_.innerHTML = ajax_link.responseText;
            ajax = elem_.querySelector("#reload_block");
            rtr = document.getElementById('ajax');
            rtr.innerHTML = ajax.innerHTML;
            pk = rtr.querySelector(".pk_saver").getAttribute("data-pk");
            window.scrollTo(0,0);
            document.title = elem_.querySelector('title').innerHTML;
            if_list(rtr);
            window.history.pushState(null, "vfgffgfgf", "/communities/" + pk + "/");
        }
      }
      ajax_link.send(form_data);
});

on('#ajax', 'click', '.create_community_claim_btn', function() {
  form_data = new FormData(document.querySelector("#community_claim_form"));
  form_post = document.querySelector("#community_claim_form");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/managers/progs_community/create_claim/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    toast_info("Жалоба отправлена!");
    document.querySelector(".create_fullscreen").style.display = "none";
    document.getElementById("create_loader").innerHTML="";

  }};

  link_.send(form_data);
});



on('#ajax', 'click', '.member_create', function() {
  send_with_pk_and_reload("/communities/progs/add_member/")
})
on('#ajax', 'click', '.member_delete', function() {
  send_with_pk_and_reload("/communities/progs/delete_member/")
})

on('#ajax', 'click', '.member_follow_create', function() {
  send_with_pk_and_reload("/follows/add_member/")
})
on('#ajax', 'click', '.member_follow_delete', function() {
  send_with_pk_and_reload("/follows/delete_member/")
})
