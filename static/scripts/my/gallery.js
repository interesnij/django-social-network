
$('.photos-container').on('click', '.photo_detail', function() {
    photo = $(this); photo_id = photo.data("id"); user_uuid = photo.data("uuid");
    $('#photo_loader').html('').load("/gallery/load/photo/" + photo_id + "/" + user_uuid + "/")
    $('.photo_fullscreen').show();
});

$('.album-container').on('click', '.album_photo_detail', function() {
    photo = $(this); pk = photo.data("pk"); uuid = photo.data("uuid"); uuid2 = photo.data("uuid2");
    $('#photo_loader').html('').load("/gallery/load/u_photo/" + pk + "/" + uuid + "/" + uuid2 + "/")
    $('.photo_fullscreen').show();
});

Dropzone.options.inner = {
  init: function() {
    this.on("completemultiple", function(file) {
      console.log("fff");
    })
  },
};
