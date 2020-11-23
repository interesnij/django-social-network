request_user_id = document.body.querySelector(".userpic").getAttribute("data-pk");

ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
ws_path = ws_scheme + '://' + "раса.рус:8001" + "/notify/post/";
webSocket = new channels.WebSocketBridge();
webSocket.connect(ws_path);

function plus_notify(){
  notify = document.body.querySelector(".new_unread_notify");
  notify.innerHTML ? (notify_count = notify.innerHTML.replace(/\s+/g, '')) : notify_count = 0;
  notify.innerHTML = int(notify_count) += 1;
  notify.classList.add("badge", "badge-danger");
}

webSocket.socket.onclose = function () {
  console.log("Disconnected from inbox stream");
};

webSocket.listen(function (event) {
  switch (event.key) {
    case "notification":
    if (event.creator_id === request_user_id) {
      null
    } else if (event.recipient_id === request_user_id) {
      plus_notify()
    }
      break;

    case "social_update":
      //document.body.querySelector("#notification").classList.add("badge", "badge-danger");
      update_social_activity(event.id_value);
      break;

    case "additional_news":
      if (event.creator_id === request_user_id) {
        $(".stream-update").show();
      }
      break;

    case "message":
      if (event.creator_id === request_user_id) {
        console.log("Вы создатель сообщения")
      };
      console.log(event.reseiver_ids);
      console.log(event.message_id);
      break;

    default:
      console.log('error: ', event);
      console.log(typeof (event))
      break;
  }
})

on('#ajax', 'click', '.user_create_chat', function() {
  loader = document.getElementById("item_loader");
  pk = this.getAttribute("data-pk");
  open_fullscreen("/chat/chat_progs/create_chat/" + pk + "/", loader)
});
on('#ajax', 'click', '.user_send_page_message', function() {
  loader = document.getElementById("item_loader");
  pk = this.getAttribute("data-pk");
  open_fullscreen("/chat/message_progs/send_page_message/" + pk + "/", loader)
});

on('#ajax', 'click', '.user_add_members', function() {
  block = this.nextElementSibling.querySelector("#chat_members");
  if (!block.querySelector(".load_pag")){
  block.classList.add("mt-4");
  list_load(block, "/users/load/friends/")
} else { block.style.display = "block"}
})

on('#ajax', 'click', '#add_chat_btn', function() {
  form = this.parentElement.parentElement.parentElement;
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

on('#ajax', 'click', '#send_page_message_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  this.disabled = true;
  pk = this.getAttribute("data-pk");
  form_data = new FormData(form);

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/chat/message_progs/send_page_message/' + pk + '/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            toast_success("Сообщение отправлено");
            document.querySelector(".item_fullscreen").style.display = "none";
            document.getElementById("item_loader").innerHTML="";
        }
      }
      ajax_link.send(form_data);
});

on('#ajax', 'click', '#message_post_btn', function() {
  form_post = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form_post);
  message_load = form_post.parentElement.parentElement.querySelector(".chatlist");
  pk = document.body.querySelector(".pk_saver").getAttribute("chat-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/chat/message_progs/send_message/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.text').value = "";
    clear_message_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    new_post.querySelector(".media") ? (message_load.append(new_post),
                                       message_load.querySelector(".message_empty") ? message_load.querySelector(".message_load").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.chat_ajax', function(e) {
  e.preventDefault();
	var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector(".chat_load_container");
        rtr = document.querySelector('.chat_load_container');
        rtr.innerHTML = ajax.innerHTML;
        scrollToBottom ("#scrolled");
        window.history.pushState(null, "vfgffgfgf", url);
				page = 2;
				loaded = false;
      }
    }
    ajax_link.send();
});
