function case_user_notify() {
  console.log('заявки, дружба, приглашения...');
  new Audio('/static/audio/apple/stargaze.mp3').play();
}
function case_post_notify(uuid) {
    console.log('Реакции, репосты на записи');
    if (document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' )){
      post = document.body.querySelector( '[data-uuid=' + '"' + uuid + '"' + ']' );
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
          document.body.querySelector(".post_empty") ? document.body.querySelector(".post_empty").style.display = "none" : null
      }
  };

  link_.send()
}
}


request_user_id = document.body.querySelector(".userpic").getAttribute("data-pk");
notify = document.body.querySelector(".new_unread_notify");
notify.querySelector(".tab_badge") ? (notify_count = notify.querySelector(".tab_badge").innerHTML.replace(/\s+/g, ''), notify_count = notify_count*1) : notify_count = 0;

ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
ws_path = ws_scheme + '://' + "раса.рус:8002" + "/notify/";
webSocket = new channels.WebSocketBridge();
webSocket.connect(ws_path);


webSocket.socket.onmessage = function(e){ console.log(e.data); };
webSocket.socket.onopen = function () {
  console.log("Соединение установлено!");
};

webSocket.socket.onclose = function () {
  console.log("Соединение прервано...");
};
tab_span = document.createElement("span");
tab_span.classList.add("tab_badge", "badge-danger");



webSocket.listen(function (event) {
  switch (event.key) {
      case "notification":
        console.log("notification");
        if (event.recipient_id == request_user_id){

          if (event.name == "user_notify"){ case_user_notify() }
          else if (event.name == "post_notify"){ case_post_notify(event.post_id) }

          notify_count = notify_count * 1;
          notify_count += 1;
          tab_span.innerHTML = notify_count;
          notify.innerHTML = "";
          notify.append(tab_span);
        }
        break;

      case "create_item":
        console.log("create_item");
        if (event.creator_id != request_user_id){
          if (event.name == "post_create"){
            case_post_create(request_user_id, event.post_id)
          }
          else {
            console.log("not post_create")
          }
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
      break;
  }
})
