function msToTime(duration) {
  var milliseconds = parseInt((duration % 1000) / 100),
    seconds = Math.floor((duration / 1000) % 60),
    minutes = Math.floor((duration / (1000 * 60)) % 60);

  minutes = (minutes < 10) ? "0" + minutes : minutes;
  seconds = (seconds < 10) ? "0" + seconds : seconds;

  return minutes + ":" + seconds;
}


music_player = new FWDMSP({
		//main settings
		instanceName:"player1",
		playlistsId:"audio_playlists",
		mainFolderPath:"/static/images/",
		skinPath:"audio_white",
		showSoundCloudUserNameInTitle:"no",   // показывать имя пользователя soundcloud
		showMainBackground:"yes",  						// показать общий фон
		verticalPosition:"bottom",                    // расположение плеера
		rightClickContextMenu:"developer",
		useDeepLinking:"no",									// использовать глубокие ссылки - защита от перехвата. Не будет работать с souncloud
		rightClickContextMenu:"no",           // показ контекстног меню по щелчку правой кнопкой мыши
		addKeyboardSupport:"no",             // добавить поддержку клавиатуры
		animate:"yes",												// фнимация
		autoPlay:"no",												// автостарт плеера
		loop:"no",														// повтор песни
		shuffle:"no",													// перемешивание треков
		maxWidth:850,                         // максимальная ширина
		volume:.8,														// громкость по умолчанию 80%

		// controller settings
		showControllerByDefault:"yes",        // показать контроллер по умолчанию
		showThumbnail:"yes",                  // показывать миниатюры
		showNextAndPrevButtons:"yes",					// показывать кнопки переключения треков
		showSoundAnimation:"yes",							// показывать анимацию музыкального воспроизведения
		showLoopButton:"yes",                 // показывать кнопку повтора треков
		showShuffleButton:"yes",              // показывать кнопку перемешивания треков
		expandBackground:"no",
		showBuyButton:"yes",
    showPlaylistItemBuyButton:"no",
		titleColor:"#000000",                 // цвет названия
		timeColor:"#919191",                  // цвет времени

		// настройки выравнивания и размера контроллера (подробно описаны в документации!)
		controllerHeight:76,                 // высота контроллера
		startSpaceBetweenButtons:9,          // начальное пространство между кнопками
		spaceBetweenButtons:8,               // пространство между кнопками
		separatorOffsetOutSpace:5,           // смещение разделителя вне пространства
		separatorOffsetInSpace:9,            // смещение разделителя в пространстве
		lastButtonsOffsetTop:14,             // смещение последних кнопок сверху
		allButtonsOffsetTopAndBottom:14,     // смещение всех кнопок вверх и вниз
		titleBarOffsetTop:13,                // смещение сверху секции названия
		mainScrubberOffsetTop:47,            // смещение сверху скруббера
		spaceBetweenMainScrubberAndTime:10,  // пространство между скруббером и секцией времени
		startTimeSpace:10,                   // пространство относительно начала в секуии времени
		scrubbersOffsetWidth:2,              // ширина смещения скруббера
		scrubbersOffestTotalWidth:0,         // общая ширина смещения скруббера
		volumeButtonAndScrubberOffsetTop:47, // всещение сверху скруббера и кнопки громкости
		spaceBetweenVolumeButtonAndScrubber:6,// пространство между скруббером и кнопкой громмкости
		volumeScrubberOffestWidth:4,         // смещение слева скруббера громкости
		scrubberOffsetBottom:10,             // сммещение скруббера снизу
		equlizerOffsetLeft:1,                // смещение эквалайзера влево

		//playlists window settings
		showPlaylistsSearchInput:"no",      // показывать поле поиска в плейлисте
		usePlaylistsSelectBox:"no",         // показывать поле плейлистов сверху выбранного плейлиста
		showPlaylistsSelectBoxNumbers:"no", // пронумеровать плейлисты в поле выбора плейлиста
		showPlaylistsButtonAndPlaylists:"yes", // показывать кнопку, вызывающую окно плейлистов сверху и сами плейлисты
		showPlaylistsByDefault:"no",         // показывать плейлист по умолчанию
		thumbnailSelectedType:"opacity",     // тип выбора миниатюры (к примеру прозрачность)
		startAtPlaylist:0,                   // воспроизводить с плейлиста номер...
		startAtTrack:0,                      // воспроизводить с трека номер...
		startAtRandomTrack:"no",             // воспроизводить со случайного трека...
		buttonsMargins:0,                    // отступы кнопок
		thumbnailMaxWidth:330,               // макс. ширина миниатюр
		thumbnailMaxHeight:330,              // макс. высота миниатюр
		horizontalSpaceBetweenThumbnails:40, // пространство между миниатюрами по горизонтали
		verticalSpaceBetweenThumbnails:40,   // пространство между миниатюрами по вертикали
		mainSelectorBackgroundSelectedColor:"#FFFFFF", // цвет фона выбранного
		mainSelectorTextNormalColor:"#737373",  // цвет текста селектора
		mainSelectorTextSelectedColor:"#000000", // цвет текста селектора выбранного
		mainButtonTextNormalColor:"#7C7C7C", // цвет текста кнопок
		mainButtonTextSelectedColor:"#FFFFFF", // цвет текста кнопок выбранных

		//playlist settings
		playTrackAfterPlaylistLoad:"no",     // воспроизведение трека после загрузки плейлиста
		//showPlayListButtonAndPlaylist:"yes",
		showPlayListOnAndroid:"yes",         // показывать плейлисты на android
		showPlayListByDefault:"no",          // показывть плейлист по умолчанию
		showPlaylistItemPlayButton:"yes",    // показать кнопку воспроизведения элемента плейлиста
		addScrollBarMouseWheelSupport:"yes",  // прокручивать колесиком мыши
		showTracksNumbers:"yes",							// показывать номер трека
		playlistBackgroundColor:"#000000",    // цвет фона плейлиста
		trackTitleNormalColor:"#737373",      // цвет заголовка трека
		trackTitleSelectedColor:"#000000",    // цвет заголовка выбранного трека
		trackDurationColor:"#7C7C7C",         // цвет времени трека
		maxPlaylistItems:30,                  // Макс. количество плейлистов
		nrOfVisiblePlaylistItems:12,          // число видимых элементов списка воспроизведения
		trackTitleOffsetLeft:0,               // смещение слева заголовка трека
		playPauseButtonOffsetLeftAndRight:11, // смещение слева и справа кнопки play
		durationOffsetRight:9,							  // смещение справа продолжительности трека
		scrollbarOffestWidth:7,               // шмрмна смещения полосы прокрутки

		//playback rate / speed
		showPlaybackRateButton:"yes",         // показать кнопку скорости воспроизведения
		defaultPlaybackRate:1, //min - 0.5 / max - 3 // скорость воспроизведения по умолчанию (от 0,5 до 3)
		playbackRateWindowTextColor:"#888888",// цвет текста на окне выбора скорости

		//search bar settings
		showSearchBar:"no",                  // показывать секцию поиска треков
		showSortButtons:"yes",                // показывать секцию сортировки треков
		searchInputColor:"#999999",						// цвет секции поиска
		searchBarHeight:38,									  // высота секции поиска
		inputSearchTextOffsetTop:1,           // смещение текста ввода поиска сверху
		inputSearchOffsetLeft:0,              // смещение текста ввода поиска слева

		//opener settings
		openerAlignment:"right",              // открывание
		showOpener:"yes",                     // показывать эффект
		showOpenerPlayPauseButton:"yes",      // показывать кнопку плей / пауза
		openerEqulizerOffsetLeft:3,           // сдвигание эквалайзера слева
		openerEqulizerOffsetTop:-1,           // сдвигание эквалайзера сверху

		//a to b loop
		atbTimeBackgroundColor:"transparent", // цвет фона "от / до"
		atbTimeTextColorNormal:"#888888",     // цвет текста "от / до"
		atbTimeTextColorSelected:"#FFFFFF",   // цвет выбранного текста "от / до"
		atbButtonTextNormalColor:"#888888",   // цвет кнопки "от / до"
		atbButtonTextSelectedColor:"#FFFFFF", // цвет выбранной кнопки "от / до"
		atbButtonBackgroundNormalColor:"#FFFFFF", // цвет фона кнопки "от / до"
		atbButtonBackgroundSelectedColor:"#000000", // цвет фона выбранной кнопки "от / до"
	});

