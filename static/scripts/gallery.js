
    $(document).ready(function() {
        $('#albums_load').html('').load("/gallery/albums/" + "{{ user.uuid }}");
        $('#photos_load').html('').load("/gallery/photos/" + "{{ user.uuid }}");
    });

    $("#photos_add").click(function() { 
        $('#photos_add_window').show();
    })

    $("#albums_add").click(function() {
        $('#photo_add_loader').html('').load("/gallery/add_album/" + "{{ user.uuid }}");
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
