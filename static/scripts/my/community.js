/*!
   fullscreen's script of community
  */
$('#ajax').on('click', '.c_article_detail', function() {var item = $(this); var pk = item.data("pk"); var uuid = item.data("uuid"); $('#article_loader').html('').load("/article/read/" + pk + "/" + uuid + "/"); $('.article_fullscreen').show();});
$('#ajax').on('click', '.c_fullscreen', function() {var item = $(this); var pk = item.data("pk"); var uuid = item.data("uuid");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();});
$('#ajax').on('click', '.c_all_likes', function() {var btn = $(this); item = $(this).parents('.interaction'); var pk = item.data("pk"); var uuid = item.data("uuid");$('#votes_loader').html('').load("/window/all_community_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});
$('#ajax').on('click', '.c_all_dislikes', function() {var btn = $(this); item = $(this).parents('.interaction'); var pk = item.data("pk"); var uuid = item.data("uuid");$('#votes_loader').html('').load("/window/all_community_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});
$('#ajax').on('click', '.c_all_reposts', function() {var btn = $(this); item = $(this).parents('.interaction'); var pk = item.data("pk"); var uuid = item.data("uuid");$('#votes_loader').html('').load("/window/all_community_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();});

$('#ajax').on('click', '.photo_fullscreen_hide', function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty(); });
$('#ajax').on('click', '.item_fullscreen_hide', function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); });
$('#ajax').on('click', '.votes_fullscreen_hide', function() { $('.votes_fullscreen').hide(); $('#votes_loader').empty(); });
$('#ajax').on('click', '.article_fullscreen_hide', function() {$('.article_fullscreen').hide(); $('#article_loader').empty();});


/*!
   card headers manage scripts
  */
$('#ajax').on('click', '.item_community_remove', function() {var link = $(this).parent(); var pk = link.data('id'); var uuid = link.data('uuid');$.ajax({url: "/community/delete/" + pk + "/" + uuid + "/",success: function(data) {$(link).parents('.card').hide();$('.activefullscreen').hide();$.toast({heading: 'Информация',text: 'Запись успешно удалена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_community_fixed', function() {var link = $(this).parent(); var pk = link.parent().data('id'); var uuid = link.parent().data('uuid');$.ajax({url: "/community/fixed/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span style='cursor:pointer' class='dropdown-item item_community_unfixed'> Открепить</span>");$.toast({heading: 'Информация',text: 'Запись закреплена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.item_community_unfixed', function() {var link = $(this).parent(); var pk = link.parent().data('id'); var uuid = link.parent().data('uuid');$.ajax({url: "/community/unfixed/" + pk + "/" + uuid + "/",success: function(data) {link.parent().html("<span style='cursor:pointer' class='dropdown-item item_community_fixed'>Закрепить</span>");$.toast({heading: 'Информация',text: 'Запись откреплена!',showHideTransition: 'fade',icon: 'info'})}});});
$('#ajax').on('click', '.js-textareacopybtn', function() {btn = $(this);link = btn.find('.js-copytextarea');link.focus();link.select();try {var successful = document.execCommand('copy');var msg = successful ? 'successful' : 'unsuccessful';console.log('Copying text command was ' + msg);} catch (err) {console.log('Oops, unable to copy');}});


/*!
   get comment script of community
  */
$('#ajax').on('click', '.c_comment.comments_close', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = btn.data('pk'); var container = item.find(".load_comments");$.ajax({url: "/community/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() {item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");},success:function(data){container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");}}); return false;});

$('#ajax').on('click', '.c_comment.comments_open', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");container.empty(); btn.removeClass('comments_open').addClass("comments_close");});

$("#ajax").on('click', '.reply_comment', function() {var reply_comment_form = $(this); var objectUser = reply_comment_form.prev().text().trim(); var form = reply_comment_form.next().find(".text-comment"); form.val(objectUser + ', '); reply_comment_form.next().show(); form.focus();})

/*!
   get votes script of community
  */
$("#ajax").on('click', '.c_like', function() {like = $(this); item = like.parents('.interaction'); pk = item.data('pk'); uuid = item.data('uuid'); dislike = like.next().next();$.ajax({url: "/votes/community_like/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").toggleClass('svg_success'); like.find(".likes_count").toggleClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count);dislike.find(".svg_default").removeClass('svg_danger'); dislike.find(".dislikes_count").removeClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$("#ajax").on('click', '.c_dislike', function() {var dislike = $(this); item = dislike.parents('.interaction'); var pk = item.data('pk'); var uuid = item.data('uuid'); var like = dislike.prev().prev();$.ajax({url: "/votes/community_dislike/" + uuid + "/" + pk + "/", type: 'POST', data: {'obj': pk},success: function(json) {like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger');dislike.find(".dislikes_count").toggleClass('svg_danger');dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")}}); return false;});

$('#ajax').on('click', '.c_repost', function() {var item = $(this); var item_id = item.data("uuid"); $('#user_item_pk').html(item_id);});

  $("#ajax").on('click', '.c_like2', function() {
            var like = $(this); var pk = like.data('pk'); var uuid = like.data('uuid'); var dislike = like.next().next();
            $.ajax({
                url: "/votes/community_comment/" + uuid + "/" + pk + "/like/", type: 'POST', data: {'obj': pk},
                success: function(json) {
                  like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");
                  dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")
                }
            }); return false;
        });

  $("#ajax").on('click', '.c_dislike2', function() {
          var dislike = $(this); var pk = dislike.data('pk'); var uuid = dislike.data('uuid'); var like = dislike.prev().prev();
          $.ajax({
              url: "/votes/community_comment/" + uuid + "/" + pk + "/dislike/",
              type: 'POST',
              data: { 'obj': pk },
              success: function(json) {
                like.find("[data-count='like']").text(json.like_count); like.find(".svg_default").removeClass('svg_success'); like.find(".likes_count").removeClass('svg_success'); like.siblings('.like_window').html('').load("/window/c_like_window/" + uuid + "/" + pk + "/");
                dislike.find("[data-count='dislike']").text(json.dislike_count); dislike.find(".svg_default").toggleClass('svg_danger'); dislike.find(".dislikes_count").toggleClass('svg_danger'); dislike.siblings('.dislike_window').html('').load("/window/c_dislike_window/" + uuid + "/" + pk + "/")
              }
          });   return false;
  });


  /*!
     comment create scripts
    */
  $('#ajax').on('click', '.comment_image', function() {
  		var photo = $(this); var pk = photo.data("id"); var uuid = photo.data("uuid");
  		$('#photo_loader').html('').load("/gallery/load/comment/" + pk + "/" + uuid + "/"); $('.photo_fullscreen').show();
  });
  $('#ajax').on('click', '.upload_photo', function() {
    btn = $(this); img_block = btn.parent().parent().prev();
    if (!img_block.empty()){img_block.empty()};
    img_block.append('<span class="close_upload_block" title="Закрыть панель загрузки фото"><svg fill="currentColor" style="width:15px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/>+<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div><div class="col-lg-6 col-md-6"><a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file2 hide_image" type="file" name="photo2" accept="image/*" id="id_item_comment_photo2"><div class="comment_photo2"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">+<path d="M0 0h24v24H0z" fill="none"/><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></h4></div></div>');img_block.show();
  });

    $('#ajax').on('click', '.comment_photo1', function() {
      var img = $(this); var entrou = false; var imageLoader = img.prev();
      imageLoader.click();
      $(imageLoader).on("change", function() {
          if (!entrou) { var imgPath = $(this)[0].value; var extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
              if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
                  if (typeof FileReader != "undefined") {
                      var image_holder = $(img); image_holder.empty(); var reader = new FileReader();
                      reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);
                  } } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();});

    });

    $('#ajax').on('click', '.comment_photo2', function() {
      var img = $(this); var entrou = false; var imageLoader = img.prev();
      imageLoader.click();
      $(imageLoader).on("change", function() {
          if (!entrou) { var imgPath = $(this)[0].value; var extn = imgPath.substring(imgPath.lastIndexOf(".") + 1).toLowerCase();
              if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
                  if (typeof FileReader != "undefined") {
                      var image_holder = $(img); image_holder.empty(); var reader = new FileReader();
                      reader.onload = function(e) { $img = $("<img />", { id: "targetImageCrop", src: e.target.result, class: "thumb-image" }).appendTo(image_holder); }; image_holder.show(); reader.readAsDataURL($(this)[0].files[0]);
                  } } else { this.value = null; } } entrou = true; setTimeout(function() { entrou = false; }, 1000); img.prev().prev().show();});

    });
  $('#ajax').on('click', '.delete_thumb1', function(e) {e.preventDefault(); var a = $(this); a.parent().empty().append('<a href="#" style="display:none" class="delete_thumb1">Удалить</a><input class="file1 hide_image" type="file" name="photo" accept="image/*" id="id_item_comment_photo"><div class="comment_photo1"><h4 class="svg_default"><svg width="35" height="35" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg></h4></div>');});
  $('#ajax').on('click', '.close_upload_block', function() {$(this).parent().empty();});

  $("#ajax").on('click', '.reply_comment', function() {var reply_comment_form = $(this); var objectUser = reply_comment_form.prev().text().trim(); var form = reply_comment_form.next().find(".text-comment"); form.val(objectUser + ', '); reply_comment_form.next().show(); form.focus();})
  $('#ajax').on('click', '.u_comment.comments_open', function() {
    var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments"); container.empty(); btn.removeClass('comments_open').addClass("comments_close");
  });
  $('#ajax').on('click', '.select_photo', function() {uuid = $(this).data("uuid");$('#photo_loader').html("").load("/users/load/img_load/" + uuid + "/"); $('.photo_fullscreen').show();});


    $('#ajax').on('click', '.с_itemComment', function() {
        button1 = $(this); form1 = parent().parent().parent().parent(); upload_block = form1.find(".upload_block");
        $.ajax({
            url: '/community/post-comment/', data: new FormData($(form1)[0]), contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); form1.parent().prev().append(data); upload_block.empty()},
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации комментария нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}); },
        });
        return false;
    });

    $('#ajax').on('click', '.c_replyComment', function() {
        button = $(this); form2 = button.parent().parent().parent().parent(); block = form2.parent(); upload_block = form2.find(".upload_block"); reply_stream = block.next().next(); pk = button.data('pk'); uuid = button.data('uuid');
        $.ajax({
            url: '/community/reply-comment/' + uuid + "/" + pk + "/",
            data: new FormData($(form2)[0]),
            contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); reply_stream.addClass("replies_open"); block.hide(); upload_block.empty(); },
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
        });
        return false;
    });
    $('#ajax').on('click', '.c_replyParentComment', function() {
        button = $(this); form3 = button.parent().parent().parent().parent(); block = form3.parent(); upload_block = form3.find(".upload_block"); pk = button.data('pk'); uuid = button.data('uuid'); reply_stream = block.parents('.stream_reply_comments');
        $.ajax({
            url: '/community/reply-comment/' + uuid + "/" + pk + "/",
            data: new FormData($(form3)[0]), contentType: false, cache: false, processData: false, type: 'POST',
            success: function(data) { $(".form-control-rounded").val(""); reply_stream.append(data); block.hide(); upload_block.empty();},
            error: function(data) { $.toast({heading: 'Ошибка',text: 'Для публикации ответа нужно написать что-нибудь и/или вставить изображение(ия)',showHideTransition: 'fade',icon: 'error'}) },
        });
        return false;
    });
