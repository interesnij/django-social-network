$('body').on('click', '.track_add', function() {
  pk = $(this).parent().data("pk");
  $.ajax({
      url: "/music/manage/add_track/" + pk + "/",
      success: function (data) {
        $.toast({heading: 'Информация',text: 'Трек добавлен в Ваш основной плейлист!',showHideTransition: 'fade',icon: 'info'})
      }
  });
});
