on('#ajax', 'click', '.c_avatar_detail', function() {
  uuid = this.getAttribute('photo-uuid');
  loader = document.getElementById("photo_loader");
  open_fullscreen("/gallery/load/community_avatar_detail/" + uuid + "/", loader)
});
