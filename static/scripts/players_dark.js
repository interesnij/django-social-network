
music_player = new MUSIC({
    //main settings
    instanceName:"player1",
    playlistsId:"audio_playlists",
    mainFolderPath:"/static/images/",
    skinPath:"audio_dark",
    showSoundCloudUserNameInTitle:"no",
    position:"bottom",
    rightClickContextMenu:"developer",
    animate:"yes",
    autoPlay:"no",
    loop:"no",
    shuffle:"no",
    maxWidth:850,
    volume:.8,
    //controller settings
    showControllerByDefault:"yes",
    showThumbnail:"yes",
    showSoundAnimation:"yes",
    showLoopButton:"yes",
    showShuffleButton:"yes",
    showDownloadMp3Button:"yes",
    expandBackground:"no",
    titleColor:"#FFFFFF",
    timeColor:"#888888",
    //controller align and size settings (described in detail in the documentation!)
    controllerHeight:76,
    startSpaceBetweenButtons:9,
    spaceBetweenButtons:8,
    separatorOffsetOutSpace:5,
    separatorOffsetInSpace:9,
    lastButtonsOffsetTop:14,
    allButtonsOffsetTopAndBottom:14,
    titleBarOffsetTop:13,
    mainScrubberOffsetTop:47,
    spaceBetweenMainScrubberAndTime:10,
    startTimeSpace:10,
    scrubbersOffsetWidth:2,
    scrubbersOffestTotalWidth:0,
    volumeButtonAndScrubberOffsetTop:47,
    spaceBetweenVolumeButtonAndScrubber:6,
    volumeScrubberOffestWidth:4,
    scrubberOffsetBottom:10,
    equlizerOffsetLeft:1,
    //playlists window settings
    showPlaylistsButtonAndPlaylists:"yes",
    showPlaylistsByDefault:"no",
    thumbnailSelectedType:"opacity",
    startAtPlaylist:0,
    startAtTrack:0,
    buttonsMargins:0,
    thumbnailMaxWidth:330,
    thumbnailMaxHeight:330,
    horizontalSpaceBetweenThumbnails:40,
    verticalSpaceBetweenThumbnails:40,
    //playlist settings
    showPlayListButtonAndPlaylist:"yes",
    showPlayListOnAndroid:"yes",
    showPlayListByDefault:"no",
    showPlaylistItemPlayButton:"yes",
    showPlaylistItemDownloadButton:"yes",
    forceDisableDownloadButtonForPodcast:"no",
    forceDisableDownloadButtonForOfficialFM:"no",
    forceDisableDownloadButtonForFolder:"no",
    addScrollBarMouseWheelSupport:"no",
    showTracksNumbers:"yes",
    playlistBackgroundColor:"#000000",
    trackTitleNormalColor:"#888888",
    trackTitleSelectedColor:"#FFFFFF",
    trackDurationColor:"#888888",
    maxPlaylistItems:100,
    nrOfVisiblePlaylistItems:12,
    trackTitleOffsetLeft:0,
    playPauseButtonOffsetLeftAndRight:11,
    durationOffsetRight:9,
    downloadButtonOffsetRight:11,
    scrollbarOffestWidth:7,

    //opener settings
    openerAlignment:"right",
    showOpener:"yes",
    showOpenerPlayPauseButton:"yes",
    openerEqulizerOffsetLeft:3,
    openerEqulizerOffsetTop:-1,
});


