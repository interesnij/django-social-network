on('#ajax', 'click', '.user_community_create_window', function(e) {
  e.preventDefault();
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/communities/progs/create_community_window/" + pk + "/", loader)
});

on('#ajax', 'click', '#add_community_btn', function() {
  form_data = new FormData(document.querySelector("#add_community_form"));
  pk = this.getAttribute("data-pk");
  uuid = this.getAttribute("data-uuid");
  var ajax_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    ajax_link.open( 'POST', "/communities/progs/add/" + pk + "/", true );
    ajax_link.onreadystatechange = function () {
      if ( this.readyState == 4 && this.status == 200 ) {
        elem_ = document.createElement('span');
        elem_.innerHTML = ajax_link.responseText;
        ajax = elem_.querySelector("#reload_block");
        rtr = document.getElementById('ajax');
        rtr.innerHTML = ajax.innerHTML;
        community_pk = rtr.querySelector(".pk_saver").getAttribute("data-pk");
        window.scrollTo(0,0);
        document.title = elem_.querySelector('title').innerHTML;
        Index.initLink();
        lenta_community = rtr.querySelector('#lenta_community');
        link = lenta_community.getAttribute("data-link");
        list_load(lenta_community, link);
        window.history.pushState({route: '/communities/' + community_pk + '/'}, "network", '/communities/' + community_pk + '/');
      }
    }
    ajax_link.send(form_data);
});

on('#ajax', 'change', '#sub_category', function() {
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
