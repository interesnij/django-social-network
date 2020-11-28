function case_user_notify() {
  console.log('заявки, дружба, приглашения...');
  new Audio('/static/audio/apple/stargaze.mp3').play();
}
function case_post_notify(uuid) {
    console.log('Реакции, репосты на записи');
    if (document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' )){
      post_update_votes(document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' ), uuid);
      new Audio('/static/audio/apple/nota.mp3').play();
    }
}

function case_post_create(request_user_id, uuid) {
  if (document.body.querySelector(".pk_saver") && document.body.querySelector(".pk_saver").getAttribute('data-pk') !=request_user_id) {
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
  link_.open('GET', "/posts/user/load_post/" + uuid + "/" + request_user_id + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          lenta = document.body.querySelector('.post_stream');
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          lenta.prepend(new_post);
          document.body.querySelector(".post_empty") ? document.body.querySelector(".post_empty").style.display = "none" : null}}
  link_.send()
}}

function case_message_create(request_user_id, chat_id, message_uuid) {
  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');

  if (document.body.querySelector(".chat_list_container")) {
  link_.open('GET', "/chat/message_progs/load_message/" + message_uuid + "/", true);
  link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

  link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          lenta = document.body.querySelector('.is_paginate');
          elem = link_.responseText;
          new_post = document.createElement("span");
          new_post.innerHTML = elem;
          lenta.querySelector('[data-pk=' + '"' + chat_id + '"' + ']') ? (li = lenta.querySelector('[data-pk=' + '"' + chat_id + '"' + ']'), li.innerHTML = new_post.querySelector("li").innerHTML)
          : lenta.prepend(new_post);
          new Audio('/static/audio/apple/message.mp3').play();
          document.body.querySelector(".message_empty") ? document.body.querySelector(".message_empty").style.display = "none" : null}}
  link_.send()
}
  else if (document.body.querySelector(".chat_container") && document.body.querySelector(".chat_container").getAttribute('data-pk') != chat_id) {
    link_.open('GET', "/chat/message_progs/load_chat_message/" + message_uuid + "/", true);
    link_.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    link_.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        lenta = document.body.querySelector('.is_paginate');
        elem = link_.responseText;
        new_post = document.createElement("span");
        new_post.innerHTML = elem;
        lenta.prepend(new_post);
        document.body.querySelector(".message_empty") ? document.body.querySelector(".message_empty").style.display = "none" : null}}
  link_.send()
} else {
      chats = document.body.querySelector(".new_unread_chats");
      chats.querySelector(".tab_badge") ? (count = chats.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''), count = count*1) : count = 0;
      tab_span = document.createElement("span");
      chats.classList.add("tab_badge", "badge-success");
      chats.innerHTML = "";tab_span.append(tab_span);
      new Audio('/static/audio/apple/message.mp3').play()
  }
}


request_user_id = document.body.querySelector(".userpic").getAttribute("data-pk");
notify = document.body.querySelector(".new_unread_notify");
notify.querySelector(".tab_badge") ? (notify_count = notify.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''), notify_count = notify_count*1) : notify_count = 0;
tab_span = document.createElement("span");
tab_span.classList.add("tab_badge", "badge-success");


ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
ws_path = ws_scheme + '://' + "раса.рус:8002" + "/notify/";
webSocket = new channels.WebSocketBridge();
webSocket.connect(ws_path);

webSocket.socket.onmessage = function(e){ console.log(e.data); };
webSocket.socket.onopen = function () {console.log("Соединение установлено!")};
webSocket.socket.onclose = function () {console.log("Соединение прервано...")};


webSocket.listen(function (event) {
  switch (event.key) {
      case "notification":
        console.log("уведомления, счетчики, и звуки");
        //if (event.recipient_id == request_user_id){
        //  if (event.name == "user_notify"){ case_user_notify() }
        //  else if (event.name == "post_notify"){ case_post_notify(event.post_id) }
        //  notify_count = notify_count * 1;notify_count += 1;tab_span.innerHTML = notify_count;notify.innerHTML = "";notify.append(tab_span);
        //}
        if (event.name == "user_notify"){ case_user_notify() }
        else if (event.name == "post_notify"){ case_post_notify(event.post_id) }
        notify_count = notify_count * 1;notify_count += 1;tab_span.innerHTML = notify_count;notify.innerHTML = "";notify.append(tab_span);
        break;

      case "create_item":
        console.log("отрисовка созданных элементов для пользователей на странице");
        if (event.creator_id != request_user_id){
          if (event.name == "post_create"){
            case_post_create(request_user_id, event.post_id)
          }
        }
        break;

    case "message":
      console.log("уведомления сообщений, звуки, отрисовка созданных элементов для участников чата");
      if (event.creator_id != request_user_id){
        if (event.name == "message_create"){case_message_create(request_user_id, event.chat_id, event.message_id);}
      }
      break;

    default:
      console.log('error: ', event);
      break;
  }
})
