on('#ajax', 'click', '.u_album_photo_detail', function() {
  var container, uuid, uuid2, pk, loader;
  container = this.parentElement;
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  uuid2 = container.getAttribute('data-uuid2');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/u_album_photo/" + pk + "/" + uuid + "/" + uuid2 + "/", loader)
});
on('#ajax', 'click', '.u_photo_detail', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = document.body.querySelector(".pk_saver").getAttribute('data-uuid');
  pk = this.getAttribute('photo-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/u_photo/" + pk + "/" + uuid + "/", loader)
});
on('#ajax', 'click', '.u_photos_add', function() {
  document.querySelector('#photos_add_window').style.display =="none";
})

on('#ajax', 'click', '#u_albums_add', function() {
  var container, uuid, loader;
  container = this.parentElement;
  uuid = this.getAttribute('data-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/user/add_album/" + uuid + "/", loader)
});

on('#ajax', 'click', '.u_photo_edit', function() {
  document.querySelector('#block_description_form').style.display =="none";
})
