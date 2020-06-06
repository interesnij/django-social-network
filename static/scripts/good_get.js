on('#ajax', 'click', '.u_good_detail', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("good_loader");
  open_fullscreen('/goods/user/good/' + pk + '/' + uuid + '/', loader)
});

on('#ajax', 'click', '#c_good_add', function() {
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("good_add_loader");
  open_fullscreen('/goods/community/add/' + pk + '/', loader)
});
on('#ajax', 'click', '#u_good_add', function() {
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("create_loader");
  open_fullscreen('/goods/user/add/' + pk + '/', loader)
});

on('#add_good_user_form', 'change', '#category', function() {
  var val = this.value;
  if (val == '') {
    document.getElementById('subcat').innerHTML = "";
  } else {
    var link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    link.open( 'GET', "/goods/progs/cat/" + val + "/", true );
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
