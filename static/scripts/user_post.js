
on('#ajax', 'click', '#form_post_btn', function() {
  var form_post, form_data, lenta_load, pk, link_, elem

  form_data = new FormData(document.forms.new_post);
  form_post = document.querySelector("#form_post");
  lenta_load = form_post.parentElement.nextElementSibling;
  pk = lenta_load.querySelector(".stream").getAttribute("user-pk");

  link_ = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  link_.open( 'POST', "/posts/add_post/" + pk + "/", true );

  link_.onreadystatechange = function () {
  if ( this.readyState == 4 && this.status == 200 ) {
    elem = link_.responseText;
    new_post.innerHTML = elem.innerHTML;
    lenta_load.querySelector(".stream").prepend(new_post)
    lenta_load.querySelector(".post_empty") ? lenta_load.querySelector(".post_empty").style.display = "none" : console.log("post_empty не обнаружен");
  }};

  link_.send(form_data);
});

    //document.getElementById('id_text').value = "";
    //document.getElementById('for_images_upload').innerHTML = "";
    //document.getElementById('for_gallery').innerHTML = "";
    //document.getElementById('for_doc').innerHTML = "";
    //document.getElementById('for_good').innerHTML = "";
    //document.getElementById('for_question').innerHTML = "";
    //document.getElementById('for_settings').innerHTML = "";
