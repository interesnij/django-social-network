function get_toggle_messages() {
  list = document.body.querySelectorAll(".custom_color");
  query = [];
  for (var i = 0; i < list.length; i++){
      query.push(list[i])
  };
  return query
}
function show_chat_console(is_favourite) {
  _console = document.body.querySelector(".console_btn_other");
  is_favourite ? (btn = _console.querySelector(".toggle_message_favourite"), btn.classList.add("active")) : null;

  list = document.body.querySelectorAll(".custom_color");
  query = [];
  for (var i = 0; i < list.length; i++){
      query.push(list[i])
  };

  _console.style.display = "unset";
  _console.previousElementSibling.style.display = "none";
  _console.parentElement.parentElement.querySelector("h5").style.display = "none"
}

function hide_chat_console(is_favourite) {
  _console = document.body.querySelector(".console_btn_other");
  is_favourite ? (btn = _console.querySelector(".toggle_message_favourite"), btn.classList.add("active")) : null;
  _console.style.display = "none";
  _console.previousElementSibling.style.display = "unset";
  _console.parentElement.parentElement.querySelector("h5").style.display = "unset"
}

on('#ajax', 'click', '.message_dropdown', function() {this.nextElementSibling.classList.toggle("show")})

on('#ajax', 'input', '.message_text', function() {
  check_message_form_btn()
}) 

on('#ajax', 'click', '.user_create_chat', function() {
  loader = document.getElementById("item_loader");
  pk = this.getAttribute("data-pk");
  open_fullscreen("/chat/user_progs/create_chat/" + pk + "/", loader)
});
on('#ajax', 'click', '.user_send_page_message', function() {
  loader = document.getElementById("item_loader");
  pk = this.getAttribute("data-pk");
  open_fullscreen("/chat/user_progs/send_page_message/" + pk + "/", loader)
});

on('#ajax', 'click', '.u_chat_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  pk = document.body.querySelector(".pk_saver").getAttribute('chat-pk')
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/chat_photo/" + pk + "/" + photo_pk + "/", loader)
});
on('#ajax', 'click', '.c_chat_photo', function() {
  photo_pk = this.getAttribute('photo-pk');
  pk = document.body.querySelector(".pk_saver").getAttribute('chat-pk')
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/community/chat_photo/" + pk + "/" + photo_pk + "/", loader)
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
      ajax_link.open( 'POST', '/chat/user_progs/create_chat/' + pk + '/', true );
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
      ajax_link.open( 'POST', '/chat/user_progs/send_page_message/' + pk + '/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            toast_success("Сообщение отправлено");
            document.querySelector(".item_fullscreen").style.display = "none";
            document.getElementById("item_loader").innerHTML="";
        } else {this.disabled = false}
      }
      ajax_link.send(form_data);
});

on('#ajax', 'click', '#message_post_btn', function() {
  form_post = this.parentElement.parentElement.parentElement;
  form_data = new FormData(form_post);
  message_load = form_post.parentElement.parentElement.querySelector(".chatlist");
  pk = document.body.querySelector(".pk_saver").getAttribute("chat-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/chat/user_progs/send_message/" + pk + "/", true );
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    form_post.querySelector('.text').value = "";
    clear_message_attach_block();

    elem = link_.responseText;
    new_post = document.createElement("span");
    new_post.innerHTML = elem;
    new_post.querySelector(".media") ? (message_load.append(new_post),
                                       message_load.querySelector(".item_empty") ? message_load.querySelector(".item_empty").style.display = "none" : null)
                                    :  toast_error("Нужно написать или прикрепить что-нибудь!");
  }};

  link_.send(form_data);
});

on('#ajax', 'click', '.chat_ajax', function(e) {
  _this = this;
  e.preventDefault();
	var url = this.getAttribute('href');
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url, true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        scrollToBottom ("#scrolled");
        window.history.pushState(null, "vfgffgfgf", url);
        m_page = 2;
        m_loaded = false;
        scrolled(window.location.href, '.chat_container', target = 0);
        _this.querySelector(".tab_badge") ? (chats = document.body.querySelector(".new_unread_chats"),
                                             all_count = chats.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''),
                                             all_count = all_count*1,
                                             result = all_count - 1,
                                             result > 0 ? chats.querySelector(".tab_badge").innerHTML = result : chats.innerHTML = '',
                                             console.log("Вычитаем 1, так как в чате есть непрочитанные сообщения")
                                           ) : null;
      }
    }
    ajax_link.send();
});

on('#ajax', 'click', '.toggle_message', function(e) {
  message = this.parentElement.parentElement;
  is_toggle = false, is_favourite = false;
  if (message.classList.contains("custom_color")) {
    message.classList.remove("custom_color");
    list = message.parentElement.querySelectorAll(".message");
    for (var i = 0; i < list.length; i++){
      if (list[i].classList.contains("custom_color")) {
        is_toggle = true
      };
      if (list[i].classList.contains("favourite")) {
        is_favourite = true
      }
    }
    is_toggle ? null : hide_chat_console(is_favourite)
  } else {
    message.classList.add("custom_color");
    show_chat_console(is_favourite)
  };
  if (get_toggle_messages().length > 1) {
    document.body.querySelector(".one_message").style.display = "none"
  } else {
    document.body.querySelector(".one_message").style.display = "unset"
  };
})

on('#ajax', 'click', '.toggle_message_favourite', function() {
  is_favourite = false;
  this.classList.contains("active") ? url = "/chat/user_progs/unfavorite_message/" : "/chat/user_progs/favorite/";

  list = get_toggle_messages();
  for (var i = 0; i < list.length; i++){
  ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'GET', url + list[i].getAttribute("data-uuid") + "/", true );
		ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        console.log("ok")
      }
    }
    ajax_link.send();
  };
  for (var i = 0; i < list.length; i++){
    if (list[i].classList.contains("favourite")) {
      is_favourite = true
    }
  }
  hide_chat_console(is_favourite)
});

on('#ajax', 'click', '.u_message_delete', function() {
  list = get_toggle_messages();
  for (var i = 0; i < list.length; i++){
    remove_item_and_show_restore_block(list[i], "/chat/user_progs/delete_message/", "u_message_restore", "Сообщение удалено")
  };
  hide_chat_console(null)
});

on('#ajax', 'click', '.u_message_restore', function() {
  item = this.parentElement.nextElementSibling;
  uuid = this.getAttribute("data-uuid");
  block = this.parentElement;
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/restore_message/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    block.remove();
    item.style.display = "flex";
    item.classList.remove("custom_color")
  }};
  link.send();
});

on('#ajax', 'click', '.u_message_fixed', function() {
  item = document.body.querySelector(".custom_color");

  uuid = this.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/fixed_message/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    hide_chat_console(null);
    item.classList.add("is_fixed");
    item.style.display = "none"
  }};
  link.send();
});
on('#ajax', 'click', '.u_message_unfixed', function() {
  item = this.parentElement.nextElementSibling;
  uuid = this.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/unfixed_message/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    hide_chat_console(null)
  }};
  link.send();
});
on('#ajax', 'click', '.u_message_reply', function() {
  item = this.parentElement.nextElementSibling;
  uuid = this.getAttribute("data-uuid");
  link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link.open( 'GET', "/chat/user_progs/reply_message/" + uuid + "/", true );
  link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link.onreadystatechange = function () {
  if ( link.readyState == 4 && link.status == 200 ) {
    hide_chat_console(null)
  }};
  link.send();
});
