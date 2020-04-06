
on('#ajax', 'click', '#form_post_btn', function() {
  var form_post, formEntries, options, lenta_load, pk

  form_post = document.getElementById('form_post');
  formEntries = new FormData(form_post);
  options = {method: 'POST',body: formEntries,};

  lenta_load = form_post.parentElement.nextElementSibling;
  pk = lenta_load.querySelector(".stream").getAttribute("user-pk");
  fetch("/posts/add_post/" + pk + "/", options).then(data => {
    //document.getElementById('id_text').value = "";
    //document.getElementById('for_images_upload').innerHTML = "";
    //document.getElementById('for_gallery').innerHTML = "";
    //document.getElementById('for_doc').innerHTML = "";
    //document.getElementById('for_good').innerHTML = "";
    //document.getElementById('for_question').innerHTML = "";
    //document.getElementById('for_settings').innerHTML = "";
    lenta_load.querySelector(".stream").prepend(data);
    lenta_load.querySelector(".post_empty").style.display = "none";

  }).catch(error => {console.log("Все не ОК")})
});
