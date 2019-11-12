
    $("#photos_add").click(function() {
        $('#photos_add_window').show();
    })

    $("#albums_add").click(function() {
        var user = $(this);
        var user_id = user.data("uuid");
        $('#photo_add_loader').html('').load("/gallery/user_add_album/" + user_id + "/"); 
        $('.add_fullscreen').show();
    })

    $('.add_fullscreen_hide').on('click', function() {
        $('.add_fullscreen').hide();
        $('#photo_loader').empty();
    });

    $('.photo_fullscreen_hide').on('click', function() {
        $('.photo_fullscreen').hide();
        $('#photo_loader').empty();
    });

    $('.infinite-container').on('click', '.photo_detail', function() {
        var photo = $(this);
        var photo_id = photo.data("id");
        var user_uuid = photo.data("uuid");
        $('#photo_loader').html('').load("/gallery/user_photo/" + photo_id + "/" + user_uuid + "/")
        $('.photo_fullscreen').show();
    });
