on('#ajax', 'click', '.user_create_chat', function() {
  loader = document.getElementById("create_loader");
  pk = this.getAttribute("data-pk");
  open_fullscreen("/chat/chat_progs/create_chat/" + pk + "/", loader)
});

on('#ajax', 'click', '.user_add_members', function() {
  block = this.parentElement.parentElement.parentElement.querySelector("#chat_members");
  list_load(block, "/users/load/friends/")
})

on('#ajax', 'click', '#add_chat_btn', function() {
  form = document.querySelector("#add_chat_form");
  this.disabled = true;
  pk = this.getAttribute("data-pk");
  form_data = new FormData(form);

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/chat/chat_progs/create_chat/' + pk + '/', true );
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
            window.history.pushState(null, "vfgffgfgf", "/chat/" + pk + "/");
        }
      }
      ajax_link.send(form_data);
});
