
var goods_infinite = new Waypoint.Infinite({
    element: $('.goods-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
});

$("#good_add").click(function() {
    $('#good_add_loader').html('').load("{% url 'good_add_community' pk=user.pk %}");
    $('.good_add_fullscreen').show();
})
