$('body').on('click', '.track_add', function() {
  btn = $(this)
  block = btn.parent();
  pk = block.parent().data("pk");
  $.ajax({
      url: "/music/manage/add_track/" + pk + "/",
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

$('#ajax').on('click', '.jp-playlist-current .track_item', function() {
  track = $(this); li = track.parents('.infinite-item'); track_id = li.data('counter');
  my_playlist_stop(track_id); li.addClass("playlist_pause");
  });

$('#ajax').on('click', '.playlist_pause .track_item', function() {
  track = $(this); li = track.parents('.infinite-item'); track_id = li.data('counter');
  my_playlist_play(track_id); li.removeClass("playlist_pause")
  });

  $('#ajax').on('click', '.tag_playlist .track_item', function() {
    track = $(this); track_id = track.parents('.infinite-item').data('counter'); playlist_block = $('body').find('.music-dropdown'); tag_pk = track.parents('.ul_track_list').data('pk');
    if (!playlist_block.hasClass('tag_' + tag_pk)){
    $.ajax({
      url: "/music/manage/temp_tag/" + tag_pk + "/",
      success: function(data) {
        load_playlist(playlist_block);
        playlist_block.removeClass().addClass('dropdown-menu music-dropdown tag_' + tag_pk);
        setTimeout(function(){ my_playlist_play(track_id)},2000);
      }
    });
    }else{
      my_playlist_play(track_id);
    };
  });
  $('#ajax').on('click', '.genre_playlist .track_item', function() {
        track = $(this); track_id = track.parents('.infinite-item').data('counter'); playlist_block = $('body').find('.music-dropdown'); genre_pk = track.parents('.ul_track_list').data('pk');
      if (!playlist_block.hasClass('genre_' + genre_pk)){
      $.ajax({
        url: "/music/manage/temp_genre/" + genre_pk + "/",
        success: function(data) {
          load_playlist(playlist_block);
          playlist_block.removeClass().addClass('dropdown-menu music-dropdown user_' + genre_pk);
          setTimeout(function(){ my_playlist_play(track_id)},2000);
        }
      });
      }else{my_playlist_play(track_id);};
    });
    $('#ajax').on('click', '.user_playlist .track_item', function() {
          track = $(this); track_id = track.parents('.infinite-item').data('counter'); playlist_block = $('body').find('.music-dropdown'); user_pk = {{ user.pk }};
        if (!playlist_block.hasClass('user_' + user_pk)){
        $.ajax({

          url: "/music/manage/my_list/" + user_pk + "/",
          success: function(data) {
            load_playlist(playlist_block);
            playlist_block.removeClass().addClass('dropdown-menu music-dropdown user_' + user_pk);
            setTimeout(function(){ my_playlist_play(track_id)},2000);
          }
        });
        }else{my_playlist_play(track_id);};
      });
