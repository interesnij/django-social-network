
$('.infinite-container').on('click', '.good_detail', function() {
    var good = $(this);
    var good_id = good.data("id");
    $('#good_loader').html('').load("/goods/user_good/" + good_id) 
    $('.good_fullscreen').show();
});

var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function() {
        $('.load').show();
    },
    onAfterPageLoad: function($items) {
        $('.load').hide();
    }
});

$('#ajax').on('click', '.good_fullscreen_hide', function() {
    $('.good_add_fullscreen').hide();
    $('#good_add_loader').empty();
});