FWDMSPUtils.onReady(function(){
        music_player.addListener(FWDMSP.READY, music_onReady);
        music_player.addListener(FWDMSP.PLAY, music_onPlay);
        music_player.addListener(FWDMSP.PAUSE, music_onPause);
    });

function music_onReady(){console.log("Аудио плеер готов");}

function music_onPause(){
  try{
  div = document.createElement("div");
  div.innerHTML = music_player.getTrackTitle();
  title = div.querySelector('span').innerHTML;
  document.title = "Музыка приостановлена";
  if(document.querySelector(".user_status")){
    document.querySelector(".user_status").innerHTML = "Музыка приостановлена";
  }}catch{var a=0}
}
function music_onPlay(){
    console.log("Воспроизводится трек № : " + music_player.getTrackId());
    try{
    div = document.createElement("div");
    div.innerHTML = music_player.getTrackTitle();
    title = div.querySelector('span').innerHTML;
    document.title = title;
    if(document.querySelector(".user_status")){
      document.querySelector(".user_status").innerHTML = title;
    }}catch{var a=0};
    try{video_player.pause();}catch{var a=0}
};

function save_playlist(suffix, post_link, get_link, track_id){
    var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
    playlist_link.open( 'GET', post_link, true );
    playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      document.querySelector("body").className = "";
      document.querySelector("body").classList.add(suffix);

      var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      _link.open( 'GET', get_link, true );
      _link.onreadystatechange = function () {
        if ( _link.readyState == 4 && _link.status == 200 ) {
          var response = document.createElement('span');
          response.innerHTML = _link.responseText;
          var list = response.querySelectorAll("li");
          var count = list.length;
          for(i=0; i<count; i++) {
            _source=list[i].getAttribute("data-path") + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d';
            _title=list[i].getAttribute("data-title");
            _thumbPath=list[i].getAttribute("data-thumbpath");
            _duration=list[i].getAttribute("data-duration");
            time = msToTime(_duration);
            music_player.addTrack(_source, _title, _thumbPath, time, true, false, null);
          }
          music_player.loadPlaylist(0);
          if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
            console.log("Плейдист загружен!");
          setTimeout(function() {music_player.playSpecificTrack(suffix, track_id)}, 50);
        }
      }};
      _link.send( null );
    }};
    playlist_link.send( null );
    };


