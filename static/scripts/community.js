
  $('#ajax').on('click', '.member_create', function() {
    var member_create = $(this);
    var pk = member_create.data('id');
  $.ajax({
      url: "/communities/add_community_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.member_delete', function() {
    var member_delete = $(this);
    var pk = member_delete.data('id');
  $.ajax({
      url: "/communities/delete_community_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.member_follow_create', function() {
    var member_follow_create = $(this);
    var pk = member_follow_create.data('id');
  $.ajax({
      url: "/follows/add_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });

  $('#ajax').on('click', '.member_follow_delete', function() {
    var member_follow_delete = $(this);
    var pk = member_follow_delete.data('id');
  $.ajax({
      url: "/follows/delete_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/reload/" + pk + "/");
      }
  });
  });
