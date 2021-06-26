on('#ajax', 'click', '.message', function() {
  btn_display = document.body.querySelector(".target_display");
  this.classList.contains("custom_color") ? (this.classList.remove("custom_color"),
                                             btn_display.querySelector(".settings_btn").style.display = "none",
                                             btn_display.querySelector(".type_display").style.display = "block")
                                          : (this.classList.add("custom_color"),
                                             btn_display.querySelector(".type_display").style.display = "none",
                                             btn_display.querySelector(".settings_btn").style.display = "block")
});

on('#ajax', 'click', '.message_dropdown', function() {this.nextElementSibling.classList.toggle("show")})

on('#ajax', 'input', '.message_text', function() {
  btn_block = this.nextElementSibling.nextElementSibling;
  if (this.value.trim() == ""){
     btn_block.querySelector("#voice_start_btn").style.display = "block";
     btn_block.querySelector("#message_post_btn").style.display = "none";
  } else {
    btn_block.querySelector("#voice_start_btn").style.display = "none";
    btn_block.querySelector("#message_post_btn").style.display = "block";
  }
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
