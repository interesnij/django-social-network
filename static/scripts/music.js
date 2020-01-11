


$('body').on('click', '.track_add', function() {
  btn = $(this)
  block = btn.parent();
  pk = block.parent().data("pk");
  $.ajax({
      url: "/music/manage/add_track/",
      success: function (data) {
        $.toast({heading: 'Информация',text: 'Трек добавлен в Ваш основной плейлист!',showHideTransition: 'fade',icon: 'info'});
        btn.remove();
        block.append("<span class='track_remove' title='Удалить'><svg xmlns='http://www.w3.org/2000/svg' fill='currentColor' style='width:20px;' class='svg_default' viewBox='0 0 24 24'><path fill='none' d='M0 0h24v24H0z'/><path d='M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z'/></svg></span>")
      }
  });
});

$('body').on('click', '.track_remove', function() {
  btn = $(this)
  block = btn.parent();
  pk = block.parent().data("pk");
  $.ajax({
      url: "/music/manage/remove_track/" + pk + "/",
      success: function (data) {
        $.toast({heading: 'Информация',text: 'Трек удален из Вашего основного плейлиста!',showHideTransition: 'fade',icon: 'info'});
        btn.remove();
        block.append("<span class='track_add' title='Добавить'><svg fill='currentColor' style='width:25px;' class='svg_default' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/><path d='M0 0h24v24H0z' fill='none'/></svg></span>")
      }
  });
});

$(document).on("click.bs.dropdown.data-api", ".noclose", function (e) { e.stopPropagation() });
