on('#ajax', 'click', '.send_manager_messages', function() {
  create_fullscreen("/managers/message/send_messages/", "worker_fullscreen");
});

on('#ajax', 'click', '#send_manager_messages_btn', function() {
  form = this.parentElement.parentElement.parentElement;
  _text = form.querySelector(".smile_supported").innerHTML;
  if (_text.replace(/<[^>]*(>|$)|&nbsp;|&zwnj;|&raquo;|&laquo;|&gt;/g,'').trim() == "" && form.querySelector(".files_0")){
    toast_error("Напишите или прикрепите что-нибудь");
    form.querySelector(".page_message_text").classList.add("border_red");
    return
  } else {
    this.disabled = true;
  };
  $input = document.createElement("input");
  $input.setAttribute("name", "text");
  $input.setAttribute("type", "hidden");
  $input.classList.add("input_text");
  $input.value = _text;
  form_post.append($input);
  form_data = new FormData(form);

    var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      ajax_link.open( 'POST', '/managers/message/send_messages/', true );
      ajax_link.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
      ajax_link.onreadystatechange = function () {
        if ( this.readyState == 4 && this.status == 200 ) {
            toast_success("Рассылка создана");
            close_work_fullscreen();
        } else {this.disabled = false}
      }
      ajax_link.send(form_data);
});
