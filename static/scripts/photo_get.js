on('#ajax', 'click', '.u_album_photo_detail', function() {
  var container, uuid, uuid2, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  uuid2 = container.getAttribute('data-uuid2');
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/u_album_photo/" + pk + "/" + uuid + "/" + uuid2 + "/", loader)
});
on('#ajax', 'click', '.u_photo_detail', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/u_photo/" + pk + "/" + uuid + "/", loader)
});