if (document.querySelector("#video_player")) {
video_player = new FWDUVPlayer({
//main settings
instanceName:"player_dark",
parentId:"video_player",
playlistsId:"video_playlists",
mainFolderPath:"/static",
skinPath:"images/video_dark/",
displayType:"responsive",
					initializeOnlyWhenVisible:"no",
					useVectorIcons:"no",
					fillEntireVideoScreen:"no",
					fillEntireposterScreen:"yes",
					goFullScreenOnButtonPlay:"no",
					playsinline:"yes",
					privateVideoPassword:"428c841430ea18a70f7b06525d4b748a",
					youtubeAPIKey:'AIzaSyCgbixU3aIWCkiZ76h_E-XpEGig5mFhnVY',
					useHEXColorsForSkin:"no",
					normalHEXButtonsColor:"#666666",
					useDeepLinking:"yes",
					googleAnalyticsTrackingCode:"",
					useResumeOnPlay:"no",
					showPreloader:"yes",
					preloaderBackgroundColor:"#000000",
					preloaderFillColor:"#FFFFFF",
					addKeyboardSupport:"yes",
					autoScale:"yes",
					stopVideoWhenPlayComplete:"no",
					playAfterVideoStop:"no",
					autoPlay:"no",
					loop:"no",
					shuffle:"no",
					showErrorInfo:"yes",
					maxWidth:1170,
					maxHeight:659,
					volume:.8,
					backgroundColor:"#000000",
					videoBackgroundColor:"#000000",
					posterBackgroundColor:"#000000",
					//logo settings
					showLogo:"yes",
					hideLogoWithController:"yes",
					logoPosition:"topRight",
					logoLink:"",
					logoMargins:10,
					//playlists/categories settings
					usePlaylistsSelectBox:"yes",
					showPlaylistsButtonAndPlaylists:"yes",
					showPlaylistsByDefault:"no",
					thumbnailSelectedType:"opacity",
					startAtPlaylist:0,
					buttonsMargins:15,
					thumbnailMaxWidth:350,
					thumbnailMaxHeight:350,
					horizontalSpaceBetweenThumbnails:40,
					verticalSpaceBetweenThumbnails:40,
					inputBackgroundColor:"#333333",
					inputColor:"#999999",
					//playlist settings
					showPlaylistButtonAndPlaylist:"yes",
					playlistPosition:"right",
					showPlaylistByDefault:"yes",
					showPlaylistName:"yes",
					showLoopButton:"yes",
					showShuffleButton:"yes",
					showPlaylistOnFullScreen:"no",
					showNextAndPrevButtons:"yes",
					showThumbnail:"yes",
					forceDisableDownloadButtonForFolder:"yes",
					addMouseWheelSupport:"yes",
					startAtRandomVideo:"no",
					stopAfterLastVideoHasPlayed:"no",
					addScrollOnMouseMove:"no",
					randomizePlaylist:'no',
					folderVideoLabel:"VIDEO ",
					playlistRightWidth:320,
					playlistBottomHeight:380,
					startAtVideo:0,
					maxPlaylistItems:50,
					thumbnailWidth:71,
					thumbnailHeight:71,
					spaceBetweenControllerAndPlaylist:1,
					spaceBetweenThumbnails:1,
					scrollbarOffestWidth:8,
					scollbarSpeedSensitivity:.5,
					playlistBackgroundColor:"#000000",
					playlistNameColor:"#FFFFFF",
					thumbnailNormalBackgroundColor:"#1b1b1b",
					thumbnailHoverBackgroundColor:"#313131",
					thumbnailDisabledBackgroundColor:"#272727",
					youtubeAndFolderVideoTitleColor:"#FFFFFF",
					folderAudioSecondTitleColor:"#999999",
					youtubeOwnerColor:"#888888",
					youtubeDescriptionColor:"#888888",
					mainSelectorBackgroundSelectedColor:"#FFFFFF",
					mainSelectorTextNormalColor:"#FFFFFF",
					mainSelectorTextSelectedColor:"#000000",
					mainButtonBackgroundNormalColor:"#212021",
					mainButtonBackgroundSelectedColor:"#FFFFFF",
					mainButtonTextNormalColor:"#FFFFFF",
					mainButtonTextSelectedColor:"#000000",
					//controller settings
					showController:"yes",
					showControllerWhenVideoIsStopped:"yes",
					showNextAndPrevButtonsInController:"no",
					showRewindButton:"yes",
					showPlaybackRateButton:"yes",
					showVolumeButton:"yes",
					showTime:"yes",
					showQualityButton:"yes",
					showInfoButton:"yes",
					showDownloadButton:"yes",
					showShareButton:"yes",
					showEmbedButton:"yes",
					showChromecastButton:"no",
					showFullScreenButton:"yes",
					disableVideoScrubber:"no",
					showScrubberWhenControllerIsHidden:"yes",
					showDefaultControllerForVimeo:"no",
					repeatBackground:"yes",
					controllerHeight:42,
					controllerHideDelay:3,
					startSpaceBetweenButtons:7,
					spaceBetweenButtons:8,
					scrubbersOffsetWidth:2,
					mainScrubberOffestTop:14,
					timeOffsetLeftWidth:5,
					timeOffsetRightWidth:3,
					timeOffsetTop:0,
					volumeScrubberHeight:80,
					volumeScrubberOfsetHeight:12,
					timeColor:"#888888",
					youtubeQualityButtonNormalColor:"#888888",
					youtubeQualityButtonSelectedColor:"#FFFFFF",
					//advertisement on pause window
					aopwTitle:"Advertisement",
					aopwWidth:400,
					aopwHeight:240,
					aopwBorderSize:6,
					aopwTitleColor:"#FFFFFF",
					//subtitle
					subtitlesOffLabel:"Subtitle off",
					//popup add windows
					showPopupAdsCloseButton:"yes",
					//embed window and info window
					embedAndInfoWindowCloseButtonMargins:15,
					borderColor:"#333333",
					mainLabelsColor:"#FFFFFF",
					secondaryLabelsColor:"#a1a1a1",
					shareAndEmbedTextColor:"#5a5a5a",
					inputBackgroundColor:"#000000",
					inputColor:"#FFFFFF",
					//loggin
					isLoggedIn:"yes",
					playVideoOnlyWhenLoggedIn:"yes",
					loggedInMessage:"Please login to view this video.",
					//audio visualizer
					audioVisualizerLinesColor:"#ff9f00",
					audioVisualizerCircleColor:"#FFFFFF",
					//lightbox settings
					lightBoxBackgroundOpacity:.6,
					lightBoxBackgroundColor:"#000000",
					//sticky on scroll
					stickyOnScroll:"no",
					stickyOnScrollShowOpener:"yes",
					stickyOnScrollWidth:"700",
					stickyOnScrollHeight:"394",
					//sticky display settings
					showOpener:"yes",
					showOpenerPlayPauseButton:"yes",
					verticalPosition:"bottom",
					horizontalPosition:"center",
					showPlayerByDefault:"yes",
					animatePlayer:"yes",
					openerAlignment:"right",
					mainBackgroundImagePath:"content/minimal_skin_dark/main-background.png",
					openerEqulizerOffsetTop:-1,
					openerEqulizerOffsetLeft:3,
					offsetX:0,
					offsetY:0,
					//playback rate / speed
					defaultPlaybackRate:1, //0.25, 0.5, 1, 1.25, 1.2, 2
					//cuepoints
					executeCuepointsOnlyOnce:"no",
					//annotations
					showAnnotationsPositionTool:"no",
					//ads
					openNewPageAtTheEndOfTheAds:"no",
					playAdsOnlyOnce:"no",
					adsButtonsPosition:"left",
					skipToVideoText:"You can skip to video in: ",
					skipToVideoButtonText:"Skip Ad",
					adsTextNormalColor:"#888888",
					adsTextSelectedColor:"#FFFFFF",
					adsBorderNormalColor:"#666666",
					adsBorderSelectedColor:"#FFFFFF",
					//a to b loop
					useAToB:"yes",
					atbTimeBackgroundColor:"transparent",
					atbTimeTextColorNormal:"#888888",
					atbTimeTextColorSelected:"#FFFFFF",
					atbButtonTextNormalColor:"#888888",
					atbButtonTextSelectedColor:"#FFFFFF",
					atbButtonBackgroundNormalColor:"#FFFFFF",
					atbButtonBackgroundSelectedColor:"#000000",
					//thumbnails preview
					thumbnailsPreviewWidth:196,
					thumbnailsPreviewHeight:110,
					thumbnailsPreviewBackgroundColor:"#000000",
					thumbnailsPreviewBorderColor:"#666",
					thumbnailsPreviewLabelBackgroundColor:"#666",
					thumbnailsPreviewLabelFontColor:"#FFF",
					// context menu
					showContextmenu:'yes',
					showScriptDeveloper:"no",
					contextMenuBackgroundColor:"#1f1f1f",
					contextMenuBorderColor:"#1f1f1f",
					contextMenuSpacerColor:"#333",
					contextMenuItemNormalColor:"#888888",
					contextMenuItemSelectedColor:"#FFFFFF",
					contextMenuItemDisabledColor:"#444"
})

FWDUVPUtils.onReady(function(){
    video_player.addListener(FWDUVPlayer.READY, video_onReady);
    video_player.addListener(FWDUVPlayer.PLAY, video_onPlay);
});
}
MUSICUtils.onReady(function(){
        music_player.addListener(MUSIC.READY, music_onReady);
        music_player.addListener(MUSIC.PLAY, music_onPlay);
    });

