
    $("#photos_add").click(function() {
        $('#photos_add_window').show();
    })

    $("#albums_add").click(function() {
        var user = $(this);
        var user_id = user.data("uuid");
        $('#photo_add_loader').html('').load("/gallery/user/add_album/" + user_id + "/");
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

    var photos_infinite = new Waypoint.Infinite({
        element: $('.photos-container')[0],
        onBeforePageLoad: function() { $('.load').show(); },
        onAfterPageLoad: function($items) { $('.load').hide(); }
    });

    var albums_infinite = new Waypoint.Infinite({
        element: $('.albums-container')[0],
        onBeforePageLoad: function() { $('.load').show(); },
        onAfterPageLoad: function($items) { $('.load').hide(); }
    });
