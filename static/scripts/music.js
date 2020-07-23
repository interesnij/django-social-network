on('#ajax', 'click', '.u_soundcloud_set', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = document.body.querySelector(".pk_saver").getAttribute('data-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/music/manage/user_progs/" + pk, loader)
});
