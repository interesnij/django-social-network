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
on('#ajax', 'click', '.user_community_create_window', function(e) {
  e.preventDefault();
  pk = this.getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/communities/progs/create_community_window/" + pk + "/", loader)
});
on('#ajax', 'click', '.community_claim', function() {
  this.parentElement.classList.remove("show");
  pk = document.body.querySelector(".pk_saver").getAttribute("data-pk");
  loader = document.getElementById("create_loader");
  open_fullscreen("/managers/progs_community/claim_window/" + pk, loader)
})
