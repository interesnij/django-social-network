on('#ajax', 'click', '.user_community_create_window', function(e) {
  e.preventDefault();
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/communities/progs/create_community_window/" + pk + "/", loader)
});

on('#ajax', 'click', '#create_video_list_btn', function() {
  form_data = new FormData(document.querySelector("#video_list_create"));
  pk = this.getAttribute("data-pk");
  uuid = this.getAttribute("data-uuid");
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/video/progs/create_list/" + pk + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        uuid = rtr.querySelector(".uuid_saver").getAttribute("album-uuid");
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;
        Index.initLink();
        window.history.pushState({route: '/users/detail/video_list/' + pk + '/' + uuid + '/'}, "network", '/users/detail/video_list/' + pk + '/' + uuid + '/');
      }
    }
    ajax_link.send(form_data);
});

document.querySelector("#sub_category").addEventListener( 'change', function() {
    var val = this.value;
    if (val == '') {
      document.getElementById('subcat').innerHTML = "";
    } else {
      var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      link.open( 'GET', "/communities/progs/cat/" + val + "/", true );
      link.onreadystatechange = function () {
        if ( link.readyState == 4 ) {
            if ( link.status == 200 ) {
                var sub = document.getElementById("subcat");
                sub.innerHTML = link.responseText;
            }
        }
    };
    link.send( null );
    };
});
