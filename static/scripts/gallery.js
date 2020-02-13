
    $("#photos_add").click(function() {
        $('#photos_add_window').show();
    })

    $("#albums_add").click(function() {
        var user = $(this);
        var user_id = user.data("uuid");
        $('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/");
        $('.add_fullscreen').show();
    })
