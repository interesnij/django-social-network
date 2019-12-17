var infinite = new Waypoint.Infinite({
element: $('.users-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
});
