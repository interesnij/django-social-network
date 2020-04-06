
on('#ajax', 'click', '#form_post_btn', function() {
  var form_post, formEntries, options, stream, pk

  form_post = document.getElementById('form_post');
  formEntries = new FormData(form_post);
  options = {method: 'POST',body: formEntries,};

  stream = form_post.parentElement.nextElementSibling;
  pk = stream.querySelector(".stream").getAttribute("data-pk");
  fetch("/posts/add_post/" + pk + "/", options).then(data => {
    document.getElementById('id_text').value = "";
    document.getElementById('for_images_upload').innerHTML = "";
    document.getElementById('for_gallery').innerHTML = "";
    document.getElementById('for_doc').innerHTML = "";
    document.getElementById('for_good').innerHTML = "";
    document.getElementById('for_question').innerHTML = "";
    document.getElementById('for_settings').innerHTML = "";
    stream.querySelector(".stream").prepend(data);
    stream.querySelector(".post_empty").style.display = "none";

  }).catch(error => {console.log("Все не ОК")})
});
