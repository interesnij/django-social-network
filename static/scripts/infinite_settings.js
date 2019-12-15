var infinite_item_comments = new Waypoint.Infinite({
    element: $('.stream_comments')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
});

var all_users_infinite = new Waypoint.Infinite({
      element: $('.all-users-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
  });

  var common_infinite = new Waypoint.Infinite({
      element: $('.common-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
  });

  var frends_infinite = new Waypoint.Infinite({
      element: $('.frends-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
  });

  var online_infinite = new Waypoint.Infinite({
      element: $('.online-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
  });
  var goods_infinite = new Waypoint.Infinite({
      element: $('.goods-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
  });

  var photos_infinite = new Waypoint.Infinite({
          element: $('.photos-container')[0], onBeforePageLoad: function() { $('.load').show(); }, onAfterPageLoad: function($items) { $('.load').hide(); }
      });