function music_onReady(){console.log("Аудио плеер готов");}

function video_onReady(){console.log("Видео плеер готов");}

function video_onPlay(){
    console.log("Воспроизводится видео №: " + video_player.getVideoId());
    music_player.pause();
}
function music_onPlay(){
    console.log("Воспроизводится трек № : " + music_player.getTrackId());
    title = music_player.getTrackTitle();
    document.title = title.innerHTML;
    try{video_player.pause();}catch{var a=0}
};

on('#ajax', 'click', '.tag_track', function(e) {
var track_id = this.getAttribute('data-counter');
var tag_pk = document.querySelector(".tag_playlist").getAttribute('data-pk');
var category = 'tag_' + tag_pk;

if (!document.body.classList.contains(category)){
  var playlist_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
  playlist_link.open( 'GET', '/music/manage/temp_tag/' + tag_pk, true );
  playlist_link.onreadystatechange = function () {
    if ( playlist_link.readyState == 4 && playlist_link.status == 200 ) {
      var body = document.querySelector("body");
      body.className = "";body.classList.add(category);

      var tag_link = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject( 'Microsoft.XMLHTTP' );
      tag_link.open( 'GET', '/music/get/tag/' + tag_pk, true );
      tag_link.onreadystatechange = function () {
        if ( tag_link.readyState == 4 && tag_link.status == 200 ) {
          var _test_ = document.createElement('span');
          _test_.innerHTML = tag_link.responseText;
          var list = document.createElement('span');
          var cat = document.createElement('span');
          var audio_playlists = body.querySelector("#audio_playlists");
          var all_music_playlists = body.querySelector("#all_music_playlists");
          list = _test_.querySelector(".hide_list");
          cat = _test_.querySelector(".hide_cat");
          all_music_playlists.append(list);
          audio_playlists.append(cat);
          console.log(category);
          music_player = null;
          music_player = new MUSIC({
              //main settings
              instanceName:"player2",
              playlistsId:"audio_playlists",
              mainFolderPath:"/static/images/",
              skinPath:"audio_dark",
              showSoundCloudUserNameInTitle:"no",
              position:"bottom",
              rightClickContextMenu:"developer",
              animate:"yes",
              autoPlay:"no",
              loop:"no",
              shuffle:"no",
              maxWidth:850,
              volume:.8,
              //controller settings
              showControllerByDefault:"yes",
              showThumbnail:"yes",
              showSoundAnimation:"yes",
              showLoopButton:"yes",
              showShuffleButton:"yes",
              showDownloadMp3Button:"yes",
              expandBackground:"no",
              titleColor:"#FFFFFF",
              timeColor:"#888888",
              //controller align and size settings (described in detail in the documentation!)
              controllerHeight:76,
              startSpaceBetweenButtons:9,
              spaceBetweenButtons:8,
              separatorOffsetOutSpace:5,
              separatorOffsetInSpace:9,
              lastButtonsOffsetTop:14,
              allButtonsOffsetTopAndBottom:14,
              titleBarOffsetTop:13,
              mainScrubberOffsetTop:47,
              spaceBetweenMainScrubberAndTime:10,
              startTimeSpace:10,
              scrubbersOffsetWidth:2,
              scrubbersOffestTotalWidth:0,
              volumeButtonAndScrubberOffsetTop:47,
              spaceBetweenVolumeButtonAndScrubber:6,
              volumeScrubberOffestWidth:4,
              scrubberOffsetBottom:10,
              equlizerOffsetLeft:1,
              //playlists window settings
              showPlaylistsButtonAndPlaylists:"yes",
              showPlaylistsByDefault:"no",
              thumbnailSelectedType:"opacity",
              startAtPlaylist:0,
              startAtTrack:0,
              buttonsMargins:0,
              thumbnailMaxWidth:330,
              thumbnailMaxHeight:330,
              horizontalSpaceBetweenThumbnails:40,
              verticalSpaceBetweenThumbnails:40,
              //playlist settings
              showPlayListButtonAndPlaylist:"yes",
              showPlayListOnAndroid:"yes",
              showPlayListByDefault:"no",
              showPlaylistItemPlayButton:"yes",
              showPlaylistItemDownloadButton:"yes",
              forceDisableDownloadButtonForPodcast:"no",
              forceDisableDownloadButtonForOfficialFM:"no",
              forceDisableDownloadButtonForFolder:"no",
              addScrollBarMouseWheelSupport:"no",
              showTracksNumbers:"yes",
              playlistBackgroundColor:"#000000",
              trackTitleNormalColor:"#888888",
              trackTitleSelectedColor:"#FFFFFF",
              trackDurationColor:"#888888",
              maxPlaylistItems:100,
              nrOfVisiblePlaylistItems:12,
              trackTitleOffsetLeft:0,
              playPauseButtonOffsetLeftAndRight:11,
              durationOffsetRight:9,
              downloadButtonOffsetRight:11,
              scrollbarOffestWidth:7,

              //opener settings
              openerAlignment:"right",
              showOpener:"yes",
              showOpenerPlayPauseButton:"yes",
              openerEqulizerOffsetLeft:3,
              openerEqulizerOffsetTop:-1,
          });
          music_player.playSpecificTrack(category, track_id);
      }};
      tag_link.send( null );
  }};
    playlist_link.send( null );
    }else{
      music_player.playSpecificTrack(category, track_id);
    };
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
