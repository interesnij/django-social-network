		new FWDMSP({
				//main settings
				instanceName:"player1",
				playlistsId:"audio_playlists",
				mainFolderPath:"/static/images/",
				skinPath:"audio_white",
				showSoundCloudUserNameInTitle:"no",   // показывать имя пользователя soundcloud
				showMainBackground:"yes",  						// показать общий фон
				position:"bottom",         						// расположение плеера
				useDeepLinking:"yes",									// использовать глубокие ссылки - защита от перехвата
				useYoutube:"no",											// использовать youtube файлы
				useVideo:"no",												// использовать видео файлы
				rightClickContextMenu:"no",           // показ контекстног меню по щелчку правой кнопкой мыши
				showButtonsToolTips:"no",             // показать всплывающие подсказки кнопок
				addKeyboardSupport:"yes",             // добавить поддержку клавиатуры
				animate:"yes",												// фнимация
				autoPlay:"no",												// автостарт плеера
				loop:"no",														// повтор песни
				shuffle:"no",													// перемешивание треков
				maxWidth:850,                         // максимальная ширина
				volume:.8,														// громкость по умолчанию 80%
				// toolTipsButtonsHideDelay:1.5,         // задержка всплывающих подсказок для кнопок
				toolTipsButtonFontColor:"#888888",
				//controller settings
				showControllerByDefault:"yes",
				showThumbnail:"yes",
				showFullScreenButton:"yes",
				showNextAndPrevButtons:"yes",
				showSoundAnimation:"yes",
				showLoopButton:"yes",
				showShuffleButton:"yes",
				showDownloadMp3Button:"yes",
				showBuyButton:"yes",
				showShareButton:"yes",
				showMainScrubberAndVolumeScrubberToolTipLabel:"yes",
				expandBackground:"no",
				titleColor:"#000000",
				timeColor:"#919191",
				scrubbersToolTipLabelBackgroundColor:"#FFFFFF",
				scrubbersToolTipLabelFontColor:"#5a5a5a",
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
				showPlaylistsSearchInput:"yes",
				usePlaylistsSelectBox:"yes",
				showPlaylistsSelectBoxNumbers:"yes",
				showPlaylistsButtonAndPlaylists:"yes",
				showPlaylistsByDefault:"no",
				thumbnailSelectedType:"opacity",
				startAtPlaylist:0,
				startAtTrack:0,
				startAtRandomTrack:"no",
				buttonsMargins:0,
				thumbnailMaxWidth:330,
				thumbnailMaxHeight:330,
				horizontalSpaceBetweenThumbnails:40,
				verticalSpaceBetweenThumbnails:40,
				mainSelectorBackgroundSelectedColor:"#FFFFFF",
				mainSelectorTextNormalColor:"#737373",
				mainSelectorTextSelectedColor:"#000000",
				mainButtonTextNormalColor:"#7C7C7C",
				mainButtonTextSelectedColor:"#FFFFFF",
				//playlist settings
				playTrackAfterPlaylistLoad:"no",
				showPlayListButtonAndPlaylist:"yes",
				showPlayListOnAndroid:"yes",
				showPlayListByDefault:"no",
				showPlaylistItemPlayButton:"yes",
				showPlaylistItemDownloadButton:"yes",
				showPlaylistItemBuyButton:"yes",
				forceDisableDownloadButtonForPodcast:"yes",
				forceDisableDownloadButtonForOfficialFM:"yes",
				forceDisableDownloadButtonForFolder:"yes",
				addScrollBarMouseWheelSupport:"yes",
				showTracksNumbers:"yes",
				playlistBackgroundColor:"#000000",
				trackTitleNormalColor:"#737373",
				trackTitleSelectedColor:"#000000",
				trackDurationColor:"#7C7C7C",
				maxPlaylistItems:30,
				nrOfVisiblePlaylistItems:12,
				trackTitleOffsetLeft:0,
				playPauseButtonOffsetLeftAndRight:11,
				durationOffsetRight:9,
				downloadButtonOffsetRight:11,
				scrollbarOffestWidth:7,
				//playback rate / speed
				showPlaybackRateButton:"yes",
				defaultPlaybackRate:1, //min - 0.5 / max - 3
				playbackRateWindowTextColor:"#888888",
				//search bar settings
				showSearchBar:"yes",
				showSortButtons:"yes",
				searchInputColor:"#999999",
				searchBarHeight:38,
				inputSearchTextOffsetTop:1,
				inputSearchOffsetLeft:0,
				//password window
				borderColor:"#333333",
				mainLabelsColor:"#FFFFFF",
				secondaryLabelsColor:"#a1a1a1",
				textColor:"#5a5a5a",
				inputBackgroundColor:"#000000",
				inputColor:"#FFFFFF",
				//opener settings
				openerAlignment:"right",
				showOpener:"yes",
				showOpenerPlayPauseButton:"yes",
				openerEqulizerOffsetLeft:3,
				openerEqulizerOffsetTop:-1,
				//popup settings
				showPopupButton:"yes",
				popupWindowBackgroundColor:"#878787",
				popupWindowWidth:850,
				popupWindowHeight:423,
				//a to b loop
				atbTimeBackgroundColor:"transparent",
				atbTimeTextColorNormal:"#888888",
				atbTimeTextColorSelected:"#FFFFFF",
				atbButtonTextNormalColor:"#888888",
				atbButtonTextSelectedColor:"#FFFFFF",
				atbButtonBackgroundNormalColor:"#FFFFFF",
				atbButtonBackgroundSelectedColor:"#000000",
			});