on('#ajax', 'click', '.tag_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('data-counter');
  var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("tag_" + tag_pk)){
    save_playlist("tag_" + tag_pk, '/music/manage/temp_tag/' + tag_pk, '/music/get/tag/' + tag_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейдист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("tag_" + tag_pk, track_id)}, 50);
  }
  }
  });

on('#ajax', 'click', '.genre_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('data-counter');
  var genre_pk = document.querySelector(".genre_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("genre_" + genre_pk)){
    save_playlist("genre_" + genre_pk, '/music/manage/temp_genre/' + genre_pk, '/music/get/genre/' + genre_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейдист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("genre_" + list_pk, track_id)}, 50);
  }
  }
});

on('#ajax', 'click', '.music_list_item', function() {
  var track_id = this.parentElement.parentElement.getAttribute('data-counter');
  var list_pk = document.querySelector(".music_playlist").getAttribute('data-pk');
  if (!document.body.classList.contains("list_" + list_pk)){
    save_playlist("list_" + list_pk, '/music/manage/temp_list/' + list_pk, '/music/get/list/' + list_pk, track_id)
  }else{
    music_player.loadPlaylist(0);
    if (FWDMSP.LOAD_PLAYLIST_COMPLETE){
      console.log("Плейлист загружен!");
    setTimeout(function() {music_player.playSpecificTrack("list_" + list_pk, track_id)}, 50);
  }
  }
});


on('#ajax', 'click', '#load_1', function(e) {
  music_player.loadPlaylist(0);
})
on('#ajax', 'click', '#load_2', function(e) {
  music_player.loadPlaylist(1);
})
on('#ajax', 'click', '#load_3', function(e) {
  music_player.loadPlaylist(2);
})

on('#ajax', 'click', '.track_add', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/manage/add_track/" + pk, true );
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='track_remove' title='Удалить'><svg xmlns='http://www.w3.org/2000/svg' fill='currentColor' style='width:22px;height:22px;' class='svg_default' viewBox='0 0 2424'><path fill='none' d='M0 0h24v24H0z'/><path d='M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z'/></svg></span>"
  }};
  _link.send( null );
});

on('#ajax', 'click', '.track_remove', function(e) {
  block = this.parentElement;
  pk = block.parentElement.getAttribute("data-pk");
  var _link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  _link.open( 'GET', "/music/manage/remove_track/" + pk, true );
  _link.onreadystatechange = function () {
    if ( _link.readyState == 4 && _link.status == 200 ) {
      block.innerHTML = "";
      block.innerHTML = "<span class='track_add' title='Добавить'><svg fill='currentColor' style='width:22px;height:22px;' class='svg_default' xmlns='http://www.w3.org/2000/svg' viewBox='0 024 24'><path d='M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z'/><path d='M0 0h24v24H0z' fill='none'/></svg></span>"
  }};
  _link.send( null );
});
