
  $('#ajax').on('click', '.member_create', function() {
    var member_create = $(this);
    var pk = member_create.data('id');
  $.ajax({
      url: "/communities/add_community_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/community_detail_reload/" + pk + "/");
        $('title').text('{{ object.name }}');
      }
  });
  });

  $('#ajax').on('click', '.member_delete', function() {
    var member_delete = $(this);
    var pk = member_delete.data('id');
  $.ajax({
      url: "/communities/delete_community_member/" + pk + "/",
      success: function () {
        $('#ajax').html('').load("/communities/community_detail_reload/" + pk + "/");
        $('title').text('{{ object.name }}');
      }
  });
  });
