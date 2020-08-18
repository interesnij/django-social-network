{% if object.is_photo_repost %}
  {{ object.get_u_photo_repost|safe }}
{% elif object.is_photo_album_repost %}
  Пользователь поделился фотоальбомом!
{% elif object.get_good_repost %}
  {{ object.get_u_good_repost|safe }}
{% elif object.get_music_repost %}
  {% include 'generic/attach/repost_track.html' %}
{% elif object.is_music_list_repost %}
  Пользователь поделился плейлистом!
{% elif object.is_video_repost %}
  {{ object.get_u_video_repost|safe }}
{% elif object.is_video_list_repost %}
  Пользователь поделился видеоальбомом!
{% elif object.is_user_repost %}
  Пользователь поделился пользователем!
{% elif object.is_community_repost %}
  Пользователь поделился сообществом!
