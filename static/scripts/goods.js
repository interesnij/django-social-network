
$('.infinite-container').on('click', '.good_detail', function() {
    var good = $(this);
    var good_id = good.data("id");
    var user_uuid = good.data("uuid");
    $('#good_loader').html('').load("/goods/user/good/" + good_id + "/" + user_uuid + "/")
    $('.good_fullscreen').show();
});

$('#ajax').on('click', '.good_fullscreen_hide', function() {
    $('.good_add_fullscreen').hide();
    $('#good_add_loader').empty();
});
