var cssSelector = {jPlayer: "#jquery_jplayer_1",cssSelectorAncestor: ".main-header"};
//var options = { swfPath: "/static/jquery.jplayer.swf", supplied: "oga, mp3", wmode: "window", smoothPlayBar: false, keyEnabled: true};
var playlist = document.querySelector("#user_playlist").getAttribute('data-list');
_playlist = JSON.parse(playlist);
var myPlaylist = new jPlayerPlaylist(cssSelector, _playlist);
document.querySelector(".music_header_btn").style.display = "block";

on('#ajax', 'click', '.tag_track', function(e) {
var track_id = this.getAttribute('data-counter');
var playlist_block = document.querySelector(".music-dropdown");
var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
if (!playlist_block.classList.contains('tag_' + tag_pk)){
  var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  playlist_link.open( 'GET', '/music/manage/temp_tag/' + tag_pk, true );
  playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      playlist_block.className = "";
      playlist_block.classList.add("dropdown-menu", "music-dropdown", "tag_" + tag_pk);
      new_playlist = document.querySelector("#export_playlist").getAttribute('data-list');
      pllll = JSON.parse(new_playlist);
      myPlaylist.setPlaylist(pllll);
      setTimeout(function(){ myPlaylist.play(track_id);},2000);
      }
    };
    playlist_link.send( null );
    }else{
      myPlaylist.play(track_id);
    };
  });

on('#ajax', 'click', '.genre_track', function(e) {
var track_id = this.getAttribute('data-counter');
var playlist_block = document.querySelector(".music-dropdown");
var genre_pk = document.querySelector(".genre_playlist").getAttribute('data-pk');
if (!playlist_block.classList.contains('genre_' + genre_pk)){
  var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  playlist_link.open( 'GET', '/music/manage/temp_genre/' + genre_pk, true );
  playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      playlist_block.className = "";
      playlist_block.classList.add("dropdown-menu", "music-dropdown", "genre_" + genre_pk);
      new_playlist = document.querySelector("#export_playlist").getAttribute('data-list');
      pllll = JSON.parse(new_playlist);
      myPlaylist.setPlaylist(pllll);
      setTimeout(function(){ myPlaylist.play(track_id);},2000);
      }
    };
    playlist_link.send( null );
    }else{
      myPlaylist.play(track_id);
    };
  });

on('#ajax', 'click', '.user_track', function(e) {
var track_id = this.getAttribute('data-counter');
var playlist_block = document.querySelector(".music-dropdown");
var user_pk = document.querySelector(".user_playlist").getAttribute('data-pk');
if (!playlist_block.classList.contains('user_' + user_pk)){
  var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  playlist_link.open( 'GET', '/music/manage/temp_list/' + user_pk, true );
  playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      playlist_block.className = "";
      playlist_block.classList.add("dropdown-menu", "music-dropdown", "user_" + user_pk);
      new_playlist = document.querySelector("#user_playlist").getAttribute('data-list');
      pllll = JSON.parse(new_playlist);
      myPlaylist.setPlaylist(pllll);
      setTimeout(function(){ myPlaylist.play(track_id);},2000);
      }
    };
    playlist_link.send( null );
    }else{
      myPlaylist.play(track_id);
    };
  });
