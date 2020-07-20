
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
